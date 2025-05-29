from collections.abc import Generator
from typing import Any
from datetime import datetime, timedelta
import zulip

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GetMessagesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Pobiera wiadomości z Zulip z możliwością filtrowania
        """
        try:
            # Pobierz credentials z konfiguracji provider
            credentials = self.runtime.credentials
            server_url = credentials.get('zulip_server_url').rstrip('/')
            email = credentials.get('zulip_email')
            api_key = credentials.get('zulip_api_key')
            
            # Pobierz parametry
            message_type = tool_parameters.get('message_type', 'all')
            stream_name = tool_parameters.get('stream_name')
            topic = tool_parameters.get('topic')
            limit = min(int(tool_parameters.get('limit', 20)), 100)  # Maksymalnie 100
            hours_ago = tool_parameters.get('hours_ago', 24)
            
            # Utworzenie klienta Zulip
            client = zulip.Client(
                email=email,
                api_key=api_key,
                site=server_url
            )
            
            # Oblicz timestamp dla filtrowania czasu
            since_timestamp = datetime.now() - timedelta(hours=float(hours_ago))
            
            # Przygotuj parametry zapytania
            request_params = {
                "num_after": limit,
                "anchor": "newest"
            }
            
            # Filtrowanie według typu wiadomości i strumienia
            if message_type == 'stream' or stream_name:
                if stream_name:
                    # Pobierz ID strumienia
                    streams_result = client.get_streams()
                    if streams_result['result'] != 'success':
                        yield self.create_text_message(f"Błąd pobierania listy strumieni: {streams_result.get('msg')}")
                        return
                        
                    stream_id = None
                    for stream in streams_result['streams']:
                        if stream['name'].lower() == stream_name.lower():
                            stream_id = stream['stream_id']
                            break
                            
                    if stream_id is None:
                        yield self.create_text_message(f"Nie znaleziono strumienia o nazwie: {stream_name}")
                        return
                    
                    # Konfiguracja dla konkretnego strumienia
                    narrow = [["stream", stream_name]]
                    if topic:
                        narrow.append(["topic", topic])
                    
                    request_params["narrow"] = narrow
                else:
                    # Wszystkie wiadomości ze strumieni
                    request_params["narrow"] = [["is", "stream"]]
                    
            elif message_type == 'private':
                request_params["narrow"] = [["is", "private"]]
            
            # Pobierz wiadomości
            result = client.get_messages(request_params)
            
            if result['result'] != 'success':
                yield self.create_text_message(f"Błąd pobierania wiadomości: {result.get('msg', 'Nieznany błąd')}")
                return
            
            messages = result['messages']
            
            # Filtruj według czasu
            filtered_messages = []
            for msg in messages:
                msg_timestamp = datetime.fromtimestamp(msg['timestamp'])
                if msg_timestamp >= since_timestamp:
                    filtered_messages.append(msg)
            
            # Przetwórz wiadomości do czytelnego formatu
            processed_messages = []
            for msg in filtered_messages:
                processed_msg = {
                    "id": msg['id'],
                    "content": msg['content'],
                    "sender_full_name": msg['sender_full_name'],
                    "sender_email": msg['sender_email'],
                    "timestamp": datetime.fromtimestamp(msg['timestamp']).isoformat(),
                    "type": msg['type']
                }
                
                if msg['type'] == 'stream':
                    processed_msg.update({
                        "stream_name": msg['display_recipient'],
                        "topic": msg['subject']
                    })
                else:
                    # Wiadomość prywatna
                    recipients = []
                    for recipient in msg['display_recipient']:
                        if recipient['email'] != email:  # Pomijamy siebie
                            recipients.append({
                                "full_name": recipient['full_name'],
                                "email": recipient['email']
                            })
                    processed_msg["recipients"] = recipients
                
                processed_messages.append(processed_msg)
            
            # Zwróć wyniki
            summary = {
                "total_messages": len(processed_messages),
                "message_type_filter": message_type,
                "time_range_hours": hours_ago,
                "stream_filter": stream_name if stream_name else "all",
                "topic_filter": topic if topic else "all"
            }
            
            if stream_name:
                summary["stream_filter"] = stream_name
            if topic:
                summary["topic_filter"] = topic
            
            yield self.create_json_message({
                "summary": summary,
                "messages": processed_messages
            })
            
        except Exception as e:
            yield self.create_text_message(f"Błąd: {str(e)}") 