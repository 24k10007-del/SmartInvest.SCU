from services.stock_service import StockService
from services.indicator_service import IndicatorService
from services.recommendation_service import RecommendationService
from services.history_service import HistoryService


class DashboardService:

    @staticmethod
    def get_dashboard():

        company = StockService.get_company()

        current = StockService.get_current()

        history = StockService.get_history()

        analysis = IndicatorService.calculate(history)

        recommendation = RecommendationService.generate({

            **current,

            **analysis

        })
        
        HistoryService.save({

            "symbol": company["symbol"],

            "currentPrice": current["currentPrice"],

            "recommendation": recommendation["recommendation"],

            "score": recommendation["score"],

            "confidence": recommendation["confidence"]

        })

        return {

            "company": company,

            "current": current,

            "analysis": analysis,

            "recommendation": recommendation

        }