# Plugin Dify-Zulip Integration

Plugin umożliwiający integrację aplikacji Dify z Zulipem, pozwalając na dwukierunkową komunikację między chatbotami/agentami AI w Dify a użytkownikami w Zulipie.

## Funkcjonalności

- **Odbieranie wiadomości z Zulipa**: Bot automatycznie reaguje na wiadomości w skonfigurowanych strumieniach
- **Inteligentne filtrowanie**: Możliwość konfiguracji, aby bot reagował tylko na wzmianki lub na wszystkie wiadomości
- **Obsługa wiadomości prywatnych**: Bot może odpowiadać na wiadomości prywatne
- **Konfigurowalny dostęp**: Możliwość ograniczenia działania bota do określonych strumieni
- **Kontekst konwersacji**: Przekazywanie metadanych wiadomości (nadawca, strumień, temat) do aplikacji Dify

## Wymagania

- Dify (self-hosted)
- Zulip (self-hosted lub cloud)
- Python 3.12+

## Instrukcja konfiguracji

### 1. Konfiguracja Zulipa

#### Krok 1: Tworzenie bota w Zulipie

1. **Zaloguj się do swojej instancji Zulip** jako administrator lub użytkownik z uprawnieniami do tworzenia botów

2. **Przejdź do ustawień organizacji**:
   - Kliknij na ikonę koła zębatego w prawym górnym rogu
   - Wybierz "Manage organization" lub "Ustawienia organizacji"

3. **Dodaj nowego bota**:
   - Przejdź do sekcji "Bots" w menu po lewej stronie
   - Kliknij "Add a new bot"

4. **Skonfiguruj bota**:
   - **Bot type**: Wybierz "Generic bot"
   - **Full name**: `Dify AI Assistant` (lub dowolną nazwę)
   - **Username**: `dify-bot` (będzie to część adresu email bota)
   - **Bot email**: `dify-bot@twoja-organizacja.zulipchat.com`
   - **Avatar**: Opcjonalnie, dodaj avatar dla bota

5. **Skopiuj dane uwierzytelniające**:
   - Po utworzeniu bota, skopiuj **API key** - będzie potrzebny w konfiguracji pluginu
   - Zanotuj pełny **email bota**

#### Krok 2: Konfiguracja uprawnień bota

1. **Ustawienia subskrypcji**:
   - W sekcji "Bots", znajdź swojego bota
   - Kliknij "Edit" obok bota
   - Dodaj bota do strumieni, w których ma działać:
     - Przejdź do sekcji "Streams"
     - Subskrybuj bota do odpowiednich strumieni (np. `general`, `support`, `ai-chat`)

2. **Uprawnienia bota**:
   - Upewnij się, że bot ma uprawnienia do:
     - Wysyłania wiadomości publicznych
     - Wysyłania wiadomości prywatnych
     - Odczytywania wiadomości ze strumieni

#### Krok 3: Konfiguracja webhook'ów (opcjonalnie dla zaawansowanych scenariuszy)

Dla standardowej konfiguracji ten krok nie jest wymagany, ponieważ plugin będzie działał jako outgoing webhook.

### 2. Konfiguracja pluginu w Dify

#### Krok 1: Instalacja pluginu

1. **Wgraj plugin do Dify**:
   - Spakuj folder pluginu do archiwum `.difypkg` (użyj załączonego skryptu `./package.sh`)
   - W interfejsie Dify przejdź do sekcji "Plugins" lub "Rozszerzenia"
   - Kliknij "Upload Plugin" i wgraj plik `.difypkg`
   - Aktywuj plugin po zainstalowaniu

#### Krok 2: Konfiguracja pluginu

1. **Przejdź do ustawień pluginu Zulip** w Dify

2. **Wypełnij wymagane pola**:

   **Zulip Site URL**:
   ```
   https://twoja-organizacja.zulipchat.com
   ```
   (lub URL Twojej self-hosted instancji Zulip)

   **Bot Email**:
   ```
   dify-bot@twoja-organizacja.zulipchat.com
   ```
   (email bota utworzonego w kroku 1)

   **Bot API Key**:
   ```
   [wklej tutaj API key skopiowany z Zulip]
   ```

   **Dify App**:
   - Wybierz aplikację Dify (Chatbot, Agent, lub Chatflow), która będzie obsługiwać wiadomości z Zulip

3. **Skonfiguruj opcjonalne ustawienia**:

   **Respond to Mentions Only** (domyślnie: `true`):
   - `true`: Bot będzie odpowiadać tylko na wzmianki (np. `@dify-bot jak mogę Ci pomóc?`)
   - `false`: Bot będzie odpowiadać na wszystkie wiadomości w dozwolonych strumieniach

   **Allowed Streams** (opcjonalne):
   ```
   general,support,ai-chat
   ```
   - Lista strumieni oddzielonych przecinkami, w których bot może działać
   - Pozostaw puste, aby bot działał we wszystkich strumieniach

#### Krok 3: Testowanie konfiguracji

1. **Otrzymanie URL webhook'a**:
   - Po skonfigurowaniu pluginu, Dify wygeneruje URL webhook'a
   - Przykład: `https://twoja-dify-instancja.com/v1/plugins/zulip/webhook`

2. **Test podstawowy**:
   - Wyślij wiadomość prywatną do bota w Zulipie
   - Bot powinien odpowiedzieć używając skonfigurowanej aplikacji Dify

3. **Test publiczny** (jeśli skonfigurowany):
   - W dozwolonym strumieniu wyślij wiadomość wzmiankując bota: `@dify-bot Cześć!`
   - Bot powinien odpowiedzieć w tym samym wątku

### 3. Konfiguracja zaawansowana

#### Webhook dla większej responsywności (opcjonalnie)

Dla lepszej wydajności możesz skonfigurować outgoing webhook w Zulipie:

1. **W Zulipie przejdź do ustawień organizacji**
2. **Sekcja "Integrations"**
3. **Dodaj "Outgoing webhook"**:
   - **Service name**: `Dify Integration`
   - **Service base URL**: `https://twoja-dify-instancja.com/v1/plugins/zulip`
   - **Interface**: `Generic webhook`
   - **Bot user**: Wybierz utworzonego bota

#### Monitorowanie i logi

- Logi pluginu są dostępne w sekcji logów Dify
- Możesz monitorować:
  - Otrzymane wiadomości z Zulip
  - Odpowiedzi aplikacji Dify
  - Błędy wysyłania wiadomości do Zulip

## Rozwiązywanie problemów

### Bot nie odpowiada

1. **Sprawdź logi** w Dify - poszukaj błędów w sekcji logów pluginu
2. **Sprawdź uprawnienia bota** w Zulipie - czy bot jest subskrybowany do właściwych strumieni
3. **Sprawdź API key** - czy jest poprawny i nie wygasł
4. **Sprawdź URL Zulip** - czy jest poprawny i dostępny

### Bot odpowiada na wszystkie wiadomości

1. **Sprawdź ustawienie "Respond to Mentions Only"** - powinno być `true`
2. **Sprawdź listę dozwolonych strumieni** - możliwe, że jest zbyt szeroka

### Błędy autoryzacji

1. **Sprawdź API key** - skopiuj ponownie z ustawień bota w Zulipie
2. **Sprawdź email bota** - musi być dokładnie taki sam jak w Zulipie
3. **Sprawdź uprawnienia bota** - czy może wysyłać wiadomości

### Problemy z formatowaniem wiadomości

- Zulip używa własnego formatu Markdown
- Aplikacja Dify może zwracać tekst w różnych formatach
- Plugin automatycznie przekazuje odpowiedzi bez modyfikacji formatowania

## Przykłady użycia

### Podstawowe pytanie

**Użytkownik w Zulipie**:
```
@dify-bot Jaka jest pogoda dzisiaj?
```

**Bot odpowie** używając skonfigurowanej aplikacji Dify.

### Wiadomość prywatna

**Użytkownik wysyła prywatną wiadomość**:
```
Potrzebuję pomocy z konfiguracją serwera
```

**Bot odpowie** prywatnie używając aplikacji Dify.

### W określonym strumieniu

Jeśli bot jest skonfigurowany dla strumienia `support`:
```
#support
@dify-bot Mam problem z logowaniem
```

Bot odpowie w wątku w strumieniu `support`.

## Licencja

Ten plugin jest dostępny na licencji MIT.

## Wsparcie

W przypadku problemów:
1. Sprawdź logi w Dify
2. Sprawdź dokumentację Zulip API
3. Upewnij się, że wszystkie URLs i klucze API są poprawne 