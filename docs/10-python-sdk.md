# Python SDK

The official Python SDK wraps the REST API described in 05-api-reference.md. It supports Python 3.9+.

## Install

```bash
pip install driftline
```

## Initialize the client

```python
from driftline import Driftline

client = Driftline(api_key="dl_live_xxxx")
```

Use a `dl_test_xxxx` key against your sandbox data. Keys are created and rotated in Settings -> API Keys; after a rotation the old key keeps working for 24 hours, so you can deploy the new one without downtime. See 03-authentication.md for the full key lifecycle.

## Create a monitor

```python
monitor = client.monitors.create(
    name="Checkout API",
    url="https://api.example.com/health",
    interval=30,          # seconds; 30s checks require the Team plan or above
    regions="all",        # check from all 12 regions
)
print(monitor.id)         # e.g. "mon_8fk2j1"
```

Free plans check every 5 minutes; Team allows 30-second intervals and Business allows 10-second intervals. Passing an interval below your plan's floor returns a validation error.

## List incidents

```python
for incident in client.incidents.list(status="open"):
    print(incident.id, incident.title, incident.stage)
```

`stage` is one of `investigating`, `identified`, `monitoring`, or `resolved` — the lifecycle described in 14-incidents.md.

## Error handling

The SDK raises typed exceptions. The one you'll hit most is `RateLimitError`: the API allows 30 requests/min on Free and 120/min on Team and Business, and 429 responses carry a `Retry-After` header the SDK surfaces for you.

```python
import time
from driftline import Driftline, RateLimitError

client = Driftline(api_key="dl_live_xxxx")

try:
    monitors = client.monitors.list()
except RateLimitError as e:
    time.sleep(e.retry_after)   # seconds, from the Retry-After header
    monitors = client.monitors.list()
```

Other exceptions include `AuthenticationError` (bad or revoked key) and `NotFoundError` (unknown resource ID). All inherit from `driftline.DriftlineError`, so a single except clause can catch everything. Prefer the CLI for one-off tasks (see 11-cli.md) and the SDK for anything running in production.
