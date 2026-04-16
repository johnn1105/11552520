# =========================================================
# Project entry point
# =========================================================
from cli import run_cli_app

def main() -> None:
    # Run the application.
    print("[SYSTEM] main() started")
    run_cli_app()
    print("[SYSTEM] main() finished")

if __name__ == "__main__":
    print("[SYSTEM] Running main.py directly")
    main()
