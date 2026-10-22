# honeypot-lite

A planned low-interaction honeypot for observing unsolicited connection attempts in an isolated environment.

> **Status: design stage.** This repository currently contains documentation only; the emulated services and logger are not implemented yet.

## Goal

Provide a small, inspectable way to study common probes without giving remote clients a real shell or access to host resources.

## Initial scope

- Emulate a limited set of service banners and harmless responses.
- Record connection metadata and protocol events as newline-delimited JSON.
- Keep logs local and make their schema explicit.
- Apply connection, message-size, and time limits.
- Provide a simple summary command for local log files.

## Security boundaries

- Run inside a dedicated container or isolated VM with no host credentials mounted.
- Deny outbound network access unless a documented use case requires it.
- Do not execute submitted commands, open uploaded files, or proxy clients to real services.
- Place logs on a size-limited volume; log data may contain attacker-supplied strings and must be treated as untrusted.
- Bind to loopback during development. Public deployment requires an explicit firewall and isolation review.
- Deploy only on infrastructure you own or are authorized to administer, and follow applicable rules for collecting connection data.

## Planned milestones

- [ ] Define a versioned JSONL event schema.
- [ ] Implement a single harmless protocol emulator.
- [ ] Add tests for oversized input, disconnects, and malformed messages.
- [ ] Add log rotation and bounded storage.
- [ ] Document container permissions and an egress-deny deployment.

## Limitations

A low-interaction honeypot cannot reliably reproduce a real operating system or capture every attacker technique. Its events are observations, not proof of attribution.

## License

MIT. See [LICENSE](LICENSE).


## Isolation first

Run only in a disposable, isolated environment with an unprivileged account, no mounted host credentials, and outbound traffic denied by default. Bound connection and message sizes, rotate logs, and never execute commands derived from client input.
