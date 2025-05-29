# Zulip Plugin dla Dify

**Autor:** bartlomiejmatlega  
**Wersja:** 0.0.1  
**Typ:** tool  

## Opis

Wtyczka Zulip dla Dify umożliwia integrację z platformą czatu Zulip. Pozwala na wysyłanie i odbieranie wiadomości z Zulip bezpośrednio z Chatflow/Chatbot/Agent w Dify.

## Funkcjonalności

### 📤 Wysyłanie Wiadomości (`send_message`)
- Wysyłanie wiadomości do strumieni (kanałów) Zulip
- Wysyłanie wiadomości bezpośrednich do użytkowników
- Obsługa tematów w wiadomościach do strumieni
- Obsługa wielu odbiorców w wiadomościach prywatnych

### 📥 Odbieranie Wiadomości (`get_messages`)
- Pobieranie wiadomości ze strumieni lub rozmów prywatnych
- Filtrowanie według typu wiadomości (strumień/prywatne/wszystkie)
- Filtrowanie według konkretnego strumienia i tematu
- Ograniczenie liczby wiadomości (1-100)
- Filtrowanie według czasu (ostatnie N godzin)

## Wymagania

- Python 3.8+
- Konto Zulip z dostępem do API
- Klucz API Zulip

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone [url-repozytorium]
cd dify-zulip
```

2. Utwórz środowisko wirtualne:
```bash
python3 -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

## Konfiguracja

### Uzyskanie Klucza API Zulip

1. Zaloguj się do swojego serwera Zulip
2. Przejdź do **Settings** → **Account & privacy** 
3. W sekcji **API key** kliknij **Generate new API key**
4. Skopiuj wygenerowany klucz

### Parametry Uwierzytelniania

W Dify skonfiguruj następujące parametry:

- **Zulip Server URL**: URL twojego serwera Zulip (np. `https://your-organization.zulipchat.com`)
- **Email**: Twój adres email użyty w Zulip
- **API Key**: Klucz API wygenerowany w Zulip

## Użytkowanie

### Wysyłanie Wiadomości do Strumienia

```
Typ wiadomości: stream
Nazwa strumienia: general
Temat: API Test
Treść: Cześć! To jest wiadomość testowa z Dify.
```

### Wysyłanie Wiadomości Prywatnej

```
Typ wiadomości: private
Odbiorcy: user1@example.com,user2@example.com
Treść: Prywatna wiadomość od bota.
```

### Pobieranie Wiadomości

```
Typ wiadomości: stream
Nazwa strumienia: general
Temat: API Test (opcjonalnie)
Limit: 10
Godzin wstecz: 24
```

## Bezpieczeństwo

- Klucz API jest bezpiecznie przechowywany w Dify jako secret
- Wszystkie połączenia używają HTTPS
- Walidacja credentials odbywa się przy każdej konfiguracji

## Wsparcie

W przypadku problemów sprawdź:
1. Czy URL serwera Zulip jest prawidłowy
2. Czy klucz API jest aktualny
3. Czy masz odpowiednie uprawnienia w Zulip

## Licencja

Ten projekt jest udostępniony na licencji open source.



