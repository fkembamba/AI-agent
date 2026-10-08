# Uploading This Repository to GitHub

## Recommended: Git command line

1. Extract the ZIP.
2. Open a terminal inside the extracted `ai-agent-resilience-complete-repo` directory.
3. Create an empty **private** GitHub repository.
4. Run:

```bash
git init
git add .
git commit -m "Initial AI Agent Resilience project baseline"
git branch -M main
git remote add origin https://github.com/YOUR-USER-OR-ORG/YOUR-REPO.git
git push -u origin main
```

This is preferred because it preserves the hidden `.github/` directory and all nested files.

## Why the folder may look like it has only a few files

Some file browsers hide directories beginning with a dot. The `.github/` directory is therefore often invisible unless hidden files are enabled.

The full repository also contains `network/`, `automation/`, `platform/`, `restore/`, `experiments/`, and `docs/`.

## Verify after push

On GitHub you should see:

- `README.md`
- `docs/`
- `network/`
- `restore/`
- `experiments/`
- `platform/`
- `automation/`
- `.github/`

Then open **Actions**. The `Validate cyber-range configuration` workflow should be present.

Do not add actual credentials or secrets to the repository.
