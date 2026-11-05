# Safe deployment boundary

The first version is an HTTP metadata observer, not a shell or command
emulator. It records only timestamp, remote IP, method, URL path and a bounded
User-Agent value. It does not read request bodies, execute submitted input,
open uploaded files, or proxy to another service.

The default bind is `127.0.0.1`. Binding to a non-loopback
address requires the explicit `--confirm-public-bind` flag.
That flag is not a substitute for isolation review.

Before any non-local deployment:
1. Use a disposable VM or container and an unprivileged account.
2. Deny outbound traffic and do not mount host credentials or sensitive paths.
3. Put logs on a dedicated size-limited volume.
4. Restrict inbound access with a host or upstream firewall.
5. Confirm that collection and retention of connection metadata is lawful.

The JSONL writer has byte and event quotas. When a quota is reached or a write
fails, the observer continues serving but drops the event; retain this
limitation in monitoring procedures. Treat every logged string as
attacker-controlled and keep logs out of public repositories.
