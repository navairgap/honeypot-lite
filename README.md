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
