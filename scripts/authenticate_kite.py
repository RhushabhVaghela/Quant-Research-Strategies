from __future__ import annotations
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.kite_auth import ZerodhaAuthenticator

def parse_args():
    p = argparse.ArgumentParser(description="Zerodha Session Authenticator & Token Manager")
    p.add_argument("--force", action="store_true", help="Force a new OAuth login even if current token is valid")
    p.add_argument("--port", type=int, default=8000, help="Local HTTP callback server port (default: 8000)")
    return p.parse_args()

def main():
    args = parse_args()
    print("Initializing Zerodha Session Authenticator...")
    authenticator = ZerodhaAuthenticator(redirect_port=args.port)

    if not args.force and authenticator.is_token_valid():
        print("Existing Zerodha access token is valid and active!")
        print("No re-authentication required.")
        return

    try:
        token = authenticator.get_valid_access_token(force_refresh=args.force)
        print(f"\nAuthentication successful! Session token active: {token[:6]}...{token[-4:]}")
    except Exception as e:
        print(f"\nAuthentication Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
