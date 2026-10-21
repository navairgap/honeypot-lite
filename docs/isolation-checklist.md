# isolation checklist

This project is in design stage; do not deploy a listener until isolation controls exist. Use a dedicated unprivileged user and disposable VM or container. Mount no host credentials or Docker socket. Deny outbound traffic by default. Enforce connection, request-size, idle-time, and session limits. Bound and rotate logs. Never invoke a shell from received input. Rebuild the environment from a known image after compromise.
