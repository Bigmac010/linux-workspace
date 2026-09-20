#!/usr/bin/env python3
"""Create portable LaTeX projects. Never commits, changes remotes or pushes."""
import argparse
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def initialise(destination, name='main'):
    destination = Path(destination).resolve()
    if Path(name).name != name or not name or name.startswith('.'):
        raise ValueError('Use a simple document name, without directories or an extension.')
    source_name = name if name.endswith('.tex') else name + '.tex'
    copies = {p: ROOT / p for p in ('.latex/build.py', '.latex/latexmkrc',
               '.latexmkrc', '.vscode/settings.json', '.vscode/extensions.json')}
    conflicts = [p for p in copies if (destination / p).exists()]
    if conflicts:
        raise ValueError('Existing configuration left unchanged: ' + ', '.join(conflicts))
    # Validate before making any changes. Existing source and Git remotes are preserved.
    destination.mkdir(parents=True, exist_ok=True)
    for relative, origin in copies.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target)
    source = destination / source_name
    if not source.exists():
        shutil.copyfile(ROOT / 'main.tex', source)
    ignore = destination / '.gitignore'
    existing = ignore.read_text() if ignore.exists() else ''
    rules = (ROOT / '.gitignore').read_text()
    with ignore.open('a', encoding='utf-8') as file:
        file.write(('\n' if existing and not existing.endswith('\n') else '') + rules)
    print(f'Open {destination} in VS Code, then edit {source.name}.')
    print('No repository was created or modified remotely. Review git status before committing.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init', help='Set up a new folder or an existing notes repository')
    init.add_argument('directory')
    init.add_argument('--name', default='main')
    compile_command = commands.add_parser('build', help='Build an existing main TeX document')
    compile_command.add_argument('source')
    compile_command.add_argument('--engine', choices=['pdflatex', 'lualatex'], default='pdflatex')
    compile_command.add_argument('--no-cache', action='store_true')
    commands.add_parser('doctor', help='Check the required programs and Evan style')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            initialise(args.directory, args.name)
            return 0
        if args.command == 'doctor':
            missing = [p for p in ['python3','latexmk','pdftex','pdflatex','lualatex','asy','gs','git'] if not shutil.which(p)]
            for program in missing:
                print('Missing:', program)
            if missing:
                return 1
            for command in [['pdflatex','--version'],['asy','--version'],['kpsewhich','evan.sty']]:
                result = subprocess.run(command, capture_output=True, text=True)
                print((result.stdout or result.stderr).splitlines()[0] if result.stdout or result.stderr else 'Not found')
                if result.returncode:
                    return 1
            return 0
        spec = importlib.util.spec_from_file_location('workspace_build', ROOT / '.latex/build.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build(args.source, args.engine, not args.no_cache)
    except (OSError, ValueError, RuntimeError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
