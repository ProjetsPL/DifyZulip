# Release v0.0.1 - Dify-Zulip Integration Plugin

## 🎉 Pierwsza wersja publiczna pluginu Dify-Zulip!

### ✨ Główne funkcjonalności

- **🔗 Dwukierunkowa integracja Dify ⟷ Zulip**
  - Odbieranie wiadomości z Zulipa przez webhook
  - Przekazywanie do aplikacji Dify do przetworzenia przez AI
  - Automatyczne wysyłanie odpowiedzi z powrotem do Zulipa

- **🎯 Inteligentne filtrowanie wiadomości**
  - Opcja reagowania tylko na wzmianki bota (`@dify-bot`)
  - Możliwość przetwarzania wszystkich wiadomości w określonych strumieniach
  - Ograniczanie dostępu do konkretnych strumieni Zulip

- **💬 Pełna obsługa typów wiadomości**
  - Wiadomości publiczne w strumieniach
  - Wiadomości prywatne (direct messages)
  - Zachowanie kontekstu konwersacji

- **🌍 Wsparcie wielojęzyczne**
  - Interfejs w 5 językach: EN, ZH, PT, JP, PL
  - Pełna lokalizacja formularzy konfiguracyjnych

- **🔧 Elastyczna konfiguracja**
  - Brak hardcode'owanych URL-i czy kluczy API
  - Wsparcie dla self-hosted instancji Dify i Zulip
  - Konfigurowalny routing do różnych aplikacji Dify

### 📦 Co zawiera ten release

- **Pakiet pluginu**: `dify-zulip-plugin-v0.0.1.difypkg` (21KB)
- **Kompletna dokumentacja**:
  - `README.md` - Główna dokumentacja użytkownika
  - `DEPLOYMENT.md` - Instrukcje wdrożenia krok po kroku
  - `TESTING.md` - Procedury testowania
  - `README-GITHUB.md` - Instrukcje instalacji z GitHub
- **Przykłady konfiguracji** w katalogu `examples/`
- **Testy jednostkowe** w katalogu `tests/`

### 🚀 Instalacja

#### Metoda 1: Bezpośrednio z GitHub
```bash
https://github.com/ProjetsPL/dify-zulip-plugin
```

#### Metoda 2: Pobierz pakiet .difypkg
1. Pobierz `dify-zulip-plugin-v0.0.1.difypkg` z tego release'a
2. Wgraj w Dify przez **Admin → Plugins → Upload Plugin**

### ⚡ Szybki start

1. **Utwórz bota w Zulipie**:
   - Przejdź do Organization settings → Bots
   - Dodaj nowego bota typu "Generic bot"
   - Skopiuj API key

2. **Zainstaluj plugin w Dify**

3. **Skonfiguruj**:
   - Zulip Site URL: `https://twoja-organizacja.zulipchat.com`
   - Bot Email i API Key
   - Wybierz aplikację Dify do obsługi

4. **Testuj**:
   ```
   @dify-bot Cześć! Jak się masz?
   ```

### 🔧 Wymagania techniczne

- **Dify**: Self-hosted z obsługą pluginów
- **Zulip**: Self-hosted lub cloud 
- **Python**: 3.12+
- **Zależności**: `requests`, `werkzeug`

### 🐛 Znane ograniczenia

- Wymaga self-hosted Dify z włączonymi pluginami
- Bot musi mieć uprawnienia do odczytu wiadomości w skonfigurowanych strumieniach
- Zalecane wyłączenie weryfikacji podpisu dla pluginów deweloperskich

### 📚 Dokumentacja

Szczegółowe instrukcje znajdziesz w:
- [README.md](README.md) - Kompletna dokumentacja
- [DEPLOYMENT.md](DEPLOYMENT.md) - Instrukcje wdrożenia
- [TESTING.md](TESTING.md) - Procedury testowania

### 🤝 Wsparcie

- 📋 [Otwórz issue](https://github.com/ProjetsPL/dify-zulip-plugin/issues) jeśli napotkasz problemy
- 📖 Sprawdź dokumentację przed zgłoszeniem błędu
- 💡 Sugestie funkcjonalności są mile widziane!

---

**🏷️ Autor**: ProjetsPL  
**📅 Data**: 29 maja 2025  
**🔖 Wersja**: 0.0.1  
**📄 Licencja**: MIT 