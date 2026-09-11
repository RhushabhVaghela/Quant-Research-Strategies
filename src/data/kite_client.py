from __future__ import annotations
import os
from typing import Any
from dotenv import load_dotenv
from kiteconnect import KiteConnect

from .kite_auth import ZerodhaAuthenticator

load_dotenv()

class KiteClient:
    """Authenticated Kite client for the research data layer."""

    def __init__(
        self,
        api_key: str | None = None,
        access_token: str | None = None,
        auto_authenticate: bool = True,
    ):
        self.api_key = api_key or os.getenv("KITE_API_KEY") or os.getenv("ZERODHA_ALGOTRADER_API_KEY")
        self.access_token = access_token or os.getenv("KITE_ACCESS_TOKEN")

        if auto_authenticate and not access_token:
            auth = ZerodhaAuthenticator(api_key=self.api_key)
            if not auth.is_token_valid(self.access_token):
                self.access_token = auth.get_valid_access_token()
                self.api_key = auth.api_key

        if not self.api_key:
            raise ValueError("KITE_API_KEY is not set.")
        if not self.access_token:
            raise ValueError("KITE_ACCESS_TOKEN is not set.")

        self._kite = KiteConnect(api_key=self.api_key)
        self._kite.set_access_token(self.access_token)

    @property
    def kite(self) -> KiteConnect:
        return self._kite

    def instruments(self, exchange: str | None = None) -> list[dict[str, Any]]:
        return self._kite.instruments(exchange) if exchange else self._kite.instruments()
