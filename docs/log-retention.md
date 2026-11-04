# log retention

Log only the metadata required for the learning objective. Apply file permissions, rotation, size limits, and a documented retention period. Never record credentials intentionally submitted by clients beyond a safe redacted indicator. Treat logs as untrusted input when generating summaries. Keep honeypot storage separate from host secrets and provide a clear procedure to archive or delete old logs.

## Export and deletion audit

Exports should state the selected time range, event count, schema version, and whether any fields were redacted. Restrict export files to the service account and create them with restrictive permissions. Deletion should cover rotated files and temporary exports, report failures rather than silently claiming success, and avoid writing deleted event content into the audit log. Validate export paths so a configured destination cannot overwrite unrelated files.


## Quota and rotation behavior

Define three independent controls before deployment: a maximum size for one active log, a maximum total size for retained logs, and a maximum retention age. Rotate only at complete JSONL record boundaries so a reader never receives half of an event as a valid line. Record the schema version and session identifier in each rotated file or its manifest.

When the total quota is reached, apply the configured policy to the oldest closed rotation first; never silently delete the active file or an unexported incident snapshot. If storage is exhausted or a write fails, report the logging failure through stderr or the supervisor, count dropped events in bounded in-memory state, and stop retrying the same failed write in a tight loop. A successful connection response must not imply that its event was durably recorded.

## Boundary tests

Exercise rotation immediately before and after a complete record, a single event larger than the file limit, a full retention quota, a disk-write error, and deletion of an expired rotation while a current log remains intact. Verify that cleanup never follows a symlink outside the configured log directory.
