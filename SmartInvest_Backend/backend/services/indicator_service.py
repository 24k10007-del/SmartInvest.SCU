import pandas as pd
import ta


class IndicatorService:

    @staticmethod
    def calculate(history):

        df = history.copy()

        # SMA
        df["SMA20"] = ta.trend.sma_indicator(df["Close"], window=20)
        df["SMA50"] = ta.trend.sma_indicator(df["Close"], window=50)

        # EMA
        df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)

        # RSI
        df["RSI14"] = ta.momentum.rsi(df["Close"], window=14)

        # MACD
        macd = ta.trend.MACD(df["Close"])

        df["MACD"] = macd.macd()
        df["Signal"] = macd.macd_signal()
        df["Histogram"] = macd.macd_diff()

        latest = df.iloc[-1]

        return {

            "SMA20": round(float(latest["SMA20"]),2),

            "SMA50": round(float(latest["SMA50"]),2),

            "EMA20": round(float(latest["EMA20"]),2),

            "RSI14": round(float(latest["RSI14"]),2),

            "MACD": round(float(latest["MACD"]),2),

            "Signal": round(float(latest["Signal"]),2),

            "Histogram": round(float(latest["Histogram"]),2)

        }