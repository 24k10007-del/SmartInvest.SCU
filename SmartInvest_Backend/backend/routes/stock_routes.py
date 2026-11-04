from flask import Blueprint, jsonify

from services.recommendation_service import RecommendationService

from services.indicator_service import IndicatorService

from services.stock_service import StockService

from services.history_service import HistoryService

stock_bp = Blueprint(
    "stock",
    __name__,
    url_prefix="/api/stock"
)


@stock_bp.route("/company", methods=["GET"])
def company():

    return jsonify(
        StockService.get_company()
    )


@stock_bp.route("/current", methods=["GET"])
def current():

    return jsonify(
        StockService.get_current()
    )
    
@stock_bp.route("/analysis", methods=["GET"])
def analysis():

    history = StockService.get_history()

    indicators = IndicatorService.calculate(history)

    current = StockService.get_current()

    return jsonify({

        "symbol": current["symbol"],

        "currentPrice": current["currentPrice"],

        **indicators

    })
    
@stock_bp.route("/recommendation", methods=["GET"])
def recommendation():

    history = StockService.get_history()

    indicators = IndicatorService.calculate(history)

    current = StockService.get_current()

    data = {

        **current,

        **indicators

    }

    result = RecommendationService.generate(data)

    save_data = {

        **current,

        **result

    }

    HistoryService.save(save_data)

    return jsonify(result)