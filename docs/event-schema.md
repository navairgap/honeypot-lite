# Honeypot event records (draft v1)

The future logger should write newline-delimited JSON (JSONL), one event per line. This is a proposed schema, not a claim that an emulator or logger is implemented.

## Example

```json
{
  "schema_version": 1,
  "timestamp": "2026-10-20T12:00:00Z",
  "event": "connection_open",
  "listener": "demo-http",
  "peer": { "address": "192.0.2.5", "port": 49152 },
  "connection_id": "local-000001",
  "bytes_received": 0,
  "duration_ms": null
}
```

## Privacy and resource limits

- Record only fields required to understand connection behavior. Do not log credentials, full request bodies, or arbitrary binary payloads by default.
- Cap every attacker-controlled string and normalize control characters before terminal display.
- Enforce a maximum event size; oversized events should be truncated with an explicit `truncated: true` flag or rejected.
- Use UTC timestamps and a monotonically increasing local event sequence when ordering matters.
- Rotate files by size and age, and define a hard disk-usage ceiling.
- Keep listener names and event types from controlled enums, not directly from client input.

## Suggested event types

`connection_open`, `connection_close`, `protocol_message`, `protocol_error`, and `limit_exceeded`. Include only metadata needed for the selected event.

## Tests

Test JSONL round trips, malformed input handling, string escaping, size limits, rotation boundaries, and continued logging after a client disconnect. No test should execute client-supplied commands or make outbound network connections.
