"""
Quotex adapter boundary.

This file deliberately does not pretend there is an official Quotex REST API.
Wire this class to the exact community Quotex client/repository you choose.

Expected normalized candle format:
{
    "time": 1710000000,
    "open": 1.0,
    "high": 1.1,
    "low": 0.9,
    "close": 1.05
}
"""

from typing import List, Dict, Any


class QuotexAdapter:
    def __init__(self, email: str, password: str, asset: str = "EURUSD"):
        self.email = email
        self.password = password
        self.asset = asset

    async def connect(self):
        """
        Connect/login using your selected community Quotex client.
        Implement the package-specific code here.
        """
        raise NotImplementedError(
            "Connect this adapter to the exact community Quotex client you use."
        )

    async def get_candles(self, seconds: int = 60, count: int = 200) -> List[Dict[str, Any]]:
        """
        Return normalized OHLC candles, oldest -> newest.
        """
        raise NotImplementedError(
            "Implement candle history using your selected community Quotex client."
        )

    async def close(self):
        pass
