#!/usr/bin/env bash

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$HOME/.config/fish"
mkdir -p "$HOME/.config/nvim"
mkdir -p "$HOME/texmf/tex/latex"

ln -sfn \
    "$WORKSPACE_DIR/dotfiles/.config/fish/config.fish" \
    "$HOME/.config/fish/config.fish"

ln -sfn \
    "$WORKSPACE_DIR/dotfiles/.config/nvim/init.lua" \
    "$HOME/.config/nvim/init.lua"

ln -sfnT \
    "$WORKSPACE_DIR/dotfiles/texmf/tex/latex/evan" \
    "$HOME/texmf/tex/latex/evan"


git config --global core.editor nvim
git config --global init.defaultBranch main

sudo chsh "$(id -un)" --shell /usr/bin/fish

echo "Workspace configuration complete."