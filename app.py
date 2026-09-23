import os
from datetime import datetime, timezone

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI

from indicators import analyze
from quotex_adapter import QuotexAdapter

load_dotenv()

app = FastAPI(title="Quotex Python Signal API")

adapter = QuotexAdapter(
    email=os.getenv("QUOTEX_EMAIL", ""),
    password=os.getenv("QUOTEX_PASSWORD", ""),
    asset=os.getenv("QUOTEX_ASSET", "EURUSD"),
)


@app.get("/")
async def root():
    return {
        "name": "Quotex Python Signal API",
        "status": "ready",
        "note": "Connect quotex_adapter.py to your selected community client."
    }


@app.get("/latest")
async def latest():
    seconds = int(os.getenv("CANDLE_SECONDS", "60"))
    count = int(os.getenv("HISTORY_SIZE", "200"))

    candles = await adapter.get_candles(seconds=seconds, count=count)
    df = pd.DataFrame(candles)

    result = analyze(df)
    result["asset"] = adapter.asset
    result["candle_seconds"] = seconds
    result["server_time"] = datetime.now(timezone.utc).isoformat()

    return result
