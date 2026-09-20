#!/usr/bin/env python3
"""Incremental LaTeX build: publish only successful PDFs beside the source."""
import argparse
import contextlib
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


@contextlib.contextmanager
def build_lock(path):
    """Serialize editor/manual builds sharing a document's auxiliary files."""
    with path.open('a+b') as stream:
        if os.name == 'nt':
            import msvcrt
            if path.stat().st_size == 0:
                stream.write(b'0')
                stream.flush()
            while True:
                try:
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    time.sleep(0.2)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == 'nt':
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def preamble_key(source):
    content = source.read_text(encoding='utf-8-sig')
    marker = re.search(r'(?m)^[ \t]*\\begin\{document\}', content)
    if not marker:
        return None
    context = {
        'source': str(source.resolve()),
        'date': str(datetime.date.today()),
        'compiler': shutil.which('pdftex'),
        'search': {key: os.environ.get(key, '') for key in
                   ('TEXINPUTS', 'TEXMFHOME', 'TEXMFLOCAL', 'TEXFORMATS')},
    }
    return hashlib.sha256((content[:marker.start()] + json.dumps(context, sort_keys=True)).encode()).hexdigest()


def prepare_cache(source, folder):
    key = preamble_key(source)
    if key is None:
        return None
    fmt = folder / (source.stem + '.fmt')
    metadata = folder / (source.stem + '.fast-preview.json')
    try:
        state = json.loads(metadata.read_text())
        if fmt.is_file() and state['key'] == key and all(
            digest(Path(p)) == value for p, value in state['inputs'].items()
        ):
            return fmt
    except (OSError, ValueError, KeyError):
        pass
    print('Refreshing preamble cache (ordinary text edits reuse it).', flush=True)
    command = ['pdftex', '-ini', '-recorder', '-interaction=nonstopmode',
               '-halt-on-error', '-output-directory=build', '-jobname=' + source.stem,
               '&pdflatex', 'mylatexformat.ltx', '"' + source.name + '"']
    cache_log = folder / (source.stem + '.cache-build.log')
    with cache_log.open('w', encoding='utf-8') as log:
        result = subprocess.run(command, cwd=source.parent, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode or not fmt.is_file():
        metadata.unlink(missing_ok=True)
        print(f'Preamble cache unavailable; using normal pdfLaTeX. See {cache_log}.')
        print(cache_log.read_text(encoding='utf-8', errors='replace')[-4000:])
        return None
    dependencies = {folder / (source.stem + '.pre'), Path(__file__).resolve()}
    recorder = folder / (source.stem + '.fls')
    for line in recorder.read_text(encoding='utf-8', errors='replace').splitlines():
        if line.startswith('INPUT '):
            path = Path(line[6:])
            path = path if path.is_absolute() else source.parent / path
            if path.resolve() != source:
                dependencies.add(path.resolve())
    compiler = shutil.which('pdftex')
    if compiler:
        dependencies.add(Path(compiler).resolve())
    metadata.write_text(json.dumps({'key': key, 'inputs': {
        str(p): digest(p) for p in dependencies
    }}, indent=2), encoding='utf-8')
    return fmt


def build(source, engine='pdflatex', cache=True):
    source = Path(source).resolve()
    if source.suffix != '.tex' or not source.is_file():
        raise ValueError('Choose an existing main .tex file.')
    folder = source.parent / 'build'
    folder.mkdir(exist_ok=True)
    config = Path(__file__).with_name('latexmkrc').resolve()
    started = time.monotonic()
    with build_lock(folder / (source.stem + '.lock')):
        env = os.environ.copy()
        env.pop('LW_FORMAT', None)
        if cache and engine == 'pdflatex':
            fmt = prepare_cache(source, folder)
            if fmt:
                env['LW_FORMAT'] = str(fmt)
        mode = '-pdf' if engine == 'pdflatex' else '-lualatex'
        command = ['latexmk', '-norc', '-r', str(config), mode, '-outdir=build',
                   '-jobname=' + source.stem,
                   '-synctex=1', '-interaction=nonstopmode', '-halt-on-error',
                   '-file-line-error', source.name]
        result = subprocess.run(command, cwd=source.parent, env=env)
        if result.returncode:
            return result.returncode
        pdf = folder / (source.stem + '.pdf')
        log = (folder / (source.stem + '.log')).read_text(encoding='utf-8', errors='replace')
        if re.search(r'Package asymptote Warning: file .*?not found', log, re.S):
            print('Asymptote figure missing; final PDF was not replaced.', file=sys.stderr)
            return 1
        if not pdf.is_file():
            raise RuntimeError('Build reported success but produced no PDF.')
        final = source.with_suffix('.pdf')
        if digest(pdf) != digest(final):
            temporary = folder / (source.stem + '.publish.pdf')
            shutil.copyfile(pdf, temporary)
            os.replace(temporary, final)
    print(f'Updated {final.name} in {time.monotonic() - started:.1f}s.', flush=True)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('--engine', choices=['pdflatex', 'lualatex'], default='pdflatex')
    parser.add_argument('--no-cache', action='store_true')
    args = parser.parse_args()
    try:
        return build(args.source, args.engine, not args.no_cache)
    except (OSError, ValueError, RuntimeError) as error:
        print(f'Build failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
