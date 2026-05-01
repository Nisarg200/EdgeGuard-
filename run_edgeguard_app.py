from __future__ import annotations

import os


def load_dotenv(path: str = ".env") -> None:
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


if __name__ == "__main__":
    load_dotenv()
    from edgeguard_app.server import run

    host = os.getenv("EDGEGUARD_HOST", "127.0.0.1")
    port = int(os.getenv("EDGEGUARD_PORT", "8080"))
    run(host=host, port=port)
