# Egress isolation verification (proposed)

Honeypot-Lite is still in the design stage. Its future deployment should deny
outbound access by default so an exposed listener cannot become a relay or
reach host-adjacent services.

This checklist is for a disposable test environment you own. It does not
replace a platform-specific firewall or container security review.

## Intended network shape

- Place the listener on a dedicated ingress network.
- Do not attach a default route from the honeypot namespace to the public
  internet or the host's management network.
- Keep administration and log collection on a separate, narrowly scoped path.
- Do not mount the container runtime socket, host home directory, SSH agent,
  cloud credentials, or unrelated host devices into the listener.
- Do not add an egress exception merely to simplify logging or debugging.

## Verification procedure

1. Start a disposable instance with the intended production network policy.
2. Record the image digest, runtime configuration, network attachments, and
   effective firewall rules.
3. Confirm that an inbound connection to the intended listener works from the
   isolated test client.
4. From the honeypot's network namespace, attempt a connection to a controlled
   canary service placed outside the permitted ingress segment. The attempt
   must fail under the egress-deny policy.
5. Verify the relevant firewall or network-policy drop counter increments.
6. Check DNS separately: a blocked TCP test does not prove that DNS queries
   cannot leave the namespace.
7. Confirm that the listener still records local events and that the denied
   probe does not create an unbounded retry loop.
8. Tear down the disposable instance and its test networks after capturing the
   verification result.

Do not use a public third-party service as the canary. The target should be a
controlled endpoint in a lab network, and the expected deny path should be
observable from the network policy.

## Evidence to retain

Record the test time, image digest, configuration revision, network policy
revision, allowed ingress path, egress test destination, result, and relevant
drop counters. Store this evidence separately from attacker-supplied event
records so untrusted client data cannot forge a successful isolation check.

## Failure handling

Treat an unexpected successful outbound connection as a deployment blocker.
Stop the instance, correct the network policy outside the running container,
and repeat the test from a fresh instance. Do not rely on application code
alone to enforce egress restrictions.

## Regression cases

Repeat the check after image, runtime, firewall, network, or logging changes.
Include both IP-based and DNS-based egress checks, and verify that local event
writing remains functional while external egress stays denied.
