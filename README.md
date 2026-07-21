# Linux Workspace

A reproducible, cloud-based Linux development environment built with GitHub Codespaces.

This workspace is designed for:

- C and C++ programming
- Python programming
- Mathematics notes and solutions
- LaTeX document creation
- NeoVim and VimTeX
- Git and GitHub workflows
- Command-line development through Fish

The environment can be opened through:

- GitHub Codespaces in a browser
- VS Code desktop
- GitHub CLI over SSH
- Windows Terminal connected to the Codespace

## Overview

This repository contains both:

1. The definition of the Linux development environment.
2. Personal configuration for Fish, NeoVim, VimTeX and LaTeX.

Actual projects should normally remain in separate GitHub repositories.

A typical workspace looks like:

```text
/workspaces/
├── linux-workspace/
├── bmo/
├── competitive-programming/
├── geometry-notes/
└── other-projects/
```

`linux-workspace` defines the environment.

The other folders are independent Git repositories containing actual work.

## Included tools

### Development

- Git
- GCC and G++
- CMake
- GDB
- Python 3
- pip
- Python virtual environments

### Editors and shells

- Current stable NeoVim
- Fish shell
- VimTeX
- lazy.nvim
- VS Code C/C++ extension
- VS Code Python extension
- LaTeX Workshop

### LaTeX and mathematics

- TeX Live
- pdfLaTeX
- XeLaTeX
- LuaLaTeX
- latexmk
- Asymptote
- `evan.sty`

### Graphical applications

- Zathura
- xfce4-terminal

Zathura and xfce4-terminal are installed, but ordinary GitHub Codespaces sessions do not provide a graphical Linux desktop.

Inside Codespaces, the practical replacements are:

```text
Zathura          → VS Code internal PDF viewer
xfce4-terminal   → VS Code terminal or Windows Terminal over SSH
```

The generated PDF is the same regardless of the viewer used.

## Repository structure

```text
linux-workspace/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
│
├── dotfiles/
│   ├── .config/
│   │   ├── fish/
│   │   │   └── config.fish
│   │   └── nvim/
│   │       └── init.lua
│   │
│   └── texmf/
│       └── tex/
│           └── latex/
│               └── evan/
│                   └── evan.sty
│
├── .gitignore
├── install.sh
└── README.md
```

## What each file does

### `.devcontainer/devcontainer.json`

Defines how GitHub Codespaces should configure the workspace.

It controls:

- which Dockerfile is used;
- the Linux user;
- the post-creation setup command;
- VS Code extensions;
- VS Code terminal settings;
- LaTeX Workshop settings;
- permission to access additional repositories.

### `.devcontainer/Dockerfile`

Builds the Linux container and installs the required programs.

It installs:

- Fish
- Git
- C and C++ tools
- Python
- TeX Live
- latexmk
- Asymptote
- Zathura
- xfce4-terminal

It also downloads the current stable NeoVim release directly rather than relying on Ubuntu's potentially older NeoVim package.

### `install.sh`

Runs after the Codespace has been created.

It:

- links the Fish configuration;
- links the NeoVim configuration;
- links `evan.sty` into the user's TeX directory;
- sets NeoVim as Git's default editor;
- sets `main` as Git's default initial branch;
- sets Fish as the login shell.

### `dotfiles/.config/fish/config.fish`

Configures Fish and provides aliases and helper functions.

### `dotfiles/.config/nvim/init.lua`

Configures NeoVim, lazy.nvim and VimTeX.

### `dotfiles/texmf`

Contains personal TeX files that should be available to every LaTeX project in the workspace.

## Creating the Codespace

Open this repository on GitHub.

Select:

```text
Code
→ Codespaces
→ Create codespace on main
```

GitHub will:

1. Read `devcontainer.json`.
2. Build the Dockerfile.
3. Install the development tools.
4. Run `install.sh`.
5. Install the configured VS Code extensions.
6. Open the workspace.

The first build may take several minutes because TeX Live is relatively large.

## Repository permissions

The current `devcontainer.json` grants this Codespace write access to:

```text
Bigmac010/bmo
```

This allows the Codespace to clone, pull from and push to that repository.

Anyone forking this workspace should change or remove this section before creating a Codespace:

```json
"codespaces": {
  "repositories": {
    "Bigmac010/bmo": {
      "permissions": {
        "contents": "write"
      }
    }
  }
}
```

To grant access to another repository:

```json
"codespaces": {
  "repositories": {
    "YOUR-USERNAME/YOUR-REPOSITORY": {
      "permissions": {
        "contents": "write"
      }
    }
  }
}
```

To grant access to several repositories:

```json
"codespaces": {
  "repositories": {
    "YOUR-USERNAME/REPOSITORY-ONE": {
      "permissions": {
        "contents": "write"
      }
    },
    "YOUR-USERNAME/REPOSITORY-TWO": {
      "permissions": {
        "contents": "write"
      }
    }
  }
}
```

Only request access to repositories the workspace actually needs.

Changes to repository permissions may require creating a new Codespace.

## Fish configuration

Fish is the default shell.

The configuration sets NeoVim as the default editor:

```fish
set -gx EDITOR nvim
set -gx VISUAL nvim
```

Available aliases:

```text
vim → nvim
vi  → nvim
ll  → ls -lah

gs  → git status
gd  → git diff
ga  → git add
gc  → git commit
gp  → git push
gl  → git pull
```

Example:

```fish
gs
ga .
gc -m "Add solution"
gp
```

### C++ compilation helper

Compile a single C++ file with:

```fish
cxx main.cpp
```

This is equivalent to:

```fish
g++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp -o main
```

Run the result:

```fish
./main
```

The function is intended for simple single-file programs.

For larger projects, use CMake or a build system.

## NeoVim configuration

NeoVim includes:

- absolute line numbers;
- relative line numbers;
- four-space indentation;
- smart case-sensitive searching;
- mouse support;
- lazy.nvim;
- VimTeX;
- latexmk integration.

## LaTeX workflow

Create or open a LaTeX file:

```fish
nvim proof.tex
```

Start continuous compilation with:

```vim
:VimtexCompile
```

The VimTeX shortcut is also:

```text
\ll
```

Save changes with:

```vim
:w
```

While continuous compilation is running, the PDF updates after the source file is saved.

Open the generated PDF in VS Code's internal PDF viewer.

A typical layout is:

```text
NeoVim editing proof.tex
+
VS Code displaying proof.pdf
```

### Manual compilation

Compile once:

```fish
latexmk -pdf proof.tex
```

Continuously recompile:

```fish
latexmk -pdf -pvc proof.tex
```

Clean temporary files:

```fish
latexmk -c proof.tex
```

This normally keeps the source and final PDF while removing temporary compilation files.

## Evan Chen's LaTeX style

The workspace includes:

```text
dotfiles/texmf/tex/latex/evan/evan.sty
```

`install.sh` links it into:

```text
~/texmf/tex/latex/evan/evan.sty
```

Confirm that TeX can find it:

```fish
kpsewhich evan.sty
```

Use it in a document with:

```latex
\documentclass[11pt]{scrartcl}
\usepackage[sexy]{evan}
```

Example:

```latex
\documentclass[11pt]{scrartcl}
\usepackage[sexy]{evan}

\title{Olympiad Notes}
\author{Your Name}
\date{}

\begin{document}

\maketitle

\begin{problem}
Prove that for every real number \(x\),
\[
x^2 \ge 0.
\]
\end{problem}

\begin{proof}
The square of every real number is nonnegative.
\end{proof}

\end{document}
```

`evan.sty` is written by Evan Chen and could be downloaded from [here](https://github.com/vEnhance/dotfiles/blob/main/texmf/tex/latex/evan/evan.sty). 

See more tips and advice about LaTeX and his LaTeX style by Evan Chen [here](https://web.evanchen.cc/faq-latex.html) 
and Evan's LaTeX guide [here](https://web.evanchen.cc/latex-style-guide.html). 

## LaTeX build files

LaTeX creates temporary files such as:

```text
*.aux
*.fdb_latexmk
*.fls
*.log
*.synctex.gz
*.out
*.toc
```

These are ignored by `.gitignore`.

The main files normally worth keeping are:

```text
document.tex
document.pdf
```

Tracking generated PDFs is optional and depends on the project.

To ignore PDFs as well, add this to `.gitignore`:

```gitignore
*.pdf
```

Do not add that rule when the repository is intended to publish compiled PDFs.

## Changing the installed programs

Edit:

```text
.devcontainer/Dockerfile
```

Add an Ubuntu package inside the `apt-get install` list:

```dockerfile
RUN apt-get update && apt-get install -y \
    existing-package \
    new-package \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

After changing the Dockerfile, rebuild the container.

In VS Code:

```text
Ctrl + Shift + P
→ Codespaces: Rebuild Container
```

A rebuild recreates the Linux container and reinstalls the packages.

Files stored under `/workspaces` remain associated with the Codespace, but important work should still be committed and pushed before rebuilding.

## Changing NeoVim

Edit:

```text
dotfiles/.config/nvim/init.lua
```

Examples of settings that can be changed:

```lua
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.wrap = false
```

To disable relative line numbers:

```lua
vim.opt.relativenumber = false
```

To use two-space indentation:

```lua
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2
```

Add another lazy.nvim plugin inside:

```lua
require("lazy").setup({
    {
        "lervag/vimtex",
        lazy = false
    },

    {
        "AUTHOR/PLUGIN"
    }
})
```

After changing the configuration, restart NeoVim.

## Changing Fish

Edit:

```text
dotfiles/.config/fish/config.fish
```

Add an alias:

```fish
alias name='command'
```

Example:

```fish
alias cls='clear'
```

Add a function:

```fish
function hello
    echo "Hello"
end
```

Apply changes immediately:

```fish
source ~/.config/fish/config.fish
```

## Changing the default shell

Fish is made the default shell in two places.

In the Dockerfile:

```dockerfile
RUN usermod --shell /usr/bin/fish vscode
```

In `install.sh`:

```bash
sudo chsh "$(id -un)" --shell /usr/bin/fish
```

VS Code also uses Fish as its default terminal through `devcontainer.json`.

To return to Bash:

1. Remove or change the Fish shell lines.
2. Set the VS Code terminal profile to Bash.
3. Rebuild the container.

## Changing VS Code extensions

Edit:

```text
.devcontainer/devcontainer.json
```

The current extensions are:

```json
"extensions": [
  "ms-vscode.cpptools",
  "ms-python.python",
  "james-yu.latex-workshop"
]
```

Add another extension ID:

```json
"extensions": [
  "ms-vscode.cpptools",
  "ms-python.python",
  "james-yu.latex-workshop",
  "PUBLISHER.EXTENSION"
]
```

Rebuild or recreate the Codespace after changing extensions.

## Changing LaTeX packages

The Dockerfile installs selected TeX Live collections rather than `texlive-full`.

This keeps the image smaller while supporting most mathematical documents.

Current collections include:

```text
texlive-latex-base
texlive-latex-recommended
texlive-latex-extra
texlive-fonts-recommended
texlive-pictures
texlive-science
texlive-xetex
texlive-luatex
```

When LaTeX reports a missing package, identify the Ubuntu TeX Live collection containing it and add that collection to the Dockerfile.

Installing `texlive-full` is possible, but it significantly increases build time and storage usage.

## Changing the NeoVim version

The Dockerfile downloads NeoVim from:

```text
https://github.com/neovim/neovim/releases/download/stable/
```

This means rebuilding later may install a newer stable NeoVim release.

For a fixed version, replace `stable` with a specific release tag.

Example structure:

```dockerfile
https://github.com/neovim/neovim/releases/download/vX.Y.Z/
```

Pinning a version improves reproducibility.

Using `stable` keeps the workspace current.

## Applying setup changes without rebuilding

Changes to `install.sh` or the dotfiles can often be applied with:

```fish
cd /workspaces/linux-workspace
bash install.sh
```

Changes to the Dockerfile require a rebuild because they affect installed system packages.

## Verifying the environment

Run:

```fish
echo $SHELL
fish --version
nvim --version
git --version
g++ --version
python --version
latexmk --version
pdflatex --version
xelatex --version
lualatex --version
asy --version
kpsewhich evan.sty
```

## Troubleshooting

### `VimtexCompile` is not recognised

Check the NeoVim version:

```fish
nvim --version | head -n 1
```

Restart NeoVim after plugins have been installed.

Confirm VimTeX is installed:

```vim
:Lazy
```

Confirm the file type:

```vim
:set filetype?
```

It should report:

```text
filetype=tex
```

### TeX cannot find `evan.sty`

Run:

```fish
kpsewhich evan.sty
```

If nothing appears, reapply the setup:

```fish
cd /workspaces/linux-workspace
bash install.sh
```

Then check again.


### The build appears frozen

TeX Live and graphical packages can take time to configure.

Check the Codespace status from the GitHub Codespaces page.

Before stopping or rebuilding, commit and push important repository changes.

## Suggested changes for forks

Most users may need/want to change:

1. Repository access in `devcontainer.json`.
2. GitHub username and repository names.
3. Fish aliases.
4. NeoVim options and plugins.
5. VS Code extensions.
6. TeX Live package collections.
7. Whether `evan.sty` is included.
8. Whether Zathura and xfce4-terminal are installed.
9. Whether NeoVim tracks the latest stable release or a pinned version.
10. Whether generated PDFs are tracked by Git.

## Licence

The original workspace configuration may be reused and modified according to the licence selected for this repository.

`evan.sty` remains separately copyrighted by Evan Chen and is distributed under the Boost Software License 1.0 contained within that file.
