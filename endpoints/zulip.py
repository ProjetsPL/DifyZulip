import json
import logging
import traceback
from typing import Mapping, Any, Optional
from werkzeug import Request, Response
from dify_plugin import Endpoint
import requests
import base64
import re

logger = logging.getLogger(__name__)

class ZulipEndpoint(Endpoint):
    """
    Endpoint obsługujący webhook'i od Zulipa i integrujący z aplikacjami Dify
    """
    
    def _execute(self, r: Request) -> Response:
        """
        Główna metoda wykonywana przy każdym wywołaniu webhook'a
        """
        try:
            # Pobierz konfigurację pluginu
            settings = self.session.plugin_config.settings
            
            # Sprawdź czy wszystkie wymagane ustawienia są obecne
            required_settings = ['zulip_site_url', 'bot_email', 'bot_api_key', 'app']
            for setting in required_settings:
                if not settings.get(setting):
                    logger.error(f"Brakuje wymaganego ustawienia: {setting}")
                    return Response(
                        json.dumps({"error": f"Brakuje konfiguracji: {setting}"}),
                        status=400,
                        content_type='application/json'
                    )
            
            # Parsuj dane z żądania Zulip
            data = r.get_json()
            if not data:
                logger.error("Brak danych JSON w żądaniu")
                return Response(
                    json.dumps({"error": "Brak danych JSON"}),
                    status=400,
                    content_type='application/json'
                )
            
            logger.info(f"Otrzymano webhook od Zulip: {data}")
            
            # Sprawdź typ wiadomości
            message_type = data.get('type')
            if message_type != 'message':
                logger.info(f"Ignoruję wiadomość typu: {message_type}")
                return Response(json.dumps({"status": "ignored"}), content_type='application/json')
            
            # Pobierz dane wiadomości
            message_data = data.get('data', {})
            if not message_data:
                logger.error("Brak danych wiadomości")
                return Response(
                    json.dumps({"error": "Brak danych wiadomości"}),
                    status=400,
                    content_type='application/json'
                )
            
            # Sprawdź czy to nie wiadomość od naszego bota (unikaj pętli)
            sender_email = message_data.get('sender_email', '')
            bot_email = settings.get('bot_email', '')
            if sender_email == bot_email:
                logger.info("Ignoruję wiadomość od własnego bota")
                return Response(json.dumps({"status": "ignored"}), content_type='application/json')
            
            # Sprawdź czy wiadomość jest z dozwolonego strumienia
            if not self._is_message_allowed(message_data, settings):
                logger.info("Wiadomość z niedozwolonego strumienia lub bez wzmianki")
                return Response(json.dumps({"status": "ignored"}), content_type='application/json')
            
            # Wyczyść treść wiadomości (usuń wzmianki bota)
            content = self._clean_message_content(message_data.get('content', ''), bot_email)
            
            if not content.strip():
                logger.info("Pusta wiadomość po oczyszczeniu")
                return Response(json.dumps({"status": "ignored"}), content_type='application/json')
            
            # Wywołaj aplikację Dify
            dify_response = self._call_dify_app(content, message_data, settings)
            
            if not dify_response:
                logger.error("Brak odpowiedzi z aplikacji Dify")
                return Response(
                    json.dumps({"error": "Brak odpowiedzi z Dify"}),
                    status=500,
                    content_type='application/json'
                )
            
            # Wyślij odpowiedź do Zulip
            success = self._send_zulip_message(dify_response, message_data, settings)
            
            if success:
                return Response(json.dumps({"status": "success"}), content_type='application/json')
            else:
                return Response(
                    json.dumps({"error": "Błąd wysyłania wiadomości do Zulip"}),
                    status=500,
                    content_type='application/json'
                )
                
        except Exception as e:
            logger.error(f"Błąd w endpoint Zulip: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                json.dumps({"error": "Wewnętrzny błąd serwera"}),
                status=500,
                content_type='application/json'
            )
    
    def _is_message_allowed(self, message_data: dict, settings: dict) -> bool:
        """
        Sprawdza czy wiadomość powinna być obsłużona przez bota
        """
        respond_to_mentions_only = settings.get('respond_to_mentions_only', True)
        allowed_streams = settings.get('allowed_streams', '')
        bot_email = settings.get('bot_email', '')
        
        # Sprawdź strumień
        if allowed_streams:
            stream_names = [s.strip() for s in allowed_streams.split(',') if s.strip()]
            current_stream = message_data.get('display_recipient', '')
            if stream_names and current_stream not in stream_names:
                return False
        
        # Sprawdź czy to wiadomość prywatna
        message_type = message_data.get('type', '')
        if message_type == 'private':
            return True
        
        # Dla wiadomości publicznych sprawdź wzmianki
        if respond_to_mentions_only:
            content = message_data.get('content', '')
            # Sprawdź czy bot jest wspomniany (format @**Bot Name**)
            mention_pattern = rf'@\*\*[^*]*{re.escape(bot_email.split("@")[0])}[^*]*\*\*'
            if not re.search(mention_pattern, content, re.IGNORECASE):
                return False
        
        return True
    
    def _clean_message_content(self, content: str, bot_email: str) -> str:
        """
        Czyści treść wiadomości usuwając wzmianki bota
        """
        if not content:
            return ""
        
        # Usuń wzmianki bota (format @**Bot Name**)
        bot_name = bot_email.split('@')[0] if '@' in bot_email else bot_email
        mention_pattern = rf'@\*\*[^*]*{re.escape(bot_name)}[^*]*\*\*'
        cleaned_content = re.sub(mention_pattern, '', content, flags=re.IGNORECASE)
        
        # Usuń nadmiarowe białe znaki
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
        
        return cleaned_content
    
    def _call_dify_app(self, message_content: str, message_data: dict, settings: dict) -> Optional[str]:
        """
        Wywołuje aplikację Dify i zwraca odpowiedź
        """
        try:
            app_config = settings.get('app')
            if not app_config:
                logger.error("Brak konfiguracji aplikacji Dify")
                return None
            
            # Przygotuj dane kontekstu
            user_id = message_data.get('sender_email', 'unknown')
            conversation_id = f"zulip_{message_data.get('id', 'unknown')}"
            
            # Wywołaj aplikację Dify przez plugin API
            response = self.session.app.invoke(
                app_id=app_config,
                inputs={
                    'query': message_content,
                    'context': {
                        'platform': 'zulip',
                        'sender': message_data.get('sender_full_name', 'Unknown'),
                        'sender_email': message_data.get('sender_email', ''),
                        'stream': message_data.get('display_recipient', ''),
                        'subject': message_data.get('subject', ''),
                        'timestamp': message_data.get('timestamp', '')
                    }
                },
                user_id=user_id,
                conversation_id=conversation_id
            )
            
            if response and hasattr(response, 'text'):
                return response.text
            elif isinstance(response, dict) and 'answer' in response:
                return response['answer']
            elif isinstance(response, dict) and 'text' in response:
                return response['text']
            else:
                logger.warning(f"Nieoczekiwany format odpowiedzi z Dify: {response}")
                return str(response) if response else None
                
        except Exception as e:
            logger.error(f"Błąd wywołania aplikacji Dify: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def _send_zulip_message(self, response_text: str, original_message: dict, settings: dict) -> bool:
        """
        Wysyła odpowiedź do Zulip
        """
        try:
            zulip_site_url = settings.get('zulip_site_url', '').rstrip('/')
            bot_email = settings.get('bot_email', '')
            bot_api_key = settings.get('bot_api_key', '')
            
            # Przygotuj dane do wysłania
            message_type = original_message.get('type', 'stream')
            
            if message_type == 'private':
                # Wiadomość prywatna - odpowiedz prywatnie
                data = {
                    'type': 'private',
                    'to': json.dumps([original_message.get('sender_email')]),
                    'content': response_text
                }
            else:
                # Wiadomość publiczna - odpowiedz w tym samym strumieniu i temacie
                data = {
                    'type': 'stream',
                    'to': original_message.get('display_recipient', ''),
                    'subject': original_message.get('subject', 'Dify Bot'),
                    'content': response_text
                }
            
            # Przygotuj autoryzację
            auth_string = f"{bot_email}:{bot_api_key}"
            auth_encoded = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {auth_encoded}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Wyślij wiadomość
            url = f"{zulip_site_url}/api/v1/messages"
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info("Wiadomość wysłana pomyślnie do Zulip")
                return True
            else:
                logger.error(f"Błąd wysyłania wiadomości do Zulip: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Błąd wysyłania wiadomości do Zulip: {str(e)}")
            logger.error(traceback.format_exc())
            return False 