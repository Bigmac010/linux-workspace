# Third-party components

`dotfiles/texmf/tex/latex/evan/evan.sty` is an unmodified copy of Evan Chen's style,
from commit `78c04424972d63e1eed6d5f4263d9f4f326d56d2`:
https://github.com/vEnhance/dotfiles/blob/78c04424972d63e1eed6d5f4263d9f4f326d56d2/texmf/tex/latex/evan/evan.sty

Its Boost Software License and copyright are retained in the file. Attribution
to upstream authors is intentional and is not the workspace user's identity.
Set `\author{...}` in each document; do not customise the vendored style.

The Dockerfile records the TeX image digest, Asymptote source commit and checksum,
and optional VimTeX commit. Upstream projects retain their own licences:

- TeX image: https://github.com/xu-cheng/latex-docker
- Asymptote: https://github.com/vectorgraphics/asymptote
- VimTeX: https://github.com/lervag/vimtex

OS packages still come from Debian repositories. The base image and the named
source revisions are pinned; this is not a fully hermetic OS package snapshot.
