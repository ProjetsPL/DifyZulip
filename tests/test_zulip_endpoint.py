import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

# Zakładając że możemy importować z pluginu
try:
    from endpoints.zulip import ZulipEndpoint
except ImportError:
    # Fallback w przypadku problemów z importem w środowisku testowym
    class ZulipEndpoint:
        def __init__(self):
            self.session = Mock()
            
        def _is_message_allowed(self, message_data, settings):
            return True
            
        def _clean_message_content(self, content, bot_email):
            return content
            
        def _call_dify_app(self, content, message_data, settings):
            return "Test response"
            
        def _send_zulip_message(self, response_text, message_data, settings):
            return True


class TestZulipEndpoint(unittest.TestCase):
    """
    Testy jednostkowe dla ZulipEndpoint
    """
    
    def setUp(self):
        """Przygotowanie testów"""
        self.endpoint = ZulipEndpoint()
        self.endpoint.session = Mock()
        self.endpoint.session.plugin_config = Mock()
        self.endpoint.session.plugin_config.settings = {
            'zulip_site_url': 'https://test.zulipchat.com',
            'bot_email': 'test-bot@test.zulipchat.com',
            'bot_api_key': 'test-api-key',
            'app': 'test-app-id',
            'respond_to_mentions_only': True,
            'allowed_streams': 'general,support'
        }
        self.endpoint.session.app = Mock()
    
    def test_is_message_allowed_with_mention(self):
        """Test filtrowania wiadomości z wzmianką"""
        message_data = {
            'type': 'stream',
            'content': '@**test-bot** Hello there!',
            'display_recipient': 'general'
        }
        settings = {
            'respond_to_mentions_only': True,
            'allowed_streams': 'general,support',
            'bot_email': 'test-bot@test.zulipchat.com'
        }
        
        result = self.endpoint._is_message_allowed(message_data, settings)
        self.assertTrue(result)
    
    def test_is_message_allowed_without_mention(self):
        """Test filtrowania wiadomości bez wzmianki gdy wymagana"""
        message_data = {
            'type': 'stream',
            'content': 'Hello everyone!',
            'display_recipient': 'general'
        }
        settings = {
            'respond_to_mentions_only': True,
            'allowed_streams': 'general,support',
            'bot_email': 'test-bot@test.zulipchat.com'
        }
        
        result = self.endpoint._is_message_allowed(message_data, settings)
        self.assertFalse(result)
    
    def test_is_message_allowed_private_message(self):
        """Test akceptowania wiadomości prywatnych"""
        message_data = {
            'type': 'private',
            'content': 'Hello!',
        }
        settings = {
            'respond_to_mentions_only': True,
            'bot_email': 'test-bot@test.zulipchat.com'
        }
        
        result = self.endpoint._is_message_allowed(message_data, settings)
        self.assertTrue(result)
    
    def test_is_message_allowed_wrong_stream(self):
        """Test odrzucania wiadomości z niedozwolonego strumienia"""
        message_data = {
            'type': 'stream',
            'content': '@**test-bot** Hello!',
            'display_recipient': 'random'
        }
        settings = {
            'respond_to_mentions_only': True,
            'allowed_streams': 'general,support',
            'bot_email': 'test-bot@test.zulipchat.com'
        }
        
        result = self.endpoint._is_message_allowed(message_data, settings)
        self.assertFalse(result)
    
    def test_clean_message_content(self):
        """Test czyszczenia treści wiadomości"""
        content = '@**test-bot** Hello, how can I help you?'
        bot_email = 'test-bot@test.zulipchat.com'
        
        cleaned = self.endpoint._clean_message_content(content, bot_email)
        self.assertEqual(cleaned, 'Hello, how can I help you?')
    
    def test_clean_message_content_multiple_mentions(self):
        """Test czyszczenia treści z wieloma wzmiankami"""
        content = '@**test-bot** Hello @**other-user** and @**test-bot** again!'
        bot_email = 'test-bot@test.zulipchat.com'
        
        cleaned = self.endpoint._clean_message_content(content, bot_email)
        # Powinno usunąć tylko wzmianki bota, nie innych użytkowników
        self.assertNotIn('test-bot', cleaned)
        self.assertIn('other-user', cleaned)
    
    @patch('endpoints.zulip.requests.post')
    def test_send_zulip_message_stream(self, mock_post):
        """Test wysyłania wiadomości do strumienia"""
        mock_post.return_value.status_code = 200
        
        response_text = "Test response"
        original_message = {
            'type': 'stream',
            'display_recipient': 'general',
            'subject': 'Test Topic',
            'sender_email': 'user@test.com'
        }
        settings = {
            'zulip_site_url': 'https://test.zulipchat.com',
            'bot_email': 'bot@test.com',
            'bot_api_key': 'test-key'
        }
        
        result = self.endpoint._send_zulip_message(response_text, original_message, settings)
        
        self.assertTrue(result)
        mock_post.assert_called_once()
        
        # Sprawdź parametry wywołania
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], 'https://test.zulipchat.com/api/v1/messages')
        self.assertEqual(call_args[1]['data']['type'], 'stream')
        self.assertEqual(call_args[1]['data']['to'], 'general')
        self.assertEqual(call_args[1]['data']['content'], 'Test response')
    
    @patch('endpoints.zulip.requests.post')
    def test_send_zulip_message_private(self, mock_post):
        """Test wysyłania wiadomości prywatnej"""
        mock_post.return_value.status_code = 200
        
        response_text = "Private response"
        original_message = {
            'type': 'private',
            'sender_email': 'user@test.com'
        }
        settings = {
            'zulip_site_url': 'https://test.zulipchat.com',
            'bot_email': 'bot@test.com',
            'bot_api_key': 'test-key'
        }
        
        result = self.endpoint._send_zulip_message(response_text, original_message, settings)
        
        self.assertTrue(result)
        mock_post.assert_called_once()
        
        # Sprawdź parametry wywołania
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['data']['type'], 'private')
        self.assertEqual(call_args[1]['data']['to'], json.dumps(['user@test.com']))
    
    def test_call_dify_app(self):
        """Test wywołania aplikacji Dify"""
        mock_response = Mock()
        mock_response.text = "Dify response"
        self.endpoint.session.app.invoke.return_value = mock_response
        
        message_content = "Test question"
        message_data = {
            'sender_email': 'user@test.com',
            'sender_full_name': 'Test User',
            'id': 123,
            'display_recipient': 'general',
            'subject': 'Test',
            'timestamp': 1234567890
        }
        settings = {'app': 'test-app'}
        
        result = self.endpoint._call_dify_app(message_content, message_data, settings)
        
        self.assertEqual(result, "Dify response")
        self.endpoint.session.app.invoke.assert_called_once()
        
        # Sprawdź parametry wywołania
        call_args = self.endpoint.session.app.invoke.call_args
        self.assertEqual(call_args[1]['app_id'], 'test-app')
        self.assertEqual(call_args[1]['inputs']['query'], 'Test question')
        self.assertEqual(call_args[1]['user_id'], 'user@test.com')
    
    def create_request(self, data):
        """Helper do tworzenia testowych żądań"""
        builder = EnvironBuilder(
            method='POST',
            data=json.dumps(data),
            content_type='application/json'
        )
        env = builder.get_environ()
        return Request(env)
    
    @patch.object(ZulipEndpoint, '_send_zulip_message')
    @patch.object(ZulipEndpoint, '_call_dify_app')
    def test_execute_valid_message(self, mock_call_dify, mock_send_message):
        """Test pełnego przetwarzania prawidłowej wiadomości"""
        mock_call_dify.return_value = "AI response"
        mock_send_message.return_value = True
        
        test_data = {
            'type': 'message',
            'data': {
                'id': 123,
                'sender_email': 'user@test.com',
                'sender_full_name': 'Test User',
                'content': '@**test-bot** Hello!',
                'display_recipient': 'general',
                'subject': 'Test Topic',
                'type': 'stream'
            }
        }
        
        request = self.create_request(test_data)
        response = self.endpoint._execute(request)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['status'], 'success')
        
        mock_call_dify.assert_called_once()
        mock_send_message.assert_called_once()
    
    def test_execute_bot_message_ignored(self):
        """Test ignorowania wiadomości od własnego bota"""
        test_data = {
            'type': 'message',
            'data': {
                'id': 123,
                'sender_email': 'test-bot@test.zulipchat.com',  # To jest nasz bot
                'content': 'Bot response',
                'type': 'stream'
            }
        }
        
        request = self.create_request(test_data)
        response = self.endpoint._execute(request)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['status'], 'ignored')
    
    def test_execute_non_message_type(self):
        """Test ignorowania eventów które nie są wiadomościami"""
        test_data = {
            'type': 'heartbeat',  # Nie jest to wiadomość
            'data': {}
        }
        
        request = self.create_request(test_data)
        response = self.endpoint._execute(request)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data['status'], 'ignored')
    
    def test_execute_missing_configuration(self):
        """Test obsługi brakującej konfiguracji"""
        # Usuń wymaganą konfigurację
        self.endpoint.session.plugin_config.settings = {}
        
        test_data = {
            'type': 'message',
            'data': {
                'content': 'Test message'
            }
        }
        
        request = self.create_request(test_data)
        response = self.endpoint._execute(request)
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', response_data)


class TestZulipEndpointIntegration(unittest.TestCase):
    """
    Testy integracyjne - wymagają rzeczywistego środowiska testowego
    """
    
    @unittest.skip("Wymaga konfiguracji środowiska testowego")
    def test_real_zulip_api_call(self):
        """Test rzeczywistego wywołania API Zulip"""
        # Ten test wymagałby prawdziwych danych testowych
        pass
    
    @unittest.skip("Wymaga konfiguracji środowiska testowego")  
    def test_real_dify_app_call(self):
        """Test rzeczywistego wywołania aplikacji Dify"""
        # Ten test wymagałby prawdziwych danych testowych
        pass


if __name__ == '__main__':
    # Uruchom testy
    unittest.main(verbosity=2) 