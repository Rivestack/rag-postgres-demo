# API Reference

The Driftline REST API lives at:

```
https://api.driftline.example/v1
```

All requests need an `Authorization: Bearer dl_live_xxxx` header — see 03-authentication.md for creating keys. Responses are JSON. Rate limits are 30 requests/min on Free and 120/min on Team and Business; a `429` response includes a `Retry-After` header telling you how many seconds to wait.

## List monitors

```bash
curl https://api.driftline.example/v1/monitors \
  -H "Authorization: Bearer dl_live_xxxx"
```

```json
{
  "data": [
    {
      "id": "mon_8f2k1",
      "name": "App health",
      "url": "https://app.example.com/health",
      "status": "up",
      "interval_seconds": 30
    }
  ],
  "has_more": false
}
```

## Create a monitor

```bash
curl -X POST https://api.driftline.example/v1/monitors \
  -H "Authorization: Bearer dl_live_xxxx" \
  -H "Content-Type: application/json" \
  -d '{"name": "Marketing site", "url": "https://www.example.com", "interval_seconds": 30}'
```

The allowed `interval_seconds` depends on your plan (see 04-billing.md). Creating a monitor past your plan limit returns `422`; existing monitors above the limit are paused, never billed.

## Get monitor status

```bash
curl https://api.driftline.example/v1/monitors/mon_8f2k1/status \
  -H "Authorization: Bearer dl_live_xxxx"
```

```json
{
  "id": "mon_8f2k1",
  "status": "down",
  "regions_failing": ["eu-west", "us-east", "ap-south"],
  "quorum_met": true,
  "since": "2026-07-01T09:14:00Z"
}
```

`quorum_met` is true when 2 or more of the 12 check regions agree the endpoint is failing — only then is a monitor DOWN (01-getting-started.md explains why).

## List incidents

```bash
curl "https://api.driftline.example/v1/incidents?state=investigating" \
  -H "Authorization: Bearer dl_live_xxxx"
```

```json
{
  "data": [
    {
      "id": "inc_x91m3",
      "monitor_id": "mon_8f2k1",
      "state": "investigating",
      "created_at": "2026-07-01T09:14:05Z"
    }
  ]
}
```

Incident `state` moves through `investigating`, `identified`, `monitoring`, and `resolved`. For push-based updates instead of polling, subscribe to the `monitor.down`, `monitor.up`, `incident.created`, and `incident.resolved` webhook events, verified via the `X-Driftline-Signature` HMAC-SHA256 header.
