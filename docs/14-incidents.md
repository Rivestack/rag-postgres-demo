# Incidents

An incident is Driftline's record of an outage or degradation, and it drives what visitors see on your status page.

## Lifecycle

Every incident moves through four states, always in this order:

**investigating -> identified -> monitoring -> resolved**

- **investigating** — something is wrong and you are looking into it.
- **identified** — you know the cause and are working on a fix.
- **monitoring** — a fix is deployed; you are watching to confirm it holds.
- **resolved** — service is fully restored.

Each state change can include an update message, which is posted to your status page and sent through your alert channels. You cannot skip backwards; if a fix does not hold, open a new incident rather than reverting the old one.

## Auto-created vs manual incidents

Driftline auto-creates an incident when a monitor goes DOWN — which requires 2 or more of our 12 check regions to agree, so noise from one bad network path never opens an incident (see 13-troubleshooting.md for chasing false alerts). Auto-created incidents start in **investigating**, list the failing regions, and are auto-resolved when the monitor recovers.

You can also create incidents manually, for problems monitors cannot see (a broken signup email, say) or for scheduled maintenance:

```bash
driftline incidents list --state investigating
```

```python
from driftline import Driftline

client = Driftline(api_key="dl_live_xxxx")
incident = client.incidents.create(
    title="Elevated error rates on EU API",
    state="investigating",
    monitor_ids=["mon_8f2ka"],
)
```

Webhook subscribers receive `incident.created` and `incident.resolved` events for both kinds — see 06-webhooks.md for signature verification.

## Postmortems

After an incident reaches **resolved**, you can attach a postmortem: a Markdown write-up of what happened, the impact, and what you are changing. Postmortems can only be attached after resolve, and they appear on the incident's public page on your status page. Viewers with any role can read them; only admins and the owner can publish them (see 15-teams-permissions.md).
