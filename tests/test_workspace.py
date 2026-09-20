import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lw', ROOT / 'tools/lw.py')
lw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lw)
build_spec = importlib.util.spec_from_file_location('builder', ROOT / '.latex/build.py')
builder = importlib.util.module_from_spec(build_spec)
build_spec.loader.exec_module(builder)


class WorkspaceTests(unittest.TestCase):
    def test_init_preserves_source_and_remote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'notes.tex').write_text('existing source')
            (root / '.git').mkdir()
            (root / '.git/config').write_text('unchanged remote')
            lw.initialise(root, 'notes')
            self.assertEqual((root / 'notes.tex').read_text(), 'existing source')
            self.assertEqual((root / '.git/config').read_text(), 'unchanged remote')
            self.assertTrue((root / '.latex/build.py').is_file())
            self.assertNotIn('*.pdf', (root / '.gitignore').read_text())

    def test_existing_settings_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '.vscode').mkdir()
            (root / '.vscode/settings.json').write_text('{"custom":true}')
            with self.assertRaises(ValueError):
                lw.initialise(root)
            self.assertFalse((root / '.latex').exists())

    def test_name_cannot_escape_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                lw.initialise(directory, '../escape')

    def test_cache_key_tracks_search_path_but_not_body(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'main.tex'
            source.write_text('\\documentclass{article}\n\\begin{document}\nBefore')
            first = builder.preamble_key(source)
            source.write_text('\\documentclass{article}\n\\begin{document}\nAfter')
            self.assertEqual(first, builder.preamble_key(source))
            with mock.patch.dict('os.environ', {'TEXINPUTS': '/another/style/location:'}):
                self.assertNotEqual(first, builder.preamble_key(source))


if __name__ == '__main__':
    unittest.main()
