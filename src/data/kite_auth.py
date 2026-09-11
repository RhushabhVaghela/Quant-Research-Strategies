from __future__ import annotations
import http.server
import os
import socketserver
import sys
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"
TOKEN_FILE_PATH = ROOT / "access_token.txt"

def update_env_file(key: str, value: str, env_path: Path = ENV_PATH) -> None:
    """Helper function to update or set a key in the .env file."""
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    key_found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}=") or line.strip().startswith(f"{key} ="):
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)

    if not key_found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"{key}={value}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    os.environ[key] = value

def save_access_token_file(token: str, token_path: Path = TOKEN_FILE_PATH) -> None:
    """Saves the access token to access_token.txt for legacy compatibility."""
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(token)

class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    received_request_token: str | None = None
    error_message: str | None = None

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)

        if "request_token" in params:
            _CallbackHandler.received_request_token = params["request_token"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
                <head><title>Zerodha Auth Success</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 60px; background-color: #f4f6f8;">
                    <div style="display: inline-block; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        <h1 style="color: #2e7d32; margin-bottom: 10px;">✔ Login Successful!</h1>
                        <p style="font-size: 16px; color: #444;">Zerodha Access Token generated and saved automatically.</p>
                        <p style="color: #888; font-size: 14px;">You can close this tab and return to your terminal.</p>
                    </div>
                </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        elif params.get("status") in (["error"], ["failed"]):
            error_msg = params.get("message", params.get("status", ["Unknown error"]))[0]
            _CallbackHandler.error_message = error_msg
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <!DOCTYPE html>
            <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 60px;">
                    <h2 style="color: #c62828;">Authentication Failed</h2>
                    <p>Error: {error_msg}</p>
                </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            # Send OK for favicon or non-token GET requests without erroring
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"OK")

    def log_message(self, format: str, *args: Any) -> None:
        pass

class ZerodhaAuthenticator:
    """Manages session verification, automated OAuth redirect callback, and token persistence."""

    def __init__(self, api_key: str | None = None, api_secret: str | None = None, redirect_port: int | None = None):
        self.api_key = api_key or os.getenv("KITE_API_KEY") or os.getenv("ZERODHA_ALGOTRADER_API_KEY")
        self.api_secret = api_secret or os.getenv("KITE_API_SECRET") or os.getenv("ZERODHA_ALGOTRADER_API_SECRET")
        port_env = os.getenv("KITE_REDIRECT_PORT") or os.getenv("ZERODHA_REDIRECT_PORT")
        self.redirect_port = redirect_port or (int(port_env) if port_env else 8000)

    def is_token_valid(self, access_token: str | None = None) -> bool:
        token = access_token or os.getenv("KITE_ACCESS_TOKEN")
        if not self.api_key or not token:
            return False
        try:
            kite = KiteConnect(api_key=self.api_key)
            kite.set_access_token(token)
            profile = kite.profile()
            return isinstance(profile, dict) and "user_id" in profile
        except Exception:
            return False

    def extract_request_token(self, text_input: str) -> str:
        """Extracts request_token whether user inputs raw token or full redirect URL."""
        text = text_input.strip()
        if "request_token=" in text:
            parsed = urllib.parse.urlparse(text)
            params = urllib.parse.parse_qs(parsed.query)
            if "request_token" in params:
                return params["request_token"][0]
        return text

    def get_valid_access_token(self, force_refresh: bool = False, timeout_seconds: int = 120) -> str:
        """Checks if current token is valid; if not, launches callback listener to fetch a new token automatically."""
        load_dotenv(ENV_PATH, override=True)
        self.api_key = self.api_key or os.getenv("KITE_API_KEY") or os.getenv("ZERODHA_ALGOTRADER_API_KEY")
        self.api_secret = self.api_secret or os.getenv("KITE_API_SECRET") or os.getenv("ZERODHA_ALGOTRADER_API_SECRET")

        if not self.api_key:
            raise ValueError("KITE_API_KEY is not set. Please add it to your .env file.")

        current_token = os.getenv("KITE_ACCESS_TOKEN")
        if not force_refresh and current_token and self.is_token_valid(current_token):
            return current_token

        if not self.api_secret:
            raise ValueError(
                "Existing KITE_ACCESS_TOKEN is expired or missing, and KITE_API_SECRET is not set in .env. "
                "Please set KITE_API_SECRET to automate token generation."
            )

        print("\n[Zerodha Auth] Access token is missing or expired.")
        print("[Zerodha Auth] Starting local redirect listener...")

        _CallbackHandler.received_request_token = None
        _CallbackHandler.error_message = None

        server = None
        # Try configured port, or fallback ports (8000, 5000, 8080, 3000)
        ports_to_try = [self.redirect_port] + [p for p in [8000, 5000, 8080, 3000] if p != self.redirect_port]
        active_port = self.redirect_port

        for port in ports_to_try:
            try:
                server = socketserver.TCPServer(("0.0.0.0", port), _CallbackHandler)
                server.timeout = 0.5
                active_port = port
                break
            except Exception:
                continue

        kite = KiteConnect(api_key=self.api_key)
        login_url = kite.login_url()

        print(f"[Zerodha Auth] Opening browser login page...")
        try:
            webbrowser.open(login_url)
        except Exception:
            print(f"Login URL: {login_url}")

        print(f"[Zerodha Auth] Listening for automatic redirect on port {active_port}...")
        print("[Zerodha Auth] Simply log in in your browser — token will be captured automatically!")

        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            if server:
                server.handle_request()
            if _CallbackHandler.received_request_token:
                break
            if _CallbackHandler.error_message:
                if server:
                    server.server_close()
                raise RuntimeError(f"Authentication failed: {_CallbackHandler.error_message}")

        if server:
            server.server_close()

        request_token = _CallbackHandler.received_request_token

        # Fallback only if automatic redirect timed out
        if not request_token:
            print("\n[Zerodha Auth] Automatic redirect did not trigger within timeout.")
            fallback_input = input("Please paste your request_token or redirected URL: ")
            request_token = self.extract_request_token(fallback_input)

        if not request_token:
            raise TimeoutError("No request_token received.")

        print("[Zerodha Auth] Captured request_token! Exchanging for access_token...")

        session_data = kite.generate_session(request_token, api_secret=self.api_secret)
        new_access_token = session_data["access_token"]

        update_env_file("KITE_ACCESS_TOKEN", new_access_token)
        save_access_token_file(new_access_token)

        print("[Zerodha Auth] Authentication complete! New KITE_ACCESS_TOKEN saved to .env.\n")
        return new_access_token

def ensure_authenticated_client(force_refresh: bool = False) -> KiteConnect:
    """Returns an authenticated KiteConnect client, refreshing the access token if needed."""
    auth = ZerodhaAuthenticator()
    token = auth.get_valid_access_token(force_refresh=force_refresh)
    kite = KiteConnect(api_key=auth.api_key)
    kite.set_access_token(token)
    return kite
