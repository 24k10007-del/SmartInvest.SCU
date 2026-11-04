class RecommendationService:
    
    @staticmethod
    def generate(data):

        score = 0
        reason = []

        # RSI
        if data["RSI14"] < 30:
            score += 25
            reason.append("RSI Oversold (peluang rebound)")

        elif data["RSI14"] < 70:
            score += 15
            reason.append("RSI masih berada di area sehat")

        else:
            score -= 15
            reason.append("RSI Overbought")

        # EMA
        if data["currentPrice"] > data["EMA20"]:
            score += 20
            reason.append("Harga di atas EMA20")

        else:
            score -= 10
            reason.append("Harga di bawah EMA20")

        # SMA
        if data["SMA20"] > data["SMA50"]:
            score += 20
            reason.append("SMA20 berada di atas SMA50")

        else:
            score -= 10
            reason.append("SMA20 berada di bawah SMA50")

        # MACD
        if data["MACD"] > data["Signal"]:
            score += 20
            reason.append("MACD Bullish")

        else:
            score -= 10
            reason.append("MACD Bearish")

        # Trend harga
        if data["currentPrice"] > data["SMA20"]:
            score += 15
            reason.append("Harga berada di atas SMA20")

        else:
            score -= 10
            reason.append("Harga berada di bawah SMA20")

        # Rekomendasi
        if score >= 60:
            recommendation = "BUY"
            confidence = "High"

        elif score >= 35:
            recommendation = "HOLD"
            confidence = "Medium"

        else:
            recommendation = "SELL"
            confidence = "High"

        return {
            "recommendation": recommendation,
            "score": score,
            "confidence": confidence,
            "reason": reason
        }