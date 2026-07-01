# Troubleshooting

Common issues and how to fix them. If you get stuck, email support@driftline.example with your org slug and a timestamp.

## False DOWN alerts

Driftline runs checks from 12 regions and only marks a monitor DOWN when **2 or more regions agree** (quorum). So a single flaky network path will not page you — if you are getting DOWN alerts, at least two regions really could not reach your endpoint.

The most common cause is a firewall or WAF blocking our checkers. Fix it by allowlisting the Driftline checker IP ranges, published at `GET /v1/meta/checker-ips`. Other things to verify:

- Your endpoint responds within the check timeout (10 seconds by default).
- You are not rate-limiting the checker user agent `Driftline-Check/1.0`.
- The health endpoint returns a 2xx status; redirects to a login page count as failures.

Each auto-created incident lists which regions failed — see 14-incidents.md.

## Webhook not firing

If your endpoint never receives `monitor.down` or other events, work through this list:

1. **Signature verification failing?** Payloads are signed with HMAC-SHA256 and delivered in the `X-Driftline-Signature` header. Verify against the *raw* request body — re-serializing the JSON first is the classic mistake and will never match.
2. **Endpoint returning non-2xx?** We treat anything else as a failure and retry 3 times with exponential backoff: 30 seconds, 5 minutes, then 30 minutes. After the third failure the delivery is marked dead — you can still inspect and replay it from the Delivery log.
3. **Check the delivery log** in Settings -> Webhooks, which shows each attempt's response code and body.

## CLI login loops

If `driftline login` keeps asking for a key:

- Confirm `~/.driftline/config.toml` is writable; a read-only home directory (common in containers) silently prevents saving.
- Make sure you pasted a live key (`dl_live_xxxx`), not a truncated one.
- If the key was rotated, remember the old key stays valid for only 24 hours — after that you must log in with the new key.
- In CI, skip login entirely and set `DRIFTLINE_API_KEY` (see 11-cli.md).
