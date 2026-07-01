# Plans and Billing

Driftline has three plans. This page explains what each includes and how upgrades, downgrades, invoices, and overages work.

## Plans

| Plan | Price | Monitors | Check interval | Extras |
|------|-------|----------|----------------|--------|
| Free | $0 | 5 | 5 minutes | Email, Slack & webhook alerts |
| Team | $29/mo | 50 | 30 seconds | Custom status page domains |
| Business | $99/mo | 500 | 10 seconds | SSO (SAML), SMS alerts |

Check history retention also varies by plan: 90 days on Free, 13 months on Team, and 25 months on Business. You can export history as CSV under **Settings -> Export** or via `GET /v1/exports` (see 05-api-reference.md).

## Upgrades are prorated

When you upgrade mid-cycle, you're charged only for the remainder of the current billing period. For example, upgrading from Team to Business halfway through the month bills you roughly half the price difference, and the new limits apply immediately.

## Downgrades

When you downgrade, the change takes effect at the start of your next billing cycle, and any unused amount is applied as a credit to your account rather than refunded. You keep your current plan's features until the cycle ends.

## Invoices

All invoices live under **Settings -> Billing**, where you can download PDFs, update your card, and set a billing email for receipts.

## What happens if you exceed your monitor limit

Driftline never surprise-bills you. If your organization has more monitors than your plan allows — say, after a downgrade from Team (50 monitors) to Free (5) — the monitors above the limit are **paused**, not billed. Paused monitors keep their configuration and history and resume as soon as you upgrade or delete other monitors.

## Questions

For anything billing-related — VAT details, annual invoicing, plan advice — email support@driftline.example. To see what your plan means for API usage, check 12-rate-limits.md.
