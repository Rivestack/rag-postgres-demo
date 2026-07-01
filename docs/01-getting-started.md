# Getting Started with Driftline

Driftline gives your team uptime monitoring and hosted status pages in a few minutes. This guide walks you through signing up, creating your first monitor, and understanding what UP and DOWN actually mean.

## Sign up

Head to the Driftline signup page and create an account with your work email, or sign in with Google. Every new organization starts on the Free plan: 5 monitors with checks every 5 minutes, no credit card required. If you need more monitors or faster checks, the Team plan ($29/mo) runs 30-second checks and the Business plan ($99/mo) runs 10-second checks — see 04-billing.md for the full breakdown.

## Create your first monitor

From the dashboard, click **New Monitor** and enter:

- **URL** — the endpoint to check, e.g. `https://app.example.com/health`
- **Interval** — depends on your plan: 5 minutes on Free, down to 30 seconds on Team and 10 seconds on Business
- **Alert channels** — email is on by default; you can add Slack or webhooks later

Prefer the terminal? The CLI can do the same thing:

```bash
driftline monitors create --url https://app.example.com/health --name "App health"
```

See 02-installation.md for setting up the CLI.

## What UP and DOWN mean

Driftline runs checks from 12 regions around the world. A single failed check from one region never triggers an alert — that's usually just local network noise. A monitor is marked **DOWN** only when 2 or more regions agree the endpoint is failing (quorum). This keeps false positives to a minimum, so when Driftline pages you, it's real.

When a monitor goes DOWN, an incident is opened automatically and moves through the lifecycle: investigating, identified, monitoring, resolved.

## Where to go next

- 02-installation.md — install and log in with the CLI
- 03-authentication.md — create API keys for scripts and integrations
- 05-api-reference.md — manage monitors and incidents over the REST API

Questions? Email support@driftline.example.
