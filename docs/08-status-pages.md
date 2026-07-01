# Status pages

Every Driftline org gets a hosted status page so your users can check availability without emailing you. Pages update in real time from the same checks that drive alerting (see 07-alerting.md).

## Your page URL

Status pages live at:

```
https://<org>.status.driftline.example
```

If your org slug is `acme`, your page is `https://acme.status.driftline.example`. The slug is set under Settings -> General and can be changed once every 30 days.

## Custom domains

On Team and Business plans you can serve the page from your own domain. Point a CNAME at your Driftline hostname:

```
status.acme.com.  CNAME  acme.status.driftline.example.
```

Then add the domain under Settings -> Status Page -> Custom domain. Driftline provisions a TLS certificate automatically, usually within a few minutes of DNS propagating. Custom domains are not available on the Free plan.

## What visitors see

- **Overall state** — a single banner: all systems operational, degraded, or major outage.
- **Per-monitor status** — the monitors you've chosen to publish, each with a 90-day uptime bar. You control which monitors appear; internal ones stay hidden.
- **Active and past incidents** — updates through the full lifecycle (investigating, identified, monitoring, resolved), plus any postmortems you attach after resolving. Incident authoring is covered in 14-incidents.md.

Visitors can subscribe to email updates directly from the page.

## Embeddable badge

Drop a live status badge into any site with one script tag:

```html
<script src="https://acme.status.driftline.example/badge.js"></script>
```

The badge renders a small pill showing current overall status and links back to your full status page. It's plain JavaScript with no dependencies and weighs under 3 KB, so it's safe for marketing pages and app footers alike. If you need programmatic status instead, query the API described in 05-api-reference.md.
