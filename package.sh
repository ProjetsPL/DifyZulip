#!/bin/bash

# Skrypt do pakowania pluginu Dify-Zulip
# Użycie: ./package.sh [nazwa-wersji]

set -e

VERSION=${1:-$(grep "version:" manifest.yaml | cut -d' ' -f2)}
PACKAGE_NAME="dify-zulip-plugin-v${VERSION}"

echo "📦 Pakowanie pluginu Dify-Zulip w wersji: ${VERSION}"

# Sprawdź czy wszystkie wymagane pliki istnieją
echo "🔍 Sprawdzanie wymaganych plików..."
required_files=(
    "manifest.yaml"
    "main.py"
    "requirements.txt"
    "group/zulip.yaml"
    "endpoints/zulip.yaml"
    "endpoints/zulip.py"
    "icon.svg"
)

for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Błąd: Brakuje pliku $file"
        exit 1
    fi
done

echo "✅ Wszystkie wymagane pliki są obecne"

# Utwórz katalog tymczasowy
temp_dir=$(mktemp -d)

echo "📁 Kopiowanie plików do katalogu tymczasowego..."

# Kopiuj pliki pluginu bezpośrednio do katalogu tymczasowego (bez podkatalogu)
rsync -av \
    --exclude='.git*' \
    --exclude='*.DS_Store' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='tests/' \
    --exclude='package.sh' \
    --exclude='*.zip' \
    --exclude='*.difypkg' \
    --exclude='.pytest_cache' \
    --exclude='venv/' \
    --exclude='env/' \
    ./ "$temp_dir/"

# Przejdź do katalogu tymczasowego
cd "$temp_dir"

echo "🗜️  Tworzenie archiwum .difypkg..."
zip -r "${PACKAGE_NAME}.difypkg" . -x ".*"

# Wróć do katalogu głównego i przenieś archiwum
cd "$OLDPWD"
mv "$temp_dir/${PACKAGE_NAME}.difypkg" ./

# Oczyść katalog tymczasowy
rm -rf "$temp_dir"

echo "✅ Plugin spakowany pomyślnie: ${PACKAGE_NAME}.difypkg"

# Wyświetl informacje o pliku
echo ""
echo "📊 Informacje o pakiecie:"
ls -lh "${PACKAGE_NAME}.difypkg"

echo ""
echo "📋 Zawartość pakietu:"
unzip -l "${PACKAGE_NAME}.difypkg" | head -20

echo ""
echo "🎉 Gotowe! Możesz teraz wgrać plik ${PACKAGE_NAME}.difypkg do Dify."
echo ""
echo "📖 Następne kroki:"
echo "1. Zaloguj się do interfejsu administratora Dify"
echo "2. Przejdź do sekcji Plugins/Extensions"  
echo "3. Kliknij 'Upload Plugin' lub 'Install Plugin'"
echo "4. Wybierz plik ${PACKAGE_NAME}.difypkg"
echo "5. Potwierdź instalację"
echo "6. Skonfiguruj plugin zgodnie z README.md"