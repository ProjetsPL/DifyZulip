import json
import traceback
import re
from typing import Mapping
from werkzeug import Request, Response
from dify_plugin import Endpoint
import requests


class ZulipEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        """
        try:
            data = r.get_json()
            if not data:
                return Response(status=400, response="No JSON data received")

            # Extract message data
            message = data.get('data', '')
            if not message:
                return Response(status=200, response="No message content")

            # Extract metadata
            sender_email = data.get('message', {}).get('sender_email', '')
            sender_full_name = data.get('message', {}).get('sender_full_name', '')
            stream_name = data.get('message', {}).get('display_recipient', '')
            subject = data.get('message', {}).get('subject', '')
            message_type = data.get('message', {}).get('type', 'stream')
            
            # Get bot email from settings
            bot_email = settings.get('bot_email', '')
            
            # Skip messages from the bot itself
            if sender_email == bot_email:
                return Response(status=200, response="Ignoring bot's own message")

            # Check if we should respond only to mentions
            respond_to_mentions_only = settings.get('respond_to_mentions_only', True)
            
            if respond_to_mentions_only:
                # Check if bot is mentioned in the message
                bot_mention_pattern = f"@**{bot_email.split('@')[0]}**"
                if bot_mention_pattern not in message:
                    return Response(status=200, response="Bot not mentioned")
                
                # Clean the mention from the message
                message = re.sub(r'@\*\*[^*]+\*\*\s*', '', message).strip()

            # Check allowed streams if configured
            allowed_streams = settings.get('allowed_streams', '')
            if allowed_streams and message_type == 'stream':
                allowed_list = [s.strip() for s in allowed_streams.split(',') if s.strip()]
                if allowed_list and stream_name not in allowed_list:
                    return Response(status=200, response="Stream not in allowed list")

            # Prepare context for Dify
            context = {
                'sender': sender_full_name,
                'sender_email': sender_email,
                'stream': stream_name if message_type == 'stream' else 'Private',
                'subject': subject
            }

            # Call Dify app
            try:
                response = self.session.app.chat.invoke(
                    app_id=settings["app"]["app_id"],
                    query=message,
                    inputs=context,
                    response_mode="blocking",
                )
                
                answer = response.get("answer", "Sorry, I couldn't process your request.")
                
                # Send response back to Zulip
                self._send_zulip_message(
                    settings=settings,
                    message_type=message_type,
                    stream_name=stream_name,
                    subject=subject,
                    sender_email=sender_email,
                    content=answer
                )
                
                return Response(
                    status=200,
                    response=json.dumps({"status": "success", "response": answer}),
                    content_type="application/json"
                )
                
            except Exception as e:
                err = traceback.format_exc()
                error_msg = "Sorry, I'm having trouble processing your request. Please try again later."
                
                # Send error message back to Zulip
                self._send_zulip_message(
                    settings=settings,
                    message_type=message_type,
                    stream_name=stream_name,
                    subject=subject,
                    sender_email=sender_email,
                    content=error_msg
                )
                
                return Response(
                    status=200,
                    response=json.dumps({"status": "error", "error": str(e)}),
                    content_type="application/json"
                )
                
        except Exception as e:
            err = traceback.format_exc()
            return Response(
                status=500,
                response=json.dumps({"error": str(e), "traceback": err}),
                content_type="application/json"
            )

    def _send_zulip_message(self, settings: Mapping, message_type: str, stream_name: str, 
                           subject: str, sender_email: str, content: str):
        """Send message back to Zulip using API"""
        try:
            zulip_url = settings.get('zulip_site_url', '').rstrip('/')
            bot_email = settings.get('bot_email', '')
            api_key = settings.get('bot_api_key', '')
            
            if not all([zulip_url, bot_email, api_key]):
                return
            
            url = f"{zulip_url}/api/v1/messages"
            
            if message_type == 'private':
                # Send private message
                data = {
                    'type': 'private',
                    'to': sender_email,
                    'content': content
                }
            else:
                # Send to stream
                data = {
                    'type': 'stream',
                    'to': stream_name,
                    'subject': subject,
                    'content': content
                }
            
            response = requests.post(
                url,
                data=data,
                auth=(bot_email, api_key),
                timeout=30
            )
            
            if not response.ok:
                print(f"Failed to send Zulip message: {response.status_code} {response.text}")
                
        except Exception as e:
            print(f"Error sending Zulip message: {e}")
            traceback.print_exc() 