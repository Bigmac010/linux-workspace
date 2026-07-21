FROM mcr.microsoft.com/devcontainers/base:ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    neovim \
    fish \
    build-essential \
    cmake \
    gdb \
    git \
    python3 \
    python-is-python3 \
    python3-pip \
    python3-venv \
    latexmk \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-pictures \
    texlive-science \
    texlive-xetex \
    texlive-luatex \
    asymptote \
    zathura \
    zathura-pdf-poppler \
    xfce4-terminal \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN usermod --shell /usr/bin/fish vscode

ENV DEBIAN_FRONTEND=
