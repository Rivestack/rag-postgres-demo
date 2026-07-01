# Rate limits

The Driftline API applies rate limits to keep the platform fast for everyone. Limits depend on your plan:

| Plan | Limit |
| --- | --- |
| Free | 30 requests/min |
| Team | 120 requests/min |
| Business | 120 requests/min |

Limits are enforced **per API key**, not per user or per IP. If your org has several integrations, give each one its own key in Settings -> API Keys — they each get their own bucket, and you can rotate or revoke one without breaking the others (see 03-authentication.md).

## What happens when you hit the limit

Requests over the limit get an HTTP `429 Too Many Requests` response. Every 429 includes a `Retry-After` header telling you how many seconds to wait:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 12
```

Respect that header rather than retrying immediately. A minimal Python backoff looks like this:

```python
import time, requests

resp = requests.get(
    "https://api.driftline.example/v1/monitors",
    headers={"Authorization": "Bearer dl_live_xxxx"},
)
if resp.status_code == 429:
    time.sleep(int(resp.headers["Retry-After"]))
    resp = requests.get(...)  # retry once
```

The Python SDK (`pip install driftline`) handles 429 retries for you automatically.

## Batching advice

Most rate-limit problems come from making one request per monitor. Avoid that:

- `GET /v1/monitors` returns all monitors in pages of 100 — one call instead of fifty.
- Fetch incidents with a single filtered call (`GET /v1/incidents?state=open`) instead of checking each monitor.
- For dashboards, cache list responses for 30–60 seconds; monitor state rarely changes faster than your check interval anyway.
- In CI, prefer one `driftline monitors list --json` call and filter locally with `jq` (see 11-cli.md).

## When you need more headroom

Upgrading from Free to Team quadruples your limit to 120 requests/min. If you are on Business and consistently hitting limits, contact support@driftline.example — describe your use case and request volume and we can usually suggest a batching pattern that fits.
