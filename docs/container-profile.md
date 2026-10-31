# Least-privilege container profile (proposed)

A future honeypot listener should be treated as hostile-input software. The container is a containment layer, not a guarantee that compromise is impossible.

## Baseline profile

- Run as a dedicated non-root UID/GID with no supplementary privileges unless explicitly justified.
- Drop all Linux capabilities by default; add only a narrowly scoped capability if the listener demonstrably requires it.
- Use a read-only root filesystem and mount only a dedicated, size-limited log directory as writable.
- Do not mount the host home directory, container runtime socket, SSH agent, cloud credentials, or host device nodes.
- Apply CPU, memory, process-count, open-file, and log-volume limits.
- Deny outbound network traffic by default. Document and review any narrowly scoped exception.
- Bind to loopback during development. Public exposure requires a separate firewall and isolation review.

## Runtime behavior

Received bytes remain data. Never invoke a shell, template engine, dynamic loader, or filesystem path operation derived from a client message. Cap connection count, message size, idle time, and per-session event volume.

## Deployment verification

Record the image digest and configuration used for each run. Verify the effective UID, mounts, capabilities, read-only paths, resource limits, listener address, and outbound policy from inside the test environment. Do not rely only on a Compose file's intended settings; inspect the running container.

## Recovery

After suspected compromise, stop the instance, preserve only the authorized evidence needed for analysis, and rebuild from a known image. Do not attempt to sanitize and reuse a potentially compromised container.

## Tests

Use a disposable local environment to verify each control. Tests must not contact public infrastructure or use real attacker traffic.