# Vendor Notification and Patch Timeline Tracking

## Vendor Engagement Protocol

If the zero-day was discovered internally (not by the vendor), follow Coordinated Vulnerability Disclosure (CVD):
1. Notify the vendor via their published security disclosure contact within 24 hours of internal confirmation.
2. Request a private confirmation and tracking number from the vendor.
3. Agree on a disclosure timeline — 90 days is the industry standard.
4. If the vendor does not respond within 7 days, escalate to CERT/CC or the relevant national CERT.

If the zero-day was publicly disclosed by a third party or is already public:
- Engage the vendor immediately for patch timeline.
- Check if a vendor emergency advisory is in progress.

## Patch Timeline Tracking

Maintain a running timeline record for each zero-day event:

| Milestone | Target | Actual | Status |
|---|---|---|---|
| Vulnerability reported to vendor | Day 0 | | |
| Vendor acknowledgment received | Day 2 | | |
| Vendor patch committed | Day 30 | | |
| Patch available for testing | Day 45 | | |
| Patch deployed to staging | Day 50 | | |
| Patch deployed to production | Day 60 | | |
| Compensating controls retired | Day 61 | | |

Update this timeline every 48 hours. Escalate to CISO if vendor patch commitment date slips by more than 14 days.
