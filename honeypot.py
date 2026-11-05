#!/usr/bin/env python3
"""Low-interaction HTTP observer. It never executes commands or proxies traffic."""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


def _clean(value: object, limit: int) -> str:
    if not isinstance(value, str):
        return ""
    return "".join(ch for ch in value if ch.isprintable())[:limit]


class EventWriter:
    """Append bounded metadata-only JSONL events with a process-local lock."""

    def __init__(self, path: str | Path, max_bytes: int = 1_000_000,
                 max_events: int = 10_000) -> None:
        if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 1:
            raise ValueError("max_bytes must be a positive integer")
        if isinstance(max_events, bool) or not isinstance(max_events, int) or max_events < 1:
            raise ValueError("max_events must be a positive integer")
        self.path = Path(path)
        self.max_bytes = max_bytes
        self.max_events = max_events
        self._bytes = self.path.stat().st_size if self.path.exists() else 0
        self._events = 0
        self._lock = threading.Lock()

    def record(self, event: dict[str, object]) -> bool:
        payload = (json.dumps(event, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")
        with self._lock:
            if self._events >= self.max_events or self._bytes + len(payload) > self.max_bytes:
                return False
            try:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                fd = os.open(self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
                try:
                    written = os.write(fd, payload)
                finally:
                    os.close(fd)
                if written != len(payload):
                    return False
            except OSError as exc:
                print(f"honeypot: log write failed: {exc}", file=sys.stderr)
                return False
            self._bytes += len(payload)
            self._events += 1
            return True


def make_handler(writer: EventWriter):
    class Handler(BaseHTTPRequestHandler):
        server_version = "MinimalObserver"
        sys_version = ""

        def _observe(self) -> None:
            target = urlsplit(self.path)
            event = {
                "timestamp": int(time.time()),
                "remote_ip": str(self.client_address[0]),
                "method": _clean(self.command, 12),
                "path": _clean(target.path, 256),
                "user_agent": _clean(self.headers.get("User-Agent", ""), 160),
            }
            writer.record(event)
            self.close_connection = True
            body = b"observer endpoint\n"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        do_GET = _observe
        do_HEAD = _observe
        do_POST = _observe
        do_PUT = _observe
        do_DELETE = _observe
        do_OPTIONS = _observe

        def log_message(self, fmt: str, *args: object) -> None:
            return

    return Handler


def _loopback(bind: str) -> bool:
    try:
        return ipaddress.ip_address(bind).is_loopback
    except ValueError:
        return bind.lower() == "localhost"


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("value must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--log", default="./honeypot-events.jsonl")
    parser.add_argument("--max-log-bytes", type=positive_int, default=1_000_000)
    parser.add_argument("--max-events", type=positive_int, default=10_000)
    parser.add_argument("--confirm-public-bind", action="store_true",
                        help="required before binding beyond loopback")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if not _loopback(args.bind) and not args.confirm_public_bind:
        parser.error("non-loopback bind requires --confirm-public-bind")
    writer = EventWriter(args.log, args.max_log_bytes, args.max_events)
    server = ThreadingHTTPServer((args.bind, args.port), make_handler(writer))
    print(f"listening on {args.bind}:{server.server_address[1]}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
