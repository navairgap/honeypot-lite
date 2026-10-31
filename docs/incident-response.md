# Event review and incident response (proposed)

A honeypot event is an observation of a connection, not proof of who initiated it or why. Treat peer addresses as network metadata that may be shared, translated, proxied, or spoofed.

## Triage sequence

1. Record the event/session identifier, UTC timestamp, listener, and relevant resource-limit counters.
2. Determine whether the event is a normal connection, malformed protocol input, limit violation, or unexpected process/network behavior.
3. Review the minimum necessary metadata. Avoid copying full request bodies into tickets or chat.
4. Check whether the container's isolation policy and outbound-deny controls remained active.
5. Escalate suspected host-boundary violations or unexpected outbound connections as an infrastructure incident, not merely a honeypot event.

## Evidence handling

Preserve a bounded, access-controlled event export with its schema version and source image/configuration identifiers. Redact authentication-like strings and unrelated personal data before sharing. Record any redaction so the export is not mistaken for a byte-for-byte original. Define retention and deletion deadlines before public deployment.

## Containment and rebuild

For suspected compromise, stop accepting new connections, isolate the instance at the network layer, preserve an authorized snapshot, then rebuild from a trusted image. Do not execute client-supplied commands to investigate the event. Do not mount additional host paths into a running instance as a debugging shortcut.

## Reporting limits

Avoid attribution claims from source IP, user-agent, service banner, or a single protocol signature. State what was observed, what was not captured, and which isolation checks were verified.