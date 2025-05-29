# Testowanie Plugin Dify-Zulip

Ten dokument opisuje jak testować plugin Dify-Zulip przed i po wdrożeniu.

## Testy przed wdrożeniem

### 1. Testy jednostkowe

```bash
# Uruchom testy jednostkowe
cd tests/
python test_zulip_endpoint.py

# Alternatywnie z pytest (jeśli zainstalowany)
pip install pytest
pytest test_zulip_endpoint.py -v
```

### 2. Walidacja struktury pluginu

```bash
# Sprawdź strukturę plików
./package.sh

# Sprawdź zawartość archiwum
unzip -l dify-zulip-plugin-v0.0.1.difypkg
```

### 3. Walidacja konfiguracji YAML

```bash
# Sprawdź poprawność plików YAML (jeśli masz yamllint)
pip install yamllint
yamllint manifest.yaml
yamllint group/zulip.yaml
yamllint endpoints/zulip.yaml
```

## Testy po wdrożeniu

### 1. Test instalacji pluginu

1. **Wgraj plugin do Dify**
2. **Sprawdź logi podczas instalacji**:
   ```bash
   tail -f /var/log/dify/app.log | grep -i plugin
   ```
3. **Sprawdź czy plugin pojawił się w liście**

### 2. Test konfiguracji

1. **Przejdź do konfiguracji pluginu Zulip**
2. **Wypełnij wszystkie wymagane pola**
3. **Zapisz konfigurację**
4. **Sprawdź czy nie ma błędów walidacji**

### 3. Test połączenia z Zulipem

#### Test API klucza
```bash
# Sprawdź czy API key działa
ZULIP_EMAIL="twój-bot@organizacja.zulipchat.com"
ZULIP_API_KEY="twój-api-key"
ZULIP_URL="https://twoja-organizacja.zulipchat.com"

curl -H "Authorization: Basic $(echo -n "$ZULIP_EMAIL:$ZULIP_API_KEY" | base64)" \
     "$ZULIP_URL/api/v1/users/me"
```

#### Test webhook endpoint
```bash
# Test basic webhook endpoint
DIFY_URL="https://twoja-dify-instancja.com"

curl -X POST "$DIFY_URL/v1/plugins/zulip/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "data": {
      "id": 12345,
      "sender_email": "test@example.com", 
      "sender_full_name": "Test User",
      "content": "Test message",
      "display_recipient": "general",
      "subject": "Test",
      "type": "stream",
      "timestamp": 1640995200
    }
  }'
```

### 4. Test funkcjonalności end-to-end

#### Test 1: Wiadomość prywatna
1. **W Zulipie wyślij prywatną wiadomość do bota**:
   ```
   Cześć! Jak się masz?
   ```
2. **Sprawdź czy bot odpowiada**
3. **Sprawdź logi Dify**:
   ```bash
   tail -f /var/log/dify/app.log | grep -i zulip
   ```

#### Test 2: Wiadomość publiczna z wzmianką
1. **W dozwolonym strumieniu wyślij**:
   ```
   @dify-bot Jaka jest pogoda dzisiaj?
   ```
2. **Sprawdź czy bot odpowiada w tym samym wątku**

#### Test 3: Wiadomość bez wzmianki (jeśli włączone)
1. **Jeśli `respond_to_mentions_only` jest `false`**
2. **Wyślij wiadomość bez wzmianki w dozwolonym strumieniu**
3. **Sprawdź czy bot odpowiada**

#### Test 4: Wiadomość w niedozwolonym strumieniu
1. **Wyślij wiadomość wzmiankując bota w strumieniu nie na liście**
2. **Bot NIE powinien odpowiadać**

### 5. Test scenariuszy błędów

#### Test 1: Nieprawidłowy API key
1. **Zmień API key na nieprawidłowy**
2. **Wyślij wiadomość testową**
3. **Sprawdź czy błąd jest logowany**

#### Test 2: Niedostępny Zulip
1. **Zmień URL Zulip na nieprawidłowy**
2. **Wyślij wiadomość testową** 
3. **Sprawdź obsługę błędu połączenia**

#### Test 3: Nieprawidłowa aplikacja Dify
1. **Wybierz nieistniejącą aplikację Dify**
2. **Sprawdź czy błąd jest odpowiednio obsłużony**

## Monitorowanie w produkcji

### 1. Metryki do śledzenia

```bash
# Liczba otrzymanych wiadomości
grep "Otrzymano webhook od Zulip" /var/log/dify/app.log | wc -l

# Liczba udanych odpowiedzi
grep "Wiadomość wysłana pomyślnie do Zulip" /var/log/dify/app.log | wc -l

# Błędy
grep "ERROR.*zulip" /var/log/dify/app.log

# Czas odpowiedzi (jeśli logowany)
grep "response_time" /var/log/dify/app.log
```

### 2. Alerty

Skonfiguruj alerty dla:
- Brak aktywności bota > 1 godzina
- Wskaźnik błędów > 5%
- Czas odpowiedzi > 10 sekund
- Błędy połączenia z Zulipem

### 3. Dashboard monitoringu

Przykładowe metryki do dashboardu:
- Liczba wiadomości na godzinę
- Średni czas odpowiedzi
- Wskaźnik sukcesu
- Najpopularniejsze pytania
- Aktywność według strumieni

## Testy obciążeniowe

### 1. Test wielu jednoczesnych wiadomości

```bash
#!/bin/bash
# test_load.sh

DIFY_URL="https://twoja-dify-instancja.com"
ENDPOINT="$DIFY_URL/v1/plugins/zulip/webhook"

# Wyślij 10 równoległych żądań
for i in {1..10}; do
  curl -X POST "$ENDPOINT" \
    -H "Content-Type: application/json" \
    -d "{
      \"type\": \"message\",
      \"data\": {
        \"id\": $((12345 + i)),
        \"sender_email\": \"test$i@example.com\",
        \"sender_full_name\": \"Test User $i\",
        \"content\": \"Test message $i\",
        \"display_recipient\": \"general\",
        \"subject\": \"Load Test\",
        \"type\": \"stream\"
      }
    }" &
done

wait
echo "Test obciążeniowy zakończony"
```

### 2. Test długotrwałych konwersacji

1. **Wyślij serię wiadomości w tej samej konwersacji**
2. **Sprawdź czy kontekst jest zachowywany**
3. **Monitoruj użycie pamięci**

## Rozwiązywanie problemów testowych

### Problem: Bot nie odpowiada

**Kroki diagnostyczne:**
1. Sprawdź logi Dify
2. Sprawdź konfigurację pluginu
3. Przetestuj API Zulip ręcznie
4. Sprawdź czy aplikacja Dify działa
5. Przetestuj webhook endpoint bezpośrednio

### Problem: Błędy 500

**Kroki diagnostyczne:**
1. Sprawdź szczegółowe logi błędów
2. Sprawdź czy wszystkie zależności są zainstalowane
3. Sprawdź uprawnienia bota w Zulipie
4. Przetestuj z prostszą wiadomością

### Problem: Opóźnienia w odpowiedziach

**Kroki diagnostyczne:**
1. Sprawdź obciążenie serwera Dify
2. Sprawdź czas odpowiedzi aplikacji AI
3. Sprawdź połączenie sieciowe z Zulipem
4. Rozważ optymalizację prompta

## Automatyzacja testów

### 1. Skrypt CI/CD

```yaml
# .github/workflows/test-plugin.yml
name: Test Dify Zulip Plugin

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest yamllint
        
    - name: Lint YAML files
      run: |
        yamllint manifest.yaml
        yamllint group/zulip.yaml
        yamllint endpoints/zulip.yaml
        
    - name: Run unit tests
      run: |
        python -m pytest tests/ -v
        
    - name: Package plugin
      run: |
        chmod +x package.sh
        ./package.sh
        
    - name: Validate package
      run: |
        unzip -t dify-zulip-plugin-v*.difypkg
```

### 2. Skrypt testów integracyjnych

```bash
#!/bin/bash
# integration_test.sh

set -e

echo "🧪 Uruchamianie testów integracyjnych..."

# Sprawdź zmienne środowiskowe
required_vars=("DIFY_URL" "ZULIP_URL" "ZULIP_BOT_EMAIL" "ZULIP_API_KEY")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "❌ Brak zmiennej środowiskowej: $var"
        exit 1
    fi
done

# Test 1: Połączenie z Zulipem
echo "🔗 Test połączenia z Zulipem..."
curl -f -H "Authorization: Basic $(echo -n "$ZULIP_BOT_EMAIL:$ZULIP_API_KEY" | base64)" \
     "$ZULIP_URL/api/v1/users/me" > /dev/null

# Test 2: Webhook endpoint
echo "🔗 Test webhook endpoint..."
curl -f -X POST "$DIFY_URL/v1/plugins/zulip/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "data": {
      "id": 99999,
      "sender_email": "integration-test@example.com",
      "sender_full_name": "Integration Test",
      "content": "Integration test message",
      "display_recipient": "test",
      "subject": "Integration Test",
      "type": "stream"
    }
  }' > /dev/null

echo "✅ Testy integracyjne zakończone pomyślnie"
```

## Checklist przed wdrożeniem produkcyjnym

- [ ] Wszystkie testy jednostkowe przechodzą
- [ ] Pliki YAML są poprawne syntaktycznie  
- [ ] Plugin pakuje się bez błędów
- [ ] Test połączenia z Zulipem działa
- [ ] Test webhook endpoint działa
- [ ] Przetestowano scenariusze błędów
- [ ] Skonfigurowano monitorowanie
- [ ] Przygotowano alerty
- [ ] Dokumentacja jest aktualna
- [ ] Zespół zna procedury wsparcia 