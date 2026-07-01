# Webhooks

Webhooks let Driftline push events to your own systems the moment something changes. Create endpoints under Settings -> Webhooks, or via the API using the key you set up in 03-authentication.md.

## Events

Driftline sends four event types:

- `monitor.down` — a monitor failed its check with regional quorum (2+ of our 12 regions agree)
- `monitor.up` — a previously down monitor recovered
- `incident.created` — an incident was opened, manually or automatically
- `incident.resolved` — an incident reached the resolved state (see 14-incidents.md for the full lifecycle)

## Payload example

Every delivery is a JSON POST:

```json
{
  "event": "monitor.down",
  "created_at": "2026-07-01T14:22:07Z",
  "data": {
    "monitor_id": "mon_8fk2j1",
    "name": "API - production",
    "url": "https://api.example.com/health",
    "regions_failing": ["us-east", "eu-west", "ap-south"]
  }
}
```

## Verifying signatures

Each request includes an `X-Driftline-Signature` header: an HMAC-SHA256 of the raw request body, keyed with your endpoint's signing secret. Always verify it before trusting the payload.

```python
import hashlib
import hmac

def verify(secret: str, body: bytes, signature: str) -> bool:
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

Reject anything that fails verification with a 401. Use the raw body bytes — re-serializing the JSON first will change the digest and break comparison.

## Retries

If your endpoint returns a non-2xx response or times out after 10 seconds, Driftline retries the delivery 3 times with exponential backoff: 30 seconds, then 5 minutes, then 30 minutes. After the third failed retry the delivery is marked dead and visible under Settings -> Webhooks -> Delivery log, where you can replay it manually.

Respond with a 2xx as quickly as possible — queue heavy work instead of doing it inline. If you only need Slack notifications rather than custom handling, the built-in integration in 09-integrations-slack.md is simpler to run.
