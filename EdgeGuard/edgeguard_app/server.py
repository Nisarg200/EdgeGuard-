"""HTTP server for the EdgeGuard interactive app."""

from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .service import EdgeGuardService


WEB_DIR = Path(__file__).with_name("web")
SERVICE = EdgeGuardService()


class EdgeGuardRequestHandler(BaseHTTPRequestHandler):
    server_version = "EdgeGuardHTTP/1.0"

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        content = path.read_bytes()
        content_type, _ = mimetypes.guess_type(str(path))
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type or 'application/octet-stream'}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_file(WEB_DIR / "index.html")
            return
        if parsed.path == "/api/config":
            self._send_json(SERVICE.app_status())
            return
        if parsed.path == "/api/scenarios":
            self._send_json({"items": SERVICE.scenarios()})
            return
        if parsed.path.startswith("/static/"):
            relative = parsed.path.removeprefix("/static/")
            self._send_file(WEB_DIR / relative)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Route not found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/ask":
            self.send_error(HTTPStatus.NOT_FOUND, "Route not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            payload = json.loads(body.decode("utf-8"))
            query = (payload.get("query") or "").strip()
            role = (payload.get("role") or "operations").strip()
            if not query:
                self._send_json({"error": "Query is required."}, status=400)
                return
            self._send_json(SERVICE.process(query=query, role=role))
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON payload."}, status=400)

    def log_message(self, format: str, *args) -> None:
        return


def run(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), EdgeGuardRequestHandler)
    print(f"EdgeGuard app running on http://{host}:{port}")
    server.serve_forever()
