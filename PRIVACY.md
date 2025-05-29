# Polityka Prywatności - Wtyczka Zulip dla Dify

## Przegląd

Ta wtyczka Zulip dla Dify umożliwia integrację z platformą czatu Zulip w celu wysyłania i odbierania wiadomości. Niniejsza polityka prywatności opisuje, jakie dane są przetwarzane i w jaki sposób.

## Zbierane Dane

### Dane Uwierzytelniania
- **URL Serwera Zulip**: Adres Twojego serwera Zulip
- **Email**: Adres email używany do logowania w Zulip
- **Klucz API**: Klucz API generowany przez Zulip do uwierzytelniania

### Dane Wiadomości
- **Treść wiadomości**: Tekst wiadomości wysyłanych i odbieranych
- **Metadane wiadomości**: Informacje o nadawcy, odbiorcy, czasie wysłania, strumieniu i temacie
- **Historia wiadomości**: Wiadomości pobrane z określonego zakresu czasowego

## Sposób Wykorzystania Danych

### Dane Uwierzytelniania
- Są używane wyłącznie do nawiązania bezpiecznego połączenia z serwerem Zulip
- Przechowywane bezpiecznie w systemie Dify jako zaszyfrowane secrets
- Nie są udostępniane stronom trzecim

### Dane Wiadomości
- Przetwarzane wyłącznie w celu realizacji funkcji wysyłania i odbierania wiadomości
- Nie są przechowywane przez wtyczkę poza czasem niezbędnym do przetworzenia
- Przekazywane bezpośrednio między Dify a serwerem Zulip

## Bezpieczeństwo Danych

- Wszystkie połączenia z serwerem Zulip używają protokołu HTTPS
- Klucze API są przechowywane jako zaszyfrowane secrets w Dify
- Wtyczka nie loguje ani nie przechowuje zawartości wiadomości
- Walidacja credentials odbywa się przy każdej konfiguracji

## Udostępnianie Danych

Wtyczka **nie udostępnia** żadnych danych stronom trzecim. Wszystkie dane:
- Pozostają w ekosystemie Dify-Zulip
- Są przetwarzane lokalnie przez wtyczkę
- Nie są wysyłane do żadnych zewnętrznych serwisów poza skonfigurowanym serwerem Zulip

## Przechowywanie Danych

- **Dane uwierzytelniania**: Przechowywane w Dify do momentu usunięcia konfiguracji
- **Dane wiadomości**: Nie są przechowywane przez wtyczkę - przetwarzane w czasie rzeczywistym
- **Logi**: Wtyczka może tworzyć logi techniczne niezbędne do debugowania (bez zawartości wiadomości)

## Prawa Użytkownika

Jako użytkownik masz prawo do:
- Usunięcia konfiguracji wtyczki w dowolnym momencie
- Odwołania klucza API w ustawieniach Zulip
- Sprawdzenia jakie dane są przetwarzane przez wtyczkę

## Zgodność z Przepisami

Ta wtyczka:
- Przestrzega zasad RODO dla użytkowników w UE
- Nie przetwarza danych osobowych poza niezbędnym minimum
- Zapewnia transparentność w zakresie przetwarzania danych

## Kontakt

W przypadku pytań dotyczących prywatności lub przetwarzania danych, skontaktuj się z autorem wtyczki: **bartlomiejmatlega**

## Aktualizacje

Ta polityka prywatności może być aktualizowana w celu odzwierciedlenia zmian we wtyczce. Użytkownicy zostaną poinformowani o istotnych zmianach.

**Ostatnia aktualizacja**: Styczeń 2025