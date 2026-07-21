#!/usr/bin/env bash

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Applying Fish and NeoVim configuration..."

mkdir -p "$HOME/.config"

ln -sfnT \
    "$WORKSPACE_DIR/dotfiles/.config/fish" \
    "$HOME/.config/fish"

ln -sfnT \
    "$WORKSPACE_DIR/dotfiles/.config/nvim" \
    "$HOME/.config/nvim"

git config --global core.editor nvim
git config --global init.defaultBranch main

sudo chsh "$(id -un)" --shell /usr/bin/fish

echo "Workspace configuration complete."
