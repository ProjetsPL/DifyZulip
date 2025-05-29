# Zulip Bot dla Dify

**Autor:** bartlomiejmatlega  
**Wersja:** 0.0.1  
**Typ:** extension

## Opis

Zulip Bot umożliwia integrację z platformą czatu Zulip jako bot, który:
- Odbiera wiadomości z Zulip jako wejście do Chatflow/Chatbot/Agent w Dify
- Wysyła odpowiedzi z powrotem do Zulip
- Obsługuje wiadomości prywatne i wzmianki w kanałach

**Architektura**: Plugin używa dwóch botów w Zulip:
1. **Generic bot** - do wysyłania odpowiedzi z Dify do Zulip (API)
2. **Outgoing webhook bot** - do odbierania wiadomości z Zulip przez Dify (webhook)

## Instrukcja Konfiguracji

### 1. Utworzenie Bota w Zulip

1. **Zaloguj się do swojego serwera Zulip**
   - Przejdź do **Settings** → **Personal settings** → **Bots**
   - Kliknij **Add a new bot**

2. **Utwórz zwykłego bota (do API)**
   - Wybierz **Generic bot** jako typ bota
   - Wprowadź nazwę bota (np. "Dify Assistant API")
   - Opcjonalnie dodaj avatar i opis
   - Kliknij **Create bot**

3. **Pobierz dane uwierzytelniania**
   - Skopiuj **Email address** bota (np. `dify-bot@your-org.zulipchat.com`)
   - Skopiuj **API key** bota
   - Zanotuj **Server URL** (np. `https://your-org.zulipchat.com`)

### 2. Konfiguracja Endpoint w Dify

1. **Utwórz nowy endpoint**
   - W Dify przejdź do sekcji Plugins
   - Zainstaluj plugin Zulip Bot
   - Utwórz nowy endpoint z niestandardową nazwą

2. **Wprowadź dane konfiguracyjne**
   - **Zulip Server URL**: URL twojego serwera Zulip
   - **Bot Email**: Adres email bota z kroku 1
   - **Bot API Key**: Klucz API bota z kroku 1
   - **Allow Retry**: Ustaw na false (zalecane)
   - **App**: Wybierz aplikację Dify do obsługi wiadomości

3. **Zapisz i skopiuj URL endpoint**
   - Zapisz konfigurację
   - Skopiuj wygenerowany URL endpoint

### 3. Konfiguracja Outgoing Webhook w Zulip

**Uwaga**: Lokalizacja opcji może się różnić w zależności od wersji Zulip i języka interfejsu. W polskiej wersji może być **Ustawienia** → **Organizacja** → **Boty**.

#### Metoda A: Konfiguracja outgoing webhook (zalecana)

**Uwaga**: Teraz utworzymy drugi bot - tym razem **Outgoing webhook bot** (inny niż Generic bot z kroku 1). Ten bot będzie **wysyłać** wiadomości **z** Zulip **do** naszego endpoint.

1. **Utwórz outgoing webhook bot**
   - W Zulip przejdź do **Settings** → **Organization** → **Bots**
   - Przewiń do sekcji **Add a new bot**
   - Wybierz **Outgoing webhook** jako typ bota (nie Generic!)

2. **Skonfiguruj outgoing webhook bot**
   - **Bot name**: Nazwa bota (np. "Dify Assistant Webhook")
   - **Endpoint URL**: Wklej URL endpoint z Dify
   - **Interface**: Wybierz **Generic** (format danych Zulip)
   - **Triggers**: Wybierz kiedy webhook ma się uruchamiać:
     - `@mention` - gdy ktoś wspomni bota
     - `direct_message` - dla wiadomości prywatnych do bota
   - Kliknij **Create bot**

#### Metoda B: Użycie integracji JSON webhook (alternatywna)

1. **Znajdź integrację JSON**
   - W Zulip przejdź do **Settings** → **Organization** → **Integrations**
   - Znajdź **JSON** w sekcji webhooks lub wyszukaj "JSON"
   - Kliknij **Configure**

2. **Skonfiguruj JSON webhook**
   - **URL**: Wklej URL endpoint z Dify
   - **Stream**: Wybierz strumień do monitorowania (opcjonalne)
   - **Bot name**: Nazwa wyświetlana dla wiadomości (opcjonalne)

### 4. Testowanie

1. **Dodaj outgoing webhook bota do strumienia/kanału**
   - Przejdź do wybranego strumienia w Zulip
   - Kliknij ikonę koła zębatego → **Add members**
   - Dodaj utworzonego **outgoing webhook bota** (nie generic bota!)

2. **Testuj interakcję**
   - **Wzmianka w strumieniu**: Napisz `@nazwa_webhook_bota Cześć!`
   - **Wiadomość prywatna**: Wyślij bezpośrednią wiadomość do **outgoing webhook bota**
   - Bot powinien odpowiedzieć używając aplikacji Dify

## Obsługiwane Funkcje

### 📥 Odbieranie Wiadomości
- Wiadomości prywatne do bota
- Wzmianki bota w kanałach publicznych (`@bot_name`)
- Automatyczne czyszczenie wzmianek z treści wiadomości
- Obsługa formatowania Markdown z Zulip

### 📤 Wysyłanie Odpowiedzi
- Odpowiedzi na wiadomości prywatne (jako wiadomość prywatna)
- Odpowiedzi w strumieniach (w tym samym temacie)
- Obsługa błędów z graceful fallback
- Użycie formatowania Zulip (emoji, Markdown)

### 🔄 Integracja z Dify
- Przekazywanie wiadomości do wybranej aplikacji Dify
- Obsługa trybu blocking dla natychmiastowych odpowiedzi
- Konfigurowalne retry policy dla webhook

## Bezpieczeństwo

- API key bota przechowywany jako encrypted secret w Dify
- Wszystkie połączenia przez HTTPS
- Walidacja wiadomości i nadawców
- Ochrona przed pętlami (bot nie odpowiada sam sobie)
- Webhook endpoint chroni przed duplikowaniem wiadomości

## Rozwiązywanie Problemów

### Problemy z konfiguracją bota

1. **Bot nie odpowiada na wzmianki**
   - Sprawdź czy bot został dodany do strumienia
   - Sprawdź trigger konfigurację w outgoing webhook
   - Upewnij się że używasz `@nazwa_bota` (bez @-organization)

2. **Bot nie odpowiada na wiadomości prywatne**
   - Sprawdź czy outgoing webhook ma włączony trigger `private_message`
   - Sprawdź czy bot ma odpowiednie uprawnienia

### Problemy z webhook

1. **Webhook nie dostarcza danych**
   - Sprawdź czy URL endpoint jest dostępny z internetu
   - Sprawdź logi webhook w **Organization settings** → **Bots** → **Active bots**
   - Użyj narzędzi jak webhook.site do debugowania

2. **Błędy formatowania danych**
   - Sprawdź czy endpoint obsługuje `application/x-www-form-urlencoded`
   - W ustawieniach bota sprawdź Interface (Generic vs Slack compatible)

### Problemy z aplikacją Dify

1. **Brak odpowiedzi od aplikacji**
   - Sprawdź czy wybrana aplikacja jest aktywna
   - Sprawdź czy aplikacja może przetwarzać zapytania tekstowe
   - Sprawdź logi w Dify

## Wymagania

- **Zulip**: Serwer Zulip z uprawnieniami administratora organizacji
- **Bot**: Możliwość tworzenia botów w organizacji
- **Webhook**: Dostęp do konfiguracji outgoing webhooks
- **Dify**: Instancja Dify z dostępem do internetu
- **Aplikacja**: Aktywna aplikacja Dify (Chatflow/Chatbot/Agent)

## Ograniczenia

- Bot odpowiada tylko na bezpośrednie wzmianki i wiadomości prywatne
- Wymaga konfiguracji outgoing webhook w Zulip
- Endpoint musi być dostępny publicznie z internetu
- Obsługuje tylko wiadomości tekstowe (brak wsparcia dla załączników)

## Licencja

Ten projekt jest udostępniony na licencji open source.



