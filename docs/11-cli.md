# Driftline CLI

The Driftline CLI lets you manage monitors and incidents from your terminal or CI pipeline. Install it with pip:

```bash
pip install driftline-cli
driftline login
```

`driftline login` prompts for an API key (see 03-authentication.md for creating one) and stores it in `~/.driftline/config.toml`. If login keeps prompting you in a loop, check 13-troubleshooting.md.

## Managing monitors

List, create, and pause monitors directly:

```bash
driftline monitors list
driftline monitors create --name "Checkout API" --url https://shop.example.com/health
driftline monitors pause mon_8f2ka
```

Pausing is handy during planned maintenance: a paused monitor runs no checks and sends no alerts. Remember that on the Free plan checks run every 5 minutes, so a newly created monitor may take a few minutes to report its first result.

## Incidents and status

```bash
driftline incidents list --state investigating
driftline status
```

`driftline incidents list` shows open incidents with their current lifecycle state (see 14-incidents.md for what each state means). `driftline status` prints a one-line summary of your org: monitors up, monitors down, and open incidents.

## Output formats

Every command accepts `--json` for machine-readable output, which is what you want in scripts:

```bash
driftline monitors list --json | jq '.[] | select(.state == "down") | .name'
```

Without `--json`, commands print a human-friendly table.

## Using the CLI in CI

In CI, skip the interactive login and set the `DRIFTLINE_API_KEY` environment variable instead; the CLI uses it when no config file is present. Use a test key (`dl_test_xxxx`) for anything that should not touch production monitors. A common pattern is pausing a monitor before a deploy and resuming it after:

```bash
driftline monitors pause mon_8f2ka
./deploy.sh
driftline monitors pause mon_8f2ka --resume
```

CLI calls count against your API rate limit — 30 requests per minute on Free, 120 on paid plans — so avoid tight polling loops in pipelines. See 12-rate-limits.md for details and batching advice.
