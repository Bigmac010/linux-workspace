"""Real compiler tests; run inside the container or with the documented tools installed."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / '.latex/build.py'
SOURCE = r'''\documentclass{scrartcl}
\usepackage[sexy,noauthor]{evan}
\title{Cache test}
\author{}
\date{}
\begin{document}
\maketitle
\begin{tcolorbox}[purplebox,title={Test}]Original text.\end{tcolorbox}
\begin{asy}
size(3cm);
draw(unitcircle);
\end{asy}
\begin{asy}
size(3cm);
draw((0,0)--(1,0)--(0,1)--cycle);
\end{asy}
\end{document}
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source, *options, success=True):
    result = subprocess.run([sys.executable, str(BUILD), *options, str(source)],
                            capture_output=True, text=True, errors='replace')
    if (result.returncode == 0) != success:
        print(result.stdout, result.stderr)
        raise AssertionError(f'Unexpected result: {result.returncode}')
    return result.stdout


with tempfile.TemporaryDirectory(prefix='latex workspace ') as directory:
    root = Path(directory)
    # Spaces in the directory and filename exercise all subprocess boundaries.
    source = root / 'sample notes.tex'
    source.write_text(SOURCE, encoding='utf-8')
    run(source)
    pdf = source.with_suffix('.pdf')
    assert pdf.exists()
    assert sorted(p.name for p in root.iterdir()) == ['build','sample notes.pdf','sample notes.tex']
    figures = [root / 'build' / f'sample notes-{i}.pdf' for i in (1,2)]
    assert all(p.exists() for p in figures)
    # Settle the generated Asymptote preamble, then ensure ordinary edits reuse the cache.
    run(source)
    fmt = root / 'build/sample notes.fmt'
    assert fmt.exists(), (root / 'build/sample notes.cache-build.log').read_text(errors='replace')
    stamp = fmt.stat().st_mtime_ns
    figure_times = [p.stat().st_mtime_ns for p in figures]
    source.write_text(SOURCE.replace('Original text.', 'Edited text.'), encoding='utf-8')
    run(source)
    assert fmt.stat().st_mtime_ns == stamp, 'Text edit rebuilt the preamble'
    assert figure_times == [p.stat().st_mtime_ns for p in figures], 'Text edit rebuilt diagrams'
    source.write_text(SOURCE.replace('draw(unitcircle);', 'draw(scale(1.1)*unitcircle);'), encoding='utf-8')
    run(source)
    assert figures[0].stat().st_mtime_ns != figure_times[0]
    assert figures[1].stat().st_mtime_ns == figure_times[1]
    source.write_text(SOURCE.replace('Cache test', 'Changed title'), encoding='utf-8')
    run(source)
    assert fmt.stat().st_mtime_ns != stamp, 'Preamble change was not picked up'
    good_pdf = sha(pdf)
    source.write_text(SOURCE.replace('Original text.', r'\undefinedWorkspaceCommand'), encoding='utf-8')
    run(source, success=False)
    assert sha(pdf) == good_pdf, 'Failed build replaced the last good PDF'
    source.write_text(SOURCE.replace('draw(unitcircle);', 'notARealAsymptoteFunction();'), encoding='utf-8')
    run(source, success=False)
    assert sha(pdf) == good_pdf, 'Failed diagram replaced the last good PDF'
    source.write_text(SOURCE, encoding='utf-8')
    run(source, '--no-cache')
    # A missing published PDF is restored even when latexmk has nothing to rebuild.
    pdf.unlink()
    run(source, '--no-cache')
    assert sha(pdf) == sha(root / 'build/sample notes.pdf')
    source.write_text(SOURCE.replace('Original text.', 'Unicode text: café, 中文.'), encoding='utf-8')
    run(source, '--engine', 'lualatex')
    assert pdf.is_file()
    assert 'Missing character:' not in (root / 'build/sample notes.log').read_text(encoding='utf-8', errors='replace')
    print('PASS: cold build, cache reuse, text edit, selective diagrams, title refresh,')
    print('      error preservation, republishing, spaces in paths, and LuaLaTeX.')
