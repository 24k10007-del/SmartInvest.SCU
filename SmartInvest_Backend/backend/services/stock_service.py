import yfinance as yf


class StockService:

    SYMBOL = "TLKM.JK"

    @staticmethod
    def get_company():

        stock = yf.Ticker(StockService.SYMBOL)

        info = stock.info

        return {
            "company": info.get("longName"),
            "symbol": StockService.SYMBOL,
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "website": info.get("website")
        }

    @staticmethod
    def get_current():

        stock = yf.Ticker(StockService.SYMBOL)

        info = stock.info

        return {

            "symbol": StockService.SYMBOL,

            "currentPrice": info.get("currentPrice"),

            "open": info.get("open"),

            "dayHigh": info.get("dayHigh"),

            "dayLow": info.get("dayLow"),

            "volume": info.get("volume"),

            "previousClose": info.get("previousClose")

        }

    @staticmethod
    def get_history():

        stock = yf.Ticker(StockService.SYMBOL)

        history = stock.history(period="6mo")

        return history