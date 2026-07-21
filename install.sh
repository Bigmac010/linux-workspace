#!/usr/bin/env bash

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$HOME/.config/fish"
mkdir -p "$HOME/.config/nvim"

ln -sfn \
    "$WORKSPACE_DIR/dotfiles/.config/fish/config.fish" \
    "$HOME/.config/fish/config.fish"

ln -sfn \
    "$WORKSPACE_DIR/dotfiles/.config/nvim/init.lua" \
    "$HOME/.config/nvim/init.lua"

git config --global core.editor nvim
git config --global init.defaultBranch main

sudo chsh "$(id -un)" --shell /usr/bin/fish

echo "Workspace configuration complete."