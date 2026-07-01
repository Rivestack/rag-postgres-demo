# Slack integration

The Slack integration posts monitor and incident updates straight into your channels, with no webhook code to maintain. If you need fully custom delivery instead, see 06-webhooks.md.

## Connect your workspace

1. Go to Settings -> Integrations -> Slack and click **Connect workspace**.
2. Approve the OAuth prompt in Slack. Driftline only requests permission to post messages and read channel names.
3. Pick a default channel — this receives alerts for any monitor without its own channel override.

Only owners and admins can connect or disconnect a workspace (see 15-teams-permissions.md for role details). One Slack workspace can be connected per org.

## Channel per monitor

Each monitor can route to its own channel. Open the monitor, choose the Alerts tab, and set **Slack channel** — for example, send `checkout-api` alerts to `#payments-oncall` while everything else goes to `#ops`. Escalation policies from 07-alerting.md still apply: if nobody acknowledges the Slack alert within the policy's window, the on-call person is notified.

## Message format

Down alerts arrive as a red attachment with the monitor name, the failing URL, which regions reported the failure, and how long the outage has lasted. Recovery messages are green and include total downtime. Incident messages carry the current lifecycle stage (investigating, identified, monitoring, or resolved) and a link to the incident on your status page (see 08-status-pages.md). Every alert message includes an **Acknowledge** button that stops escalation directly from Slack.

## Slash command

Once connected, anyone in the workspace can run:

```
/driftline status
```

This replies (visible only to the requester) with a summary: monitors up, monitors down, and any open incidents. It's the fastest way to answer "is it just me?" without leaving Slack. The same summary is available from the terminal with `driftline status` — see 11-cli.md.
