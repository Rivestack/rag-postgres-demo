# Alerting

When a monitor goes down or an incident opens, Driftline notifies your team through the channels you configure. Alerts fire only after regional quorum — at least 2 of our 12 check regions must agree a target is down — so a single flaky network path won't page anyone at 3am.

## Channels by plan

| Channel | Free | Team | Business |
|---------|------|------|----------|
| Email   | Yes  | Yes  | Yes      |
| Slack   | Yes  | Yes  | Yes      |
| Webhook | Yes  | Yes  | Yes      |
| SMS     | No   | No   | Yes      |

SMS is available on the Business plan only. Slack setup is covered in 09-integrations-slack.md, and custom webhook payloads with signature verification are documented in 06-webhooks.md.

## Alert rules

Each monitor has its own rules, edited from the monitor's Alerts tab:

- **Trigger**: alert on `monitor.down`, on `monitor.up` (recovery), or both.
- **Delay**: wait 0-30 minutes of continuous downtime before alerting, useful for targets that self-heal.
- **Recipients**: pick any mix of configured channels per monitor.

You can also manage rules from the CLI:

```bash
driftline monitors pause mon_8fk2j1   # silence checks during a maintenance window
```

Paused monitors never alert. See 11-cli.md for the full command reference.

## Escalation policies

Escalation policies make sure alerts don't die in a muted channel. A policy notifies the on-call person after N minutes if the original alert goes unacknowledged — you choose N when creating the policy (common values are 5, 10, or 15 minutes).

To set one up:

1. Go to Settings -> Escalation Policies and click **New policy**.
2. Choose the acknowledgement window (N minutes).
3. Pick the on-call user or rotation to notify when the window expires.
4. Attach the policy to one or more monitors.

Acknowledging an alert — from email, Slack, or the dashboard — stops the escalation clock. Only owners and admins can edit escalation policies; members and viewers can acknowledge but not reconfigure (see 15-teams-permissions.md).
