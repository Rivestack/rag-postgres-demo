# Teams and permissions

Driftline orgs have four roles. Pick the least-powerful role that lets someone do their job.

## Roles

| Role | What they can do |
| --- | --- |
| **viewer** | Read-only: view monitors, incidents, and dashboards. Cannot change anything. |
| **member** | Everything viewers can, plus create and pause monitors, open and update incidents, and acknowledge alerts. |
| **admin** | Everything members can, plus manage alert channels and escalation policies, invite and remove users, manage API keys, and publish postmortems. |
| **owner** | Everything admins can, plus billing, plan changes, and deleting the org. |

A good default: engineers as members, your on-call leads as admins, stakeholders as viewers.

## Inviting people

Admins and the owner can invite teammates from Settings -> Team. Invitations are sent by email, expire after 7 days, and specify a role up front — you can change the role later without re-inviting. Members and viewers cannot invite anyone.

## The owner role

Each org has exactly **one owner**. Ownership is transferable: the current owner picks another user in Settings -> Team, and that user must accept before the transfer completes. The previous owner becomes an admin. Only the owner can see invoices or change the plan (see 04-billing.md), so transfer ownership before someone with billing access leaves the company.

## SSO with SAML

SAML single sign-on is available on the **Business plan only** ($99/mo). Once configured, you can require SSO for all users, and role assignment can be mapped from your identity provider's groups so new hires land with the right permissions automatically. Free and Team orgs use email/password or magic links.

## Roles and the API

API keys are org-scoped, not user-scoped, and always have admin-level access — so treat them accordingly and rotate them from Settings -> API Keys if someone with key access leaves (the old key stays valid for 24 hours after rotation; see 03-authentication.md). For automation that should be read-only, use a viewer account with the CLI instead (see 11-cli.md).
