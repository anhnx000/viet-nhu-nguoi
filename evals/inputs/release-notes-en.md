# Release 3.4.0 (Dec 2, 2026)

## Highlights
- Export jobs are now up to 40% faster for workspaces with more than 10,000 records.
- New "Scheduled reports" feature: admins can schedule weekly or monthly reports that are delivered by email. Limited to 5 schedules per workspace during the beta.
- The legacy v1 API will be deprecated on March 31, 2027. Please migrate to v2 before that date.

## Fixes
- Fixed an issue where CSV imports failed silently when a file contained more than 50 columns.
- Fixed incorrect timezone handling in the audit log (it was always shown in UTC).

## Known issues
- Scheduled reports are not yet available for workspaces on the Free plan.
