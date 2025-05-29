# Przykładowe konfiguracje Plugin Dify-Zulip

Ten plik zawiera przykłady konfiguracji dla różnych scenariuszy użycia pluginu Dify-Zulip.

## Scenariusz 1: Bot wsparcia technicznego

### Opis
Bot który pomaga w podstawowym wsparciu technicznym, reaguje tylko na wzmianki w określonych strumieniach.

### Konfiguracja Dify App
```yaml
Type: Chatbot
Name: Technical Support Assistant
System Prompt: |
  Jesteś asystentem wsparcia technicznego. Odpowiadasz na pytania związane z:
  - Problemami z logowaniem
  - Kwestiami dotyczącymi hasła
  - Podstawowymi problemami z oprogramowaniem
  - Kierowaniem do właściwych działów
  
  Zawsze bądź pomocny i profesjonalny. Jeśli nie znasz odpowiedzi, 
  poinformuj o tym i zasugeruj kontakt z zespołem wsparcia.
```

### Konfiguracja pluginu
```yaml
Zulip Site URL: https://firma.zulipchat.com
Bot Email: support-bot@firma.zulipchat.com
Bot API Key: [twój-api-key]
Dify App: Technical Support Assistant
Respond to Mentions Only: true
Allowed Streams: support,help,it-questions
```

## Scenariusz 2: AI Asystent dla wszystkich

### Opis
Uniwersalny AI asystent który pomaga we wszystkich sprawach organizacyjnych.

### Konfiguracja Dify App
```yaml
Type: Agent
Name: Universal AI Assistant
System Prompt: |
  Jesteś uniwersalnym asystentem AI dla organizacji. Pomagasz w:
  - Odpowiadaniu na pytania ogólne
  - Wyjaśnianiu procesów wewnętrznych
  - Wyszukiwaniu informacji
  - Planowaniu i organizacji
  
  Masz dostęp do wiedzy organizacyjnej i możesz korzystać z różnych narzędzi.
Tools:
  - Search Tool (dla dostępu do bazy wiedzy)
  - Calendar Tool (dla terminarz)
  - Task Manager Tool
```

### Konfiguracja pluginu
```yaml
Zulip Site URL: https://firma.zulipchat.com
Bot Email: ai-assistant@firma.zulipchat.com
Bot API Key: [twój-api-key]
Dify App: Universal AI Assistant
Respond to Mentions Only: false
Allowed Streams: general,random,projects
```

## Scenariusz 3: Bot moderacyjny

### Opis
Bot który moderuje konwersacje i pomaga w zarządzaniu społecznością.

### Konfiguracja Dify App
```yaml
Type: Workflow
Name: Community Moderator
Description: |
  Workflow który:
  1. Analizuje toksyczność wiadomości
  2. Sprawdza czy wiadomość narusza zasady
  3. Udziela ostrzeżeń lub wskazówek
  4. Eskaluje poważne problemy
```

### Konfiguracja pluginu
```yaml
Zulip Site URL: https://spolecznosc.zulipchat.com
Bot Email: moderator@spolecznosc.zulipchat.com
Bot API Key: [twój-api-key]
Dify App: Community Moderator
Respond to Mentions Only: false
Allowed Streams: general,offtopic,newbies
```

## Scenariusz 4: Bot dla wiadomości prywatnych

### Opis
Bot który obsługuje tylko wiadomości prywatne - osobisty asystent.

### Konfiguracja Dify App
```yaml
Type: Chatbot
Name: Personal Assistant
System Prompt: |
  Jesteś osobistym asystentem użytkownika. Pomagasz w:
  - Zarządzaniu zadaniami
  - Przypomnieniach
  - Odpowiadaniu na pytania prywatne
  - Organizacji pracy
  
  To jest prywatna konwersacja, więc możesz być bardziej personalny.
```

### Konfiguracja pluginu
```yaml
Zulip Site URL: https://firma.zulipchat.com
Bot Email: personal-assistant@firma.zulipchat.com
Bot API Key: [twój-api-key]
Dify App: Personal Assistant
Respond to Mentions Only: true
Allowed Streams: (pozostaw puste)
```

## Scenariusz 5: Multi-language support bot

### Opis
Bot który automatycznie wykrywa język i odpowiada w tym samym języku.

### Konfiguracja Dify App
```yaml
Type: Agent
Name: Multilingual Support Bot
System Prompt: |
  Jesteś wielojęzycznym asystentem wsparcia. Zasady:
  
  1. Automatycznie wykrywaj język wiadomości użytkownika
  2. Odpowiadaj w tym samym języku
  3. Obsługuj: polski, angielski, hiszpański, francuski
  4. Jeśli nie rozpoznasz języka, odpowiedz po angielsku
  
  Przykład:
  - Użytkownik: "Cześć, jak się masz?"
  - Ty: "Cześć! Świetnie, dziękuję. Jak mogę Ci pomóc?"
  
  - User: "Hello, how are you?"
  - You: "Hello! I'm doing great, thank you. How can I help you?"

Tools:
  - Language Detection Tool
  - Translation Tool (if needed)
```

### Konfiguracja pluginu
```yaml
Zulip Site URL: https://international.zulipchat.com
Bot Email: multilang-bot@international.zulipchat.com
Bot API Key: [twój-api-key]
Dify App: Multilingual Support Bot
Respond to Mentions Only: true
Allowed Streams: international,support,general
```

## Scenariusz 6: Code review bot

### Opis
Bot który pomaga w przeglądzie kodu i odpowiada na pytania techniczne.

### Konfiguracja Dify App
```yaml
Type: Agent
Name: Code Review Assistant
System Prompt: |
  Jesteś asystentem do przeglądu kodu i pomocy technicznej. Specjalizujesz się w:
  
  - Analizie kodu w różnych językach programowania
  - Sugerowaniu poprawek i ulepszeń
  - Wyjaśnianiu konceptów programistycznych
  - Best practices i wzorców projektowych
  - Pomocy w debugowaniu
  
  Gdy użytkownik wklei kod, przeanalizuj go pod kątem:
  - Poprawności składniowej
  - Efektywności
  - Czytelności
  - Bezpieczeństwa
  - Zgodności z konwencjami

Tools:
  - Code Analysis Tool
  - Documentation Search Tool
  - Vulnerability Scanner
```

### Konfiguracja pluginu
```yaml
Zulip Site URL: https://dev-team.zulipchat.com
Bot Email: code-reviewer@dev-team.zulipchat.com
Bot API Key: [twój-api-key]
Dify App: Code Review Assistant
Respond to Mentions Only: true
Allowed Streams: code-review,development,programming-help
```

## Konfiguracja zaawansowana webhook'ów

### Dla scenariuszy z wysokim ruchem

Jeśli masz dużo wiadomości, możesz skonfigurować outgoing webhook w Zulipie:

```yaml
# W ustawieniach organizacji Zulip
Outgoing Webhook Configuration:
  Service name: Dify Integration
  Service base URL: https://twoja-dify.com/v1/plugins/zulip
  Interface: Generic webhook
  Bot user: [wybierz swojego bota]
  Stream: [określ strumienie lub zostaw puste]
```

### Filtrowanie na poziomie Zulip

```python
# Możesz dodać dodatkowe filtrowanie w ustawieniach webhook'a Zulip
# Przykład: reaguj tylko na wiadomości zawierające słowa kluczowe
Keywords: ["help", "pomoc", "asystent", "ai", "bot"]
```

## Monitoring i metryki

### Przykładowa konfiguracja monitoringu

```yaml
# W aplikacji Dify można skonfigurować metryki
Metrics to track:
  - Liczba otrzymanych wiadomości
  - Czas odpowiedzi
  - Wskaźnik zadowolenia użytkowników
  - Najczęściej zadawane pytania
  - Błędy i wyjątki
```

### Alerty

```yaml
# Skonfiguruj alerty dla krytycznych sytuacji
Alerts:
  - Bot nie odpowiada > 5 minut
  - Wskaźnik błędów > 10%
  - Czas odpowiedzi > 30 sekund
  - Brak połączenia z Zulipem
```

## Tips dla różnych organizacji

### Małe zespoły (< 50 osób)
```yaml
Respond to Mentions Only: false
Allowed Streams: general
Bot: Uniwersalny asystent
```

### Średnie organizacje (50-200 osób)
```yaml
Respond to Mentions Only: true
Allowed Streams: support,general,random
Bot: Specjalistyczny bot wsparcia
```

### Duże organizacje (200+ osób)
```yaml
Respond to Mentions Only: true
Allowed Streams: it-support,hr-questions
Bot: Wyspecjalizowane boty dla różnych działów
```

### Organizacje międzynarodowe
```yaml
Bot: Wielojęzyczny z automatyczną detekcją języka
Konfiguracja: Różne instancje dla różnych stref czasowych
``` 