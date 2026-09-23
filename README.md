# Quotex Python Data + Signal Starter

This project is a starter architecture for collecting Quotex market candles through a
community/unofficial Python client, calculating indicators, and exposing the latest
analysis through a local FastAPI endpoint.

IMPORTANT:
- Quotex does not provide an official public trading-data API in this project.
- The Quotex adapter is intentionally isolated because community clients can change.
- Do not hard-code credentials. Use `.env`.
- This project is for data/analysis. It does not place trades.

## 1. Install

Windows:

    py -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

Linux/macOS:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Copy `.env.example` to `.env` and fill only your local credentials if your chosen
community Quotex client requires them.

## 2. Architecture

Quotex -> community WebSocket/client adapter -> OHLC candles -> pandas -> indicators
-> CALL/PUT/WAIT analysis -> FastAPI -> browser dashboard

## 3. Quotex adapter

`quotex_adapter.py` contains a clean interface. Because unofficial Quotex clients
have different APIs and may change, replace the adapter methods with the exact client
you have installed.

The rest of the project does not need to change.

## 4. Run API

    uvicorn app:app --reload

Open:

    http://127.0.0.1:8000/docs

The `/latest` endpoint returns the latest analysis.

## 5. Signal logic

The sample engine uses:
- EMA 20 / 50 / 200
- RSI 14
- MACD 12/26/9
- Bollinger Bands 20/2
- candle direction

It returns CALL, PUT or WAIT. This is an analytical example, not a guarantee of
profit or a recommendation to trade.

## 6. Connecting a specific community client

If you tell me the exact Quotex Python package/repository you want to use, I can wire
the adapter to that package's actual login, candle-history and live-candle methods.
