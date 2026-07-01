# Installing the Driftline CLI

The Driftline CLI lets you manage monitors, check incidents, and view status from your terminal. It works on macOS, Linux, and Windows, and needs Python 3.9 or newer.

## Install

Install from PyPI:

```bash
pip install driftline-cli
```

This puts the `driftline` command on your PATH. Verify the install:

```bash
driftline --version
```

Note: `driftline-cli` is the command-line tool. If you want the Python SDK for use in your own code, that's a separate package — `pip install driftline`. See 05-api-reference.md for the API and 10-python-sdk.md for the SDK.

## Log in

Authenticate the CLI with:

```bash
driftline login
```

This opens your browser to approve the device, then stores a token locally. If you're on a headless machine, you can paste an API key instead when prompted — create one under **Settings -> API Keys**, as described in 03-authentication.md.

## Configuration file

The CLI stores its settings in `~/.driftline/config.toml`. A typical file looks like:

```toml
[auth]
api_key = "dl_live_xxxx"

[defaults]
output = "table"
```

You can edit this file directly or manage it via `driftline login`. Keep it out of version control — it contains your credentials.

## Verify everything works

Run:

```bash
driftline status
```

You should see your organization name and a summary of monitors that are UP or DOWN. Then try listing your monitors:

```bash
driftline monitors list
```

Other commands you'll use often: `driftline monitors create`, `driftline monitors pause`, and `driftline incidents list`. Each supports `--help` for flags.

## Next steps

Create your first monitor from the dashboard or CLI (01-getting-started.md), then set up API keys for automation (03-authentication.md). If a command fails with a 429 error, you've hit your plan's rate limit — 30 requests/min on Free, 120/min on Team and Business.
