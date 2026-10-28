# isolation checklist

This project is in design stage; do not deploy a listener until isolation controls exist. Use a dedicated unprivileged user and disposable VM or container. Mount no host credentials or Docker socket. Deny outbound traffic by default. Enforce connection, request-size, idle-time, and session limits. Bound and rotate logs. Never invoke a shell from received input. Rebuild the environment from a known image after compromise.
## Evidence and teardown

Record event timestamps in UTC and preserve the minimum metadata needed to reproduce a detection. Treat all captured request data as untrusted and potentially sensitive; redact authentication-like values before exporting a report. Define a retention deadline and enforce storage quotas. After a suspected compromise, preserve an authorized evidence snapshot, stop the isolated instance, and rebuild from a known image rather than attempting to sanitize and reuse it.

## Pre-launch verification gate

Do not start a listener until every item below has a recorded pass result:

- Confirm the process runs as a dedicated unprivileged identity and cannot read host home directories or container-runtime sockets.
- From the test namespace, verify outbound connections are blocked by default and only explicitly approved destinations are reachable.
- Verify connection count, request size, idle timeout, and per-session storage limits with boundary tests.
- Confirm received input is recorded as data only; no command execution, template evaluation, or dynamic file inclusion is reachable from it.
- Force a crash/restart in a disposable environment and verify logs rotate, retained data stays bounded, and the environment can be rebuilt from a known image.

