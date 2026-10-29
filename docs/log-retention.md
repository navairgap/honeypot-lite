# log retention

Log only the metadata required for the learning objective. Apply file permissions, rotation, size limits, and a documented retention period. Never record credentials intentionally submitted by clients beyond a safe redacted indicator. Treat logs as untrusted input when generating summaries. Keep honeypot storage separate from host secrets and provide a clear procedure to archive or delete old logs.

## Export and deletion audit

Exports should state the selected time range, event count, schema version, and whether any fields were redacted. Restrict export files to the service account and create them with restrictive permissions. Deletion should cover rotated files and temporary exports, report failures rather than silently claiming success, and avoid writing deleted event content into the audit log. Validate export paths so a configured destination cannot overwrite unrelated files.
