#!/usr/bin/env bash
set -euo pipefail
workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
backup_root="$HOME/.local/state/latex-workspace/backups/$(date +%Y%m%d-%H%M%S)"
link_with_backup() {
    local source="$1" destination="$2"
    mkdir -p "$(dirname "$destination")"
    if [[ -L "$destination" && "$(readlink "$destination")" == "$source" ]]; then return; fi
    if [[ -e "$destination" || -L "$destination" ]]; then
        mkdir -p "$backup_root"
        mv -- "$destination" "$backup_root/$(basename "$destination")"
        printf 'Previous configuration saved in %s\n' "$backup_root"
    fi
    ln -s -- "$source" "$destination"
}
# All paths derive from this checkout; no Git identity, credentials or remotes are set.
link_with_backup "$workspace_dir/tools/lw.py" "$HOME/.local/bin/lw"
link_with_backup "$workspace_dir/dotfiles/texmf/tex/latex/evan" "$HOME/texmf/tex/latex/evan"
chmod +x "$workspace_dir/tools/lw.py"
if [[ "${1:-}" == "--dotfiles" ]]; then
    link_with_backup "$workspace_dir/dotfiles/.config/fish/config.fish" "$HOME/.config/fish/config.fish"
    link_with_backup "$workspace_dir/dotfiles/.config/nvim/init.lua" "$HOME/.config/nvim/init.lua"
elif [[ -n "${1:-}" ]]; then
    echo 'Usage: bash install.sh [--dotfiles]' >&2
    exit 2
fi
printf 'Ready. Run: ~/.local/bin/lw doctor\n'
printf 'Create another project: ~/.local/bin/lw init /path/to/notes\n'
