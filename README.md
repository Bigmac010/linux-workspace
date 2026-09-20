# Linux Workspace

A public, reusable workspace for mathematical writing, C/C++ and Python.
Use VS Code in GitHub Codespaces or a local Dev Container. Edit LaTeX, preview
automatically, and keep your source and final PDF in a repository you own.

No account name, email, token, SSH key or destination repository is configured.
The setup does not create commits, set Git identity, change remotes, or push.
Third-party author credits and licences are preserved.

## Start with your own copy

**Recommended: Use this template → Create a new repository.** Choose your own
account, repository name and visibility. A template copy starts a new Git
history; it is different from a fork.

Then open **Code → Codespaces → Create codespace on main** in your copy.
The first container build is large and may take several minutes. Codespaces
usage is subject to your account's allowance and billing settings.

If the template button is unavailable, fork the repository, or clone a copy you
own. A fork is useful when you want to contribute improvements upstream.
See [GitHub's template guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

For a local Linux-backed environment, install Docker and VS Code's Dev Containers
extension, clone your copy, then choose **Dev Containers: Reopen in Container**.
The pinned TeX image targets Linux amd64; other architectures need emulation or
a separately tested image. The helper scripts do not require Codespaces.

## Write and preview

1. Open `main.tex`.
2. Press **Ctrl+Alt+B** for the first build.
3. Press **Ctrl+Alt+V** to open the PDF on the right.
4. Edit. After 0.5 seconds without typing, VS Code saves and starts a build.

```text
my-notes/
├── main.tex               edit this
├── main.pdf               final PDF to read, commit or share
├── build/                 diagrams, caches, logs and SyncTeX; ignored by Git
├── .latex/                portable build helpers
├── .vscode/               editor recipes
└── .latexmkrc              direct latexmk compatibility
```

The preview uses the PDF in `build/` so SyncTeX stays beside it. A successful
build updates the final PDF next to the source. If a build fails, that final PDF
remains the last successful version: check the build error before sharing.

The cached pdfLaTeX recipe precompiles the preamble and reuses unchanged diagrams.
There is no promised five-second time: machine size, document length, diagrams
and extra reference passes all matter. First builds and preamble changes are
slower. The cache refreshes when the preamble, loaded files or compiler change,
and each new day. It is never deleted merely because the editor closes.

**Build with recipe** also offers normal pdfLaTeX and LuaLaTeX. LuaLaTeX supports
the installed Unicode fonts and bypasses the preamble cache. pdfLaTeX has
different font handling and cannot typeset arbitrary Unicode/colour emoji.
Use a portable symbol such as `\ensuremath{\rightarrow}` in pdfLaTeX sources.
Automatic builds always use the first recipe, unless you change
`latex-workshop.latex.recipe.default`.

CLI equivalents:

```sh
lw build main.tex
lw build --no-cache main.tex
lw build --engine lualatex main.tex
lw doctor
```

A copied project includes its builder and can also run
`python3 .latex/build.py main.tex` when the documented tools and Evan style are
installed. Newer source code is not fetched during compilation.

## Put notes in a different repository

The workspace supplies the tools. Your notes repository stores your work.
Keep repositories as siblings, not nested Git repositories.

### Existing notes repository

In a terminal, after granting access as explained below:

```sh
cd /workspaces
gh repo clone OWNER/NOTES-REPOSITORY
lw init /workspaces/NOTES-REPOSITORY --name notes
```

Replace `OWNER/NOTES-REPOSITORY` with the repository you actually own.
`lw init` preserves an existing `notes.tex`, adds portable build/editor
configuration, and ignores generated files. It refuses to overwrite existing
configuration: merge those settings deliberately instead.

Use **File → Add Folder to Workspace** to add the notes repository to the
current VS Code window. This keeps the existing container connection and tools.

Build, review the changes, then commit explicit files:

```sh
cd /workspaces/NOTES-REPOSITORY
lw build notes.tex
git status
git add notes.tex notes.pdf .gitignore .latexmkrc .latex .vscode
git diff --cached --stat
git commit -m "Add mathematical notes and PDF"
git push
```

For later edits, stage `notes.tex` and `notes.pdf`, plus any source figures,
bibliographies or included TeX files you intentionally changed. The main source
and final PDF are tracked; `build/` is not. We do not ignore every `*.pdf` or
`*.asy`, because some are intentional source assets.

If Git asks for an author, configure your **own** identity in that notes
repository. You can use the noreply address from your GitHub email settings.
Do not copy another person's name or email from instructions.

### New notes repository

Create a repository under your own account on GitHub, initialise it with a README,
then follow the clone steps above. Alternatively use
`gh repo create OWNER/NAME --private --clone` (choose `--public` only if intended)
and initialise its folder with `lw init`.

### Codespaces permissions

A Codespace's built-in token normally covers its starting repository, not all
repositories in the account. Cloning a public repository does not imply permission
to push to it.

In **your own workspace copy**, request only the destination repositories you
need by adding this under `customizations` in `devcontainer.json`:

```json
"codespaces": {
  "repositories": {
    "YOUR-ACCOUNT/YOUR-NOTES": {
      "permissions": { "contents": "write" }
    }
  }
}
```

Keep the existing `vscode` section beside it. GitHub restricts these references
to repositories owned by the same account or organisation as the workspace.
Commit your configuration and create a **new Codespace**, then authorise it.
Rebuilding an existing Codespace does not grant the new permissions.
For other authentication arrangements follow
[GitHub's repository-access guide](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-repository-access-for-your-codespaces).
Never commit tokens or private keys. No extra repository access is requested by
this public template.

## What is installed

- TeX Live 2026, from a pinned container snapshot.
- Asymptote 3.15 built from a checksum-verified source revision, plus Ghostscript.
- A pinned, unmodified modern `evan.sty`, using `tcolorbox` and `keytheorems`.
- CMU, Inconsolata and Noto fonts for LuaLaTeX.
- Python, C/C++ tools, CMake, GDB, Git, GitHub CLI, Fish and Neovim.
- LaTeX Workshop, VS Code Python and C/C++ extensions.

The supported diagram workflow is 2D mathematical/geometry PDF output. The
container includes OpenGL libraries required to build this Asymptote release,
but supplies no graphical desktop or Vulkan renderer. Interactive GPU 3D
rendering is outside the tested workflow.

See [THIRD_PARTY.md](THIRD_PARTY.md) for versions and upstream attribution.
OS packages are not a fully frozen snapshot. Run the checks after updating them.

## Evan Chen documents

Use:

```latex
\documentclass[11pt]{scrartcl}
\usepackage[sexy,noauthor]{evan}
\title{My notes}
\author{}
```

Set your author in the document, not in `evan.sty`. Older documents using
`mdframed[style=mdpurplebox,frametitle=...]` need conversion to
`tcolorbox[purplebox,title=...]`, or their original compatible style version.
Downloading a solution does not guarantee it matches every historical version
of Evan's style. The example and integration tests exercise the modern syntax
and Asymptote geometry support.

## Optional terminal editor

VS Code is the default. To install the supplied Fish/Neovim preferences:

```sh
bash install.sh --dotfiles
```

Existing configurations are backed up under
`~/.local/state/latex-workspace/backups/`. The installer does not set your Git
name/email, credentials, remote, or global Git editor.

In Neovim, TeX edits save after 0.5 seconds and use the same builder.
Use `:LatexBuild` for a manual build with visible errors. VimTeX supplies editing
and navigation features; it does not start a second compiler. Do not edit the
same document simultaneously in both editors. Use VS Code for PDF viewing;
there is no graphical Linux desktop configured.

## Maintenance and checks

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/integration.py
```

GitHub Actions builds the actual container and tests cold builds, cache reuse,
text edits, selective diagram rebuilds, preamble changes, failed-build PDF
preservation, spaces in paths, republishing and LuaLaTeX.

The original workspace's previous Git commits are not erased by a configuration
change. GitHub still displays the repository owner and public commit/PR history.
A template copy starts a new history; cloning/forking retains history.

## Licence

Original workspace code is MIT licensed. Vendored third-party files retain
their own licences and attribution. See [LICENSE](LICENSE) and
[THIRD_PARTY.md](THIRD_PARTY.md).
