set -gx EDITOR nvim
set -gx VISUAL nvim

set -g fish_greeting

alias vim='nvim'
alias vi='nvim'
alias ll='ls -lah'

alias gs='git status'
alias gd='git diff'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'

function cxx
    if test (count $argv) -ne 1
        echo "Usage: cxx filename.cpp"
        return 1
    end

    set output (string replace -r '\.cpp$' '' $argv[1])

    g++ -std=c++20 \
        -Wall \
        -Wextra \
        -Wpedantic \
        $argv[1] \
        -o $output
end
