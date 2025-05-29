from typing import Any
import zulip

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class ZulipProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Waliduje credentials Zulip poprzez test połączenia z serwerem
        """
        try:
            server_url = credentials.get('zulip_server_url')
            email = credentials.get('zulip_email') 
            api_key = credentials.get('zulip_api_key')
            
            if not all([server_url, email, api_key]):
                raise ToolProviderCredentialValidationError("Wszystkie pola (URL serwera, email, klucz API) są wymagane")
            
            # Usuń slash na końcu URL jeśli istnieje
            server_url = server_url.rstrip('/')
            
            # Utworzenie klienta Zulip
            client = zulip.Client(
                email=email,
                api_key=api_key,
                site=server_url
            )
            
            # Test połączenia - pobieranie informacji o użytkowniku
            result = client.get_profile()
            
            if result['result'] != 'success':
                raise ToolProviderCredentialValidationError(f"Nie udało się połączyć z Zulip: {result.get('msg', 'Nieznany błąd')}")
                
        except Exception as e:
            if isinstance(e, ToolProviderCredentialValidationError):
                raise e
            raise ToolProviderCredentialValidationError(f"Błąd walidacji credentials Zulip: {str(e)}")
