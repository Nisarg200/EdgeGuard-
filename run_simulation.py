from __future__ import annotations

import json
from pathlib import Path

from edgeguard_sim.simulation import run_simulation


def main() -> None:
    output_dir = Path("outputs")
    payload = run_simulation(output_dir)

    print("EdgeGuard simulation complete.")
    print(json.dumps(payload["summary"], indent=2))
    print(f"Detailed outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
