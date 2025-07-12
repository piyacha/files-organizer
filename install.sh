#!/bin/bash
# File Organizer Installation Script

set -e

echo "📦 File Organizer Installation Script"
echo "=================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Determine installation directory
if [[ -w /usr/local/bin ]]; then
    INSTALL_DIR="/usr/local/bin"
elif [[ -w "$HOME/.local/bin" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
    # Create directory if it doesn't exist
    mkdir -p "$INSTALL_DIR"
else
    echo "⚠️  Neither /usr/local/bin nor ~/.local/bin is writable."
    echo "Trying to install to ~/.local/bin with sudo..."
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

COMMAND_NAME="file-organizer"
INSTALL_PATH="$INSTALL_DIR/$COMMAND_NAME"

# Check if main.py exists
if [[ ! -f "main.py" ]]; then
    echo "❌ main.py not found in current directory."
    echo "Please run this script from the directory containing main.py"
    exit 1
fi

# Copy and install the script
echo "📋 Installing file-organizer to $INSTALL_PATH..."

# Make main.py executable
chmod +x main.py

# Copy the script
cp main.py "$INSTALL_PATH"

# Make sure it's executable
chmod +x "$INSTALL_PATH"

echo "✅ Installation complete!"
echo ""
echo "You can now use the command: $COMMAND_NAME"
echo ""
echo "Examples:"
echo "  $COMMAND_NAME --help"
echo "  $COMMAND_NAME -s ~/Downloads -d ~/organized"
echo "  $COMMAND_NAME -s ~/Downloads -d ~/organized --execute"
echo ""

# Check if the installation directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠️  Warning: $INSTALL_DIR is not in your PATH"
    echo "Add this line to your ~/.zshrc or ~/.bash_profile:"
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
    echo ""
    echo "Then run: source ~/.zshrc (or restart your terminal)"
fi

echo "🎉 Installation successful!" 