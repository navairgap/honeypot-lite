# honeypot-lite

A tiny SSH/TCP honeypot that logs and studies intruders

> 🚧 **Status: planning** — architecture and README first, code next.

## Why

The best way to understand attackers is to watch them attack something safe. honeypot-lite emulates a few services, logs every interaction, and shows you what bots and script kiddies actually do — without ever giving them a real shell.

## Planned features

- Fake SSH and HTTP services with scripted, harmless responses
- Full session logging: credentials tried, commands attempted, files requested
- Summary dashboard of probes by country/asn (from local GeoIP)
- Written to be safe: jailed, no real executables, no outbound traffic

## Stack

`python` `asyncio` `docker`

## Notes

Defensive education tool. Run it on a VPS you own, never on shared infrastructure.

## License

MIT, see [LICENSE](LICENSE).

---
maintained · verified 2026-09-30
---
maintained · verified 2026-10-01
---
maintained · verified 2026-10-02

## Log format

Events are appended to `logs/honeypot.jsonl`, one JSON object per line:

```json
{"ts":"2026-10-03T17:55:12Z","service":"ssh","src":"185.220.101.4","event":"auth_attempt","user":"root","password":"admin123"}
```

Ship the file to your SIEM or analyze with `jq`.

## Docker Compose

```yaml
services:
  honeypot:
    build: .
    ports:
      - "2222:2222"
      - "8080:8080"
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

`docker compose up -d` — logs land in `./logs/honeypot.jsonl`.


## Running it legally

Honeypots are fine on networks you own or administer. Capturing attack traffic from others' networks without authorization is not. Know your jurisdiction before exposing it publicly.


## Tuning

`-v` raises emulation fidelity (slower, noisier logs). most deployments want `-q` and high volume: better odds of catching a real campaign. prune logs older than 90 days; attacker TTPs go stale fast.


## Analysis

quick wins with jq: `jq -r 'select(.service=="ssh") | .user' logs/*.jsonl | sort | uniq -c | sort -rn | head` — top tried usernames. same shape works for passwords and source IPs.

## Known limitations

low-interaction means the honeypot answers login attempts and banners — it never emulates a shell. attackers who get past the prompt see nothing, which is exactly when you should graduate to a high-interaction like cowrie.

## Known limitations

low-interaction means the honeypot answers login attempts and banners — it never emulates a shell. attackers who get past the prompt see nothing, which is exactly when you should graduate to a high-interaction like cowrie.
