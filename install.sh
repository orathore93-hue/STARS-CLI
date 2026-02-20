#!/usr/bin/env bash
set -e

echo "🌟 Installing STARS CLI..."

# 1. Detect Operating System
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=linux;;
    Darwin*)    PLATFORM=darwin;;
    CYGWIN*|MINGW*|MSYS*) PLATFORM=windows;;
    *)          echo "❌ Unsupported OS: ${OS}"; exit 1;;
esac

# 2. Detect Architecture
ARCH="$(uname -m)"
case "${ARCH}" in
    x86_64|amd64) ARCH_NAME=amd64;;
    arm64|aarch64) ARCH_NAME=arm64;;
    *)             echo "❌ Unsupported architecture: ${ARCH}"; exit 1;;
esac

# 3. Construct the exact binary name based on the GitHub Actions matrix
REPO="orathore93-hue/STARS-CLI"

if [ "$PLATFORM" = "windows" ]; then
    BINARY_NAME="stars-windows-${ARCH_NAME}.exe"
    DEST_BINARY="stars.exe"
else
    BINARY_NAME="stars-${PLATFORM}-${ARCH_NAME}"
    DEST_BINARY="stars"
fi

# 4. Fetch the latest release tag from GitHub API
echo "🔍 Fetching latest release version..."
LATEST_TAG=$(curl -s "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_TAG" ]; then
    echo "❌ Failed to fetch the latest release tag. Check your internet connection."
    exit 1
fi

DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${LATEST_TAG}/${BINARY_NAME}"
TMP_FILE="/tmp/${DEST_BINARY}"

# 5. Download the binary
echo "⬇️ Downloading STARS ${LATEST_TAG} for ${PLATFORM}-${ARCH_NAME}..."
curl -L --progress-bar "$DOWNLOAD_URL" -o "$TMP_FILE"

# 6. Download and verify checksum
echo "🔐 Verifying checksum..."
CHECKSUM_URL="${DOWNLOAD_URL}.sha256"
curl -sL "$CHECKSUM_URL" -o "${TMP_FILE}.sha256"

if [ -f "${TMP_FILE}.sha256" ]; then
    if command -v shasum >/dev/null 2>&1; then
        # macOS/Linux with shasum
        cd /tmp && shasum -a 256 -c "${DEST_BINARY}.sha256" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "❌ Checksum verification failed! File may be corrupted or tampered."
            exit 1
        fi
        echo "✅ Checksum verified"
    elif command -v sha256sum >/dev/null 2>&1; then
        # Linux with sha256sum
        cd /tmp && sha256sum -c "${DEST_BINARY}.sha256" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "❌ Checksum verification failed! File may be corrupted or tampered."
            exit 1
        fi
        echo "✅ Checksum verified"
    else
        echo "⚠️  Warning: No checksum tool found, skipping verification"
    fi
else
    echo "⚠️  Warning: Checksum file not found, skipping verification"
fi

# 7. Make executable
chmod +x "$TMP_FILE"

# 8. Move to system PATH
DEST_DIR="/usr/local/bin"
echo "📦 Moving binary to ${DEST_DIR}..."

# Use sudo if we don't have write permissions to /usr/local/bin
if [ ! -w "$DEST_DIR" ]; then
    echo "🔑 Requesting sudo permissions for installation..."
    SUDO="sudo"
else
    SUDO=""
fi

$SUDO mv "$TMP_FILE" "${DEST_DIR}/${DEST_BINARY}"

echo ""
echo -e "\033[92m✅ STARS CLI successfully installed!\033[0m"
echo "Run 'stars --help' to get started."
