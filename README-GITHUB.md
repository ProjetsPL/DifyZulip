# Dify-Zulip Integration Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

Plugin umożliwiający integrację aplikacji Dify z Zulipem, pozwalając na dwukierunkową komunikację między chatbotami/agentami AI w Dify a użytkownikami w Zulipie.

## 🚀 Instalacja z repozytorium GitHub

### Metoda 1: Bezpośrednia instalacja z GitHub w Dify

1. **Skopiuj URL repozytorium**:
   ```
   https://github.com/ProjetsPL/dify-zulip-plugin
   ```

2. **W interfejsie Dify**:
   - Przejdź do sekcji **Plugins/Extensions**
   - Kliknij **"Install from GitHub"** lub **"Install Plugin"**
   - Wklej URL repozytorium: `https://github.com/ProjetsPL/dify-zulip-plugin`
   - Kliknij **"Install"**

### Metoda 2: Pobierz i wgraj jako plik

1. **Pobierz kod**:
   ```bash
   git clone https://github.com/ProjetsPL/dify-zulip-plugin.git
   cd dify-zulip-plugin
   ```

2. **Spakuj plugin**:
   ```bash
   chmod +x package.sh
   ./package.sh
   ```

3. **Wgraj do Dify**:
   - W interfejsie Dify przejdź do **Plugins**
   - Kliknij **"Upload Plugin"**
   - Wybierz plik `dify-zulip-plugin-v0.0.1.difypkg`

### Metoda 3: Pobierz gotowy pakiet

1. Przejdź do [Releases](https://github.com/ProjetsPL/dify-zulip-plugin/releases)
2. Pobierz najnowszy plik `.difypkg`
3. Wgraj go w Dify przez **Upload Plugin**

## 📋 Wymagania

- **Dify**: Self-hosted z obsługą pluginów
- **Zulip**: Self-hosted lub cloud
- **Python**: 3.12+

## ⚡ Szybki start

### 1. Konfiguracja Zulipa

**Utwórz bota w Zulipie:**
1. Przejdź do **Organization settings → Bots**
2. Kliknij **"Add a new bot"**
3. Wybierz **"Generic bot"**
4. Nazwa: `Dify AI Assistant`
5. Username: `dify-bot`
6. **Skopiuj API key** - będzie potrzebny w Dify

### 2. Konfiguracja w Dify

Po zainstalowaniu pluginu:

1. **Przejdź do ustawień pluginu Zulip**
2. **Wypełnij formularz**:
   - **Zulip Site URL**: `https://twoja-organizacja.zulipchat.com`
   - **Bot Email**: `dify-bot@twoja-organizacja.zulipchat.com`
   - **Bot API Key**: [wklej API key z Zulip]
   - **Dify App**: Wybierz aplikację do obsługi wiadomości
   - **Respond to Mentions Only**: `true` (bot odpowiada tylko na wzmianki)
   - **Allowed Streams**: `general,support,ai-chat` (opcjonalnie)

3. **Zapisz konfigurację**

### 3. Test

**Wyślij wiadomość w Zulipie:**
```
@dify-bot Cześć! Jak się masz?
```

Bot powinien odpowiedzieć używając skonfigurowanej aplikacji Dify! 🎉

## 🔧 Funkcjonalności

- ✅ **Odbieranie wiadomości z Zulipa** - automatyczne reagowanie na wiadomości
- ✅ **Inteligentne filtrowanie** - tylko wzmianki vs wszystkie wiadomości  
- ✅ **Wiadomości prywatne** - obsługa wiadomości prywatnych
- ✅ **Konfigurowalny dostęp** - ograniczenie do określonych strumieni
- ✅ **Kontekst konwersacji** - przekazywanie metadanych do Dify
- ✅ **Wielojęzyczność** - interfejs w EN/ZH/PT/JP/PL

## 📁 Struktura projektu

```
dify-zulip-plugin/
├── manifest.yaml              # Konfiguracja pluginu
├── main.py                    # Punkt wejścia
├── requirements.txt           # Zależności Python
├── group/zulip.yaml          # Formularz konfiguracyjny
├── endpoints/
│   ├── zulip.yaml            # Konfiguracja webhook
│   └── zulip.py              # Logika integracji
├── icon.svg                  # Ikona pluginu
├── README.md                 # Dokumentacja
├── DEPLOYMENT.md             # Instrukcje wdrożenia
├── TESTING.md                # Procedury testowania
└── examples/                 # Przykłady konfiguracji
```

## 🐛 Rozwiązywanie problemów

### Bot nie odpowiada
1. Sprawdź logi w Dify
2. Sprawdź uprawnienia bota w Zulipie  
3. Sprawdź poprawność API key
4. Sprawdź URL Zulip

### Błędy instalacji pluginu
Jeśli wystąpi błąd weryfikacji podpisu, dodaj do `/docker/.env`:
```bash
FORCE_VERIFYING_SIGNATURE=false
```

Następnie restartuj Dify:
```bash
cd docker
docker compose down
docker compose up -d
```

## 📚 Dokumentacja

- **[README.md](README.md)** - Kompletna dokumentacja użytkownika
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Instrukcje wdrożenia krok po kroku
- **[TESTING.md](TESTING.md)** - Procedury testowania
- **[examples/](examples/)** - Przykłady konfiguracji

## 🤝 Wsparcie

1. **Sprawdź dokumentację** w plikach README, DEPLOYMENT i TESTING
2. **Sprawdź logi** w Dify i Zulipie
3. **Otwórz issue** na GitHubie jeśli problem się utrzymuje

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE) dla szczegółów.

## 🙏 Autorzy

- **ProjetsPL** - *Autor pluginu* - [@ProjetsPL](https://github.com/ProjetsPL)

---

**🔗 Przydatne linki:**
- [Dokumentacja Dify](https://docs.dify.ai/)
- [Dokumentacja Zulip API](https://zulip.com/api/)
- [Dify Plugins Marketplace](https://github.com/langgenius/dify-plugins) 