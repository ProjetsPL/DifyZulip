from collections.abc import Generator
from typing import Any
import zulip

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class SendMessageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Wysyła wiadomości do Zulip - do strumieni lub jako wiadomości bezpośrednie
        """
        try:
            # Pobierz credentials z konfiguracji provider
            credentials = self.runtime.credentials
            server_url = credentials.get('zulip_server_url').rstrip('/')
            email = credentials.get('zulip_email')
            api_key = credentials.get('zulip_api_key')
            
            # Pobierz parametry
            message_type = tool_parameters.get('message_type')
            content = tool_parameters.get('content')
            
            if not content:
                yield self.create_text_message("Błąd: Treść wiadomości jest wymagana")
                return
                
            # Utworzenie klienta Zulip
            client = zulip.Client(
                email=email,
                api_key=api_key,
                site=server_url
            )
            
            # Wysyłanie w zależności od typu wiadomości
            if message_type == 'stream':
                result = self._send_stream_message(client, tool_parameters)
            elif message_type == 'private':
                result = self._send_private_message(client, tool_parameters)
            else:
                yield self.create_text_message("Błąd: Nieprawidłowy typ wiadomości. Użyj 'stream' lub 'private'")
                return
                
            if result['result'] == 'success':
                yield self.create_json_message({
                    "status": "success",
                    "message": "Wiadomość została wysłana pomyślnie",
                    "message_id": result.get('id'),
                    "message_type": message_type
                })
            else:
                yield self.create_text_message(f"Błąd wysyłania wiadomości: {result.get('msg', 'Nieznany błąd')}")
                
        except Exception as e:
            yield self.create_text_message(f"Błąd: {str(e)}")
            
    def _send_stream_message(self, client: zulip.Client, parameters: dict[str, Any]) -> dict:
        """Wysyła wiadomość do strumienia"""
        stream_name = parameters.get('stream_name')
        topic = parameters.get('topic')
        content = parameters.get('content')
        
        if not stream_name:
            raise ValueError("Nazwa strumienia jest wymagana dla wiadomości do strumienia")
            
        if not topic:
            raise ValueError("Temat jest wymagany dla wiadomości do strumienia")
            
        return client.send_message({
            "type": "stream",
            "to": stream_name,
            "topic": topic,
            "content": content
        })
        
    def _send_private_message(self, client: zulip.Client, parameters: dict[str, Any]) -> dict:
        """Wysyła wiadomość bezpośrednią"""
        recipients = parameters.get('recipients')
        content = parameters.get('content')
        
        if not recipients:
            raise ValueError("Lista odbiorców jest wymagana dla wiadomości bezpośredniej")
            
        # Przetwarzanie listy odbiorców
        recipient_list = [email.strip() for email in recipients.split(',')]
        
        return client.send_message({
            "type": "private",
            "to": recipient_list,
            "content": content
        }) 