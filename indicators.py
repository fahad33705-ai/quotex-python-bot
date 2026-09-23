import numpy as np
import pandas as pd


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    close = df["close"]
    high = df["high"]
    low = df["low"]

    df["ema20"] = close.ewm(span=20, adjust=False).mean()
    df["ema50"] = close.ewm(span=50, adjust=False).mean()
    df["ema200"] = close.ewm(span=200, adjust=False).mean()

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi14"] = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    df["bb_mid"] = mid
    df["bb_upper"] = mid + 2 * std
    df["bb_lower"] = mid - 2 * std

    return df


def analyze(df: pd.DataFrame) -> dict:
    if len(df) < 50:
        return {"signal": "WAIT", "confidence": 0, "reason": "Not enough candles"}

    d = add_indicators(df)
    x = d.iloc[-1]

    score_call = 0
    score_put = 0
    reasons = []

    if x["close"] > x["ema20"] > x["ema50"]:
        score_call += 1
        reasons.append("EMA bullish")
    elif x["close"] < x["ema20"] < x["ema50"]:
        score_put += 1
        reasons.append("EMA bearish")

    if x["rsi14"] < 35:
        score_call += 1
        reasons.append("RSI oversold")
    elif x["rsi14"] > 65:
        score_put += 1
        reasons.append("RSI overbought")

    if x["macd"] > x["macd_signal"]:
        score_call += 1
        reasons.append("MACD bullish")
    elif x["macd"] < x["macd_signal"]:
        score_put += 1
        reasons.append("MACD bearish")

    if x["close"] <= x["bb_lower"]:
        score_call += 1
        reasons.append("Lower-band rejection zone")
    elif x["close"] >= x["bb_upper"]:
        score_put += 1
        reasons.append("Upper-band rejection zone")

    if x["close"] > x["open"]:
        score_call += 1
    elif x["close"] < x["open"]:
        score_put += 1

    total = max(score_call, score_put)
    confidence = round(total / 5 * 100)

    if score_call >= 3 and score_call > score_put:
        signal = "CALL"
    elif score_put >= 3 and score_put > score_call:
        signal = "PUT"
    else:
        signal = "WAIT"

    return {
        "signal": signal,
        "confidence": confidence,
        "close": float(x["close"]),
        "rsi": round(float(x["rsi14"]), 2) if pd.notna(x["rsi14"]) else None,
        "ema20": float(x["ema20"]),
        "ema50": float(x["ema50"]),
        "ema200": float(x["ema200"]),
        "macd": float(x["macd"]),
        "macd_signal": float(x["macd_signal"]),
        "reason": ", ".join(reasons[-4:]),
    }
