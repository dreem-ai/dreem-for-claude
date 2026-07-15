# CLAUDE.md - dreem-for-claude

## Secret scanning before every push

This repo enforces a local secret scan before any `git push`, via a `pre-push` git hook backed by [gitleaks](https://github.com/gitleaks/gitleaks) (free, open source - no paid GitHub Advanced Security required).

**One-time setup per clone:**

```bash
brew install gitleaks          # if not already installed
git config core.hooksPath .githooks
```

Once enabled, every `push` scans the commits being pushed for likely secrets (API keys, tokens, private keys, etc.) and blocks the push if gitleaks finds one.

**Rules for any session (human or Claude) working in this repo:**

- Never push with `--no-verify` to skip this check. If the hook blocks a push, treat it as a real finding: investigate first, then either remove the secret and amend, or - only if it's a genuine false positive - add a scoped rule to a `.gitleaks.toml` at the repo root (do not create a blanket allowlist).
- If gitleaks isn't installed, the hook skips the scan and says so loudly rather than failing silently - install it before assuming pushes are protected.
- This covers secrets, not dependency vulnerabilities - the repo currently has no dependency manifest (the packaging script is stdlib-only Python), so there's nothing for a vulnerability scanner to check yet. If that changes (a `requirements.txt` or similar is added), extend `.githooks/pre-push` with a vuln-scan step at that point.
