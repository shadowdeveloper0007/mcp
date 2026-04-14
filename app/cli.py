from __future__ import annotations

import sys
import traceback

from app.mcp_server import run


def main() -> int:
    try:
        run()
        return 0
    except Exception as e:
        print(f"ERROR: CLI failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
