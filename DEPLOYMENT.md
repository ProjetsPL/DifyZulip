# Instrukcje wdrożenia Plugin Dify-Zulip

## Wymagania systemowe

- Dify self-hosted (wersja z obsługą pluginów)
- Zulip self-hosted lub cloud
- Python 3.12+
- Dostęp administratora do obu systemów

## Kroki wdrożenia

### 1. Przygotowanie pluginu

```bash
# Sklonuj lub pobierz kod pluginu
cd dify-zulip-plugin

# Sprawdź strukturę plików
ls -la
# Powinny być widoczne:
# - manifest.yaml
# - main.py
# - requirements.txt
# - group/zulip.yaml
# - endpoints/zulip.yaml
# - endpoints/zulip.py
# - icon.svg
# - README.md
```

### 2. Pakowanie pluginu

```bash
# Użyj dołączonego skryptu pakowania
./package.sh

# Alternatywnie ręcznie:
# zip -r dify-zulip-plugin.difypkg . -x "*.git*" "*.DS_Store" "__pycache__/*" "*.pyc"
```

### 3. Instalacja w Dify

1. **Zaloguj się do interfejsu administratora Dify**
2. **Przejdź do sekcji Plugins/Extensions**
3. **Kliknij "Upload Plugin" lub "Install Plugin"**
4. **Wybierz plik `dify-zulip-plugin-v0.0.1.difypkg`**
5. **Potwierdź instalację i poczekaj na zakończenie procesu**

### 4. Konfiguracja w Zulipie

#### Utwórz bota

```bash
# Opcjonalnie, użyj Zulip API do utworzenia bota
curl -X POST https://twoja-organizacja.zulipchat.com/api/v1/bots \
  -u "admin@twoja-organizacja.com:ADMIN_API_KEY" \
  -d "bot_type=1" \
  -d "full_name=Dify AI Assistant" \
  -d "short_name=dify-bot"
```

Lub użyj interfejsu webowego (preferowane):

1. Zaloguj się do Zulip jako administrator
2. Przejdź do Organization settings → Bots
3. Kliknij "Add a new bot"
4. Wypełnij formularz:
   - Bot type: Generic bot
   - Full name: `Dify AI Assistant`
   - Username: `dify-bot`
5. Skopiuj wygenerowany API key

### 5. Konfiguracja pluginu w Dify

1. **Aktywuj plugin** w sekcji Plugins
2. **Przejdź do konfiguracji pluginu Zulip**
3. **Wypełnij formularz**:

```yaml
Zulip Site URL: https://twoja-organizacja.zulipchat.com
Bot Email: dify-bot@twoja-organizacja.zulipchat.com
Bot API Key: [wklej API key z Zulip]
Dify App: [wybierz aplikację z listy]
Respond to Mentions Only: true
Allowed Streams: general,support,ai-help
```

### 6. Testowanie instalacji

#### Test webhook'a

```bash
# Test podstawowy endpoint
curl -X POST https://twoja-dify-instancja.com/v1/plugins/zulip/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "data": {
      "id": 123,
      "sender_email": "test@example.com",
      "sender_full_name": "Test User",
      "content": "@dify-bot Cześć!",
      "display_recipient": "general",
      "subject": "Test",
      "type": "stream"
    }
  }'
```

#### Test wiadomości w Zulipie

1. **Wyślij wiadomość prywatną do bota**:
   ```
   Cześć, potrzebuję pomocy
   ```

2. **Wyślij wiadomość publiczną z wzmianką**:
   ```
   @dify-bot Jaka jest pogoda?
   ```

### 7. Monitorowanie

#### Logi Dify

```bash
# Sprawdź logi Dify (lokalizacja może się różnić)
tail -f /var/log/dify/app.log | grep -i zulip
```

#### Logi Zulip

```bash
# Sprawdź logi Zulip
tail -f /var/log/zulip/server.log | grep -i bot
```

## Rozwiązywanie problemów wdrożenia

### Plugin nie ładuje się

1. **Sprawdź format archiwum .difypkg**:
   ```bash
   unzip -l dify-zulip-plugin-v0.0.1.difypkg
   ```

2. **Sprawdź strukturę plików**:
   - `manifest.yaml` musi być w głównym katalogu
   - Wszystkie wymagane pliki muszą być obecne

3. **Sprawdź logi Dify** podczas ładowania pluginu

### Błędy konfiguracji

1. **Sprawdź URL Zulip**:
   ```bash
   curl -I https://twoja-organizacja.zulipchat.com
   ```

2. **Sprawdź API key bota**:
   ```bash
   curl -H "Authorization: Basic $(echo -n 'bot-email:api-key' | base64)" \
        https://twoja-organizacja.zulipchat.com/api/v1/users/me
   ```

### Bot nie odpowiada

1. **Sprawdź subskrypcje bota** w Zulipie
2. **Sprawdź uprawnienia bota**
3. **Sprawdź konfigurację aplikacji Dify**

## Aktualizacja pluginu

### 1. Przygotuj nową wersję

```bash
# Zaktualizuj wersję w manifest.yaml
sed -i 's/version: 0.0.1/version: 0.0.2/' manifest.yaml

# Spakuj nową wersję
./package.sh
```

### 2. Wgraj aktualizację

1. W Dify przejdź do sekcji Plugins
2. Znajdź plugin Zulip
3. Kliknij "Update" lub "Disable" → "Install" nową wersję

### 3. Sprawdź konfigurację

- Większość ustawień powinna być zachowana
- Sprawdź czy nowe funkcje wymagają dodatkowej konfiguracji

## Backup i przywracanie

### Backup konfiguracji

```bash
# Eksportuj konfigurację pluginu z Dify (jeśli dostępne)
dify plugin export zulip > zulip-config-backup.json
```

### Przywracanie

```bash
# Przywróć konfigurację (jeśli dostępne)
dify plugin import zulip < zulip-config-backup.json
```

## Bezpieczeństwo

### Zabezpieczenie API keys

1. **Używaj dedykowanego bota** zamiast kont użytkowników
2. **Ograniczaj uprawnienia bota** do minimum
3. **Regularnie rotuj API keys**
4. **Monitoruj aktywność bota**

### Zabezpieczenie webhook'ów

1. **Używaj HTTPS** dla wszystkich połączeń
2. **Skonfiguruj firewall** aby ograniczyć dostęp do endpoint'ów
3. **Monitoruj ruch** webhook'ów

## Wydajność

### Optymalizacja

1. **Ograniczaj dozwolone strumienie** do niezbędnych
2. **Używaj "Respond to Mentions Only"** dla dużych organizacji
3. **Monitoruj obciążenie** aplikacji Dify

### Skalowanie

- Plugin może obsługiwać wiele instancji Zulip
- Każda instancja wymaga osobnej konfiguracji
- Rozważ load balancing dla dużych instalacji