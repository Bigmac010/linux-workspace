# TeX Live 2026 snapshot; modern keytheorems and tcolorbox.
FROM ghcr.io/xu-cheng/texlive-debian:20260701@sha256:3bdf292b53c04ffa3ca694a5114397859bcd39b6b417c212414e1505e7fe8ec5
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo fish neovim build-essential cmake gdb git curl ca-certificates \
    python3 python3-pip python3-venv gh fontconfig ghostscript poppler-utils \
    fonts-cmu fonts-inconsolata fonts-noto-color-emoji fonts-noto-cjk \
    autoconf automake libtool pkg-config bison flex libgc-dev libreadline-dev libgsl-dev \
    libfftw3-dev libeigen3-dev libtirpc-dev libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*
ARG ASY_REV=e4f9fe80bff8b20110aefa559b81eefc7e864781
ARG ASY_SHA256=6eb3ddf0e25f582a93534e132a6d26917219730b4d763e803d35a1d662c9f54f
RUN curl -fL --retry 3 "https://codeload.github.com/vectorgraphics/asymptote/tar.gz/${ASY_REV}" -o /tmp/asy.tar.gz \
    && echo "${ASY_SHA256}  /tmp/asy.tar.gz" | sha256sum -c - \
    && mkdir /tmp/asy && tar -xzf /tmp/asy.tar.gz -C /tmp/asy --strip-components=1 \
    && cd /tmp/asy && ./autogen.sh \
    && ./configure --prefix=/usr/local --disable-gl --disable-vulkan --disable-lsp \
    && make -j2 asy asy-keywords.el && make install-asy \
    && mktexlsr && rm -rf /tmp/asy /tmp/asy.tar.gz
# Optional Neovim: pinned plugin, no first-start downloads.
RUN git clone https://github.com/lervag/vimtex.git /usr/local/share/nvim/site/pack/workspace/start/vimtex \
    && git -C /usr/local/share/nvim/site/pack/workspace/start/vimtex checkout 42dcf1699e45725bd3b366ecab2ae06f6e0f8118 \
    && rm -rf /usr/local/share/nvim/site/pack/workspace/start/vimtex/.git
RUN useradd --create-home --uid 1000 --shell /usr/bin/fish vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode
ENV PATH="/usr/local/bin:/home/vscode/.local/bin:/opt/texlive/bin:${PATH}"
USER vscode
WORKDIR /workspaces
