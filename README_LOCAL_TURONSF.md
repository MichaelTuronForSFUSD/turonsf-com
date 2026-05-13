# Local turonsf.com workspace

Run from this folder only:

```bash
./TURONSF_PATH_GUARD.sh
bash 01_bootstrap_hugo_from_overlay.sh
bash 02_verify_turonsf_build.sh
```

After Codex edits, rerun:

```bash
./02_verify_turonsf_build.sh
```

Live blockers remain in `hugo.toml` until the real Brevo URL and Umami website ID are supplied.
