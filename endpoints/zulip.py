import json
import traceback
import re
from typing import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint
import zulip


class ZulipEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        Handles incoming outgoing webhooks from Zulip.
        """
        # Get retry handling from settings
        retry_num = r.headers.get("X-Zulip-Retry-Num")
        if (not settings.get("allow_retry") and retry_num is not None and int(retry_num) > 0):
            return Response(status=200, response="ok")
        
        try:
            # Parse data according to Zulip outgoing webhook format
            # Can be JSON or form-encoded
            data = {}
            
            # Try JSON first
            if r.is_json:
                data = r.get_json() or {}
            elif r.form:
                # Form-encoded data
                data = r.form.to_dict()
            
            if not data:
                return Response(status=200, response="ok")
            
            # Extract message information from Zulip outgoing webhook format
            # According to docs: bot_email, bot_full_name, data, trigger, message
            message_content = data.get("data", "")  # The actual message content
            trigger = data.get("trigger", "")  # "mention" or "direct_message"
            bot_email = data.get("bot_email", "")
            bot_full_name = data.get("bot_full_name", "")
            
            # Message object contains sender info and metadata
            message_obj = data.get("message", {})
            if isinstance(message_obj, str):
                try:
                    message_obj = json.loads(message_obj)
                except json.JSONDecodeError:
                    message_obj = {}
            
            sender_email = message_obj.get("sender_email", "")
            sender_full_name = message_obj.get("sender_full_name", "")
            stream_name = message_obj.get("display_recipient", "")
            topic = message_obj.get("subject", "")  # In Zulip API, topic is called "subject"
            message_type = message_obj.get("type", "")  # "stream" or "private"
            
            # Skip if no message content
            if not message_content or not message_content.strip():
                return Response(status=200, response="ok")
            
            # Skip messages from the bot itself
            bot_email_setting = settings.get("zulip_email", "")
            if sender_email == bot_email_setting:
                return Response(status=200, response="ok")
            
            # Check if bot should respond to this message
            if self._should_respond_to_message(trigger, message_content, bot_email_setting):
                # Clean the message content (remove bot mention if present)
                clean_message = self._clean_message_content(message_content, bot_email_setting)
                
                if clean_message.strip():
                    try:
                        # Get response from Dify app
                        response = self.session.app.chat.invoke(
                            app_id=settings["app"]["app_id"],
                            query=clean_message,
                            inputs={},
                            response_mode="blocking",
                        )
                        
                        # Send response back to Zulip
                        if response and response.get("answer"):
                            self._send_zulip_response(
                                response.get("answer"), 
                                settings,
                                sender_email,
                                stream_name if message_type == "stream" else None,
                                topic if message_type == "stream" else None
                            )
                        
                        return Response(
                            status=200,
                            response="ok",
                            content_type="text/plain"
                        )
                        
                    except Exception as e:
                        error_msg = "Sorry, I'm having trouble processing your request. Please try again later."
                        self._send_zulip_response(
                            error_msg, 
                            settings,
                            sender_email,
                            stream_name if message_type == "stream" else None,
                            topic if message_type == "stream" else None
                        )
                        return Response(
                            status=200,
                            response="ok",
                            content_type="text/plain"
                        )
                        
            return Response(status=200, response="ok")
                
        except Exception as e:
            # Log error but return 200 to avoid webhook retries
            return Response(
                status=200,
                response="ok",
                content_type="text/plain"
            )
    
    def _should_respond_to_message(self, trigger: str, message: str, bot_email: str) -> bool:
        """
        Determine if the bot should respond to this message.
        """
        # Always respond to direct messages
        if trigger == "direct_message" or trigger == "private_message":
            return True
        
        # Always respond to mentions
        if trigger == "mention":
            return True
        
        # For backward compatibility, check content for mentions
        bot_name = bot_email.split('@')[0] if '@' in bot_email else bot_email
        mention_patterns = [
            f"@{bot_email}",           # Email mention
            f"@{bot_name}",            # Name mention
            f"@**{bot_name}**",        # Zulip @**name** mention
        ]
        
        message_lower = message.lower()
        for pattern in mention_patterns:
            if pattern.lower() in message_lower:
                return True
            
        return False
    
    def _clean_message_content(self, content: str, bot_email: str) -> str:
        """
        Clean message content by removing bot mentions.
        """
        bot_name = bot_email.split('@')[0] if '@' in bot_email else bot_email
        
        # Remove various mention patterns
        patterns_to_remove = [
            f"@{bot_email}",
            f"@{bot_name}",
            r"@\*\*[^*]+\*\*",  # @**name** patterns
        ]
        
        cleaned = content
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def _send_zulip_response(self, response_text: str, settings: Mapping, 
                           sender_email: str, stream_name: str = None, topic: str = None):
        """
        Send response back to Zulip.
        """
        try:
            # Initialize Zulip client
            server_url = settings.get("zulip_server_url", "").rstrip('/')
            email = settings.get("zulip_email")
            api_key = settings.get("zulip_api_key")
            
            client = zulip.Client(
                email=email,
                api_key=api_key,
                site=server_url
            )
            
            # Determine response destination based on original message context
            if stream_name and topic:
                # Respond in the same stream and topic
                client.send_message({
                    "type": "stream",
                    "to": stream_name,
                    "topic": topic,
                    "content": response_text
                })
            else:
                # Respond privately to the sender
                client.send_message({
                    "type": "private",
                    "to": [sender_email],
                    "content": response_text
                })
                
        except Exception as e:
            # Log error but don't raise to avoid webhook failures
            pass 