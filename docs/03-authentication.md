# Authentication

Every request to the Driftline API is authenticated with an API key. This page covers key types, how to create and rotate them, and how to keep them safe.

## Key types

Driftline issues two kinds of keys:

- **Live keys** start with `dl_live_` and act on your real monitors and incidents.
- **Test keys** start with `dl_test_` and hit a sandbox — nothing you do with a test key affects production data or sends alerts.

Use test keys in CI and local development, and live keys only in production.

## Creating a key

Go to **Settings -> API Keys** in the dashboard, click **Create key**, give it a descriptive name (e.g. "deploy-script"), and copy the value. The full key is shown once; after that only a prefix is visible.

## Using a key

Send the key in the `Authorization` header as a Bearer token:

```bash
curl https://api.driftline.example/v1/monitors \
  -H "Authorization: Bearer dl_live_xxxx"
```

The Python SDK takes it as a constructor argument:

```python
from driftline import Driftline

client = Driftline(api_key="dl_live_xxxx")
```

All endpoints live under `https://api.driftline.example/v1` — see 05-api-reference.md for the full list.

## Rotating keys

To rotate, open **Settings -> API Keys** and click **Rotate** next to the key. Driftline generates a new value immediately, and the old key stays valid for 24 hours so your deployments don't break mid-rotation. Update your services within that grace window, then the old key is revoked automatically.

## Keep keys out of your repo

Never commit API keys to version control — not even test keys. Load them from environment variables or a secrets manager instead:

```bash
export DRIFTLINE_API_KEY=dl_live_xxxx
```

If a key leaks, rotate it right away. The CLI stores its key in `~/.driftline/config.toml` (see 02-installation.md), which should also stay untracked. Requests with a missing or invalid key return `401 Unauthorized`.
