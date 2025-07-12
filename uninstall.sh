#!/bin/bash
# File Organizer Uninstallation Script

set -e

echo "🗑️  File Organizer Uninstallation Script"
echo "======================================="

COMMAND_NAME="file-organizer"

# Check common installation locations
INSTALL_LOCATIONS=(
    "/usr/local/bin/$COMMAND_NAME"
    "$HOME/.local/bin/$COMMAND_NAME"
    "/usr/bin/$COMMAND_NAME"
)

FOUND_INSTALLATIONS=()

# Find all installations
for location in "${INSTALL_LOCATIONS[@]}"; do
    if [[ -f "$location" ]]; then
        FOUND_INSTALLATIONS+=("$location")
    fi
done

if [[ ${#FOUND_INSTALLATIONS[@]} -eq 0 ]]; then
    echo "⚠️  No installations of $COMMAND_NAME found."
    echo "Checked locations:"
    for location in "${INSTALL_LOCATIONS[@]}"; do
        echo "  - $location"
    done
    exit 0
fi

# Show found installations
echo "Found installations:"
for installation in "${FOUND_INSTALLATIONS[@]}"; do
    echo "  - $installation"
done
echo ""

# Ask for confirmation
read -p "Do you want to remove all installations? [y/N]: " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

# Remove installations
echo "Removing installations..."
for installation in "${FOUND_INSTALLATIONS[@]}"; do
    if rm "$installation" 2>/dev/null; then
        echo "✅ Removed: $installation"
    else
        echo "❌ Failed to remove: $installation"
        echo "You may need to run with sudo or check permissions"
    fi
done

echo ""
echo "🎉 Uninstallation complete!"
echo "The command '$COMMAND_NAME' has been removed from your system." 