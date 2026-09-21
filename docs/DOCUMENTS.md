# Documents and GitHub

Create one folder per document inside the open workspace, for example `bmo2023solution/main.tex`. After a successful build, `main.pdf` appears beside it. Shared generated files live in `build/bmo2023solution/main/`. Root `main.tex` uses `build/main/`. Keep the workspace root open in VS Code so its settings apply. Open a complete document containing `\documentclass`, then save or run Build LaTeX project. Included chapter files belong to their parent document.

The shared `build/` folder is ignored by Git. Its caches speed up subsequent builds; do not clear them after every save. Previous generated files and diagnostic backups were preserved under `build/previous-build/`. Support configuration is hidden in Explorer using `files.exclude`, but remains in the repository. Open workspace settings to show it again.

## Which repository receives my work?

Saving changes only the Codespace files. Commit records changes locally; push sends commits to the configured remote. Use `git remote -v` to inspect that destination. A Codespace opened with Code > Codespaces on an existing repository is attached to that repository (or a fork). Use this template > Open in a codespace creates an unpublished workspace that you can publish as a new repository. Use this template > Create a new repository creates a separate repository first.

## Add a document to an existing repository

Git pushes commits, not individual folders to arbitrary repositories. Clone the destination separately, copy the document source and PDF into the intended folder, review the diff, commit only those files, then push from that clone. Preserve any existing destination files. Do not replace the template repository remote to copy one document.

Example, starting at the template workspace root (replace the URL and destination folder):

```sh
git clone https://github.com/YOUR-USERNAME/YOUR-BMO-REPO.git ../bmo-publish
mkdir -p ../bmo-publish/bmo2023solution
cp -i bmo2023solution/main.tex bmo2023solution/main.pdf ../bmo-publish/bmo2023solution/
cd ../bmo-publish
git status
git add bmo2023solution/main.tex bmo2023solution/main.pdf
git diff --cached --stat
git commit -m "Add BMO 2023 solutions"
git push
```

Also copy any source images, bibliography or custom style files required by the document. Do not copy generated files from build/. Codespaces credentials may need separately approved access to the destination repository, even if it belongs to you. For repeated editing, put the workspace configuration in the BMO repository and open a Codespace there.
