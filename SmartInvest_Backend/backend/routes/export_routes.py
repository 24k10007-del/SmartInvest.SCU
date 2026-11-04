from flask import Blueprint, send_file

from services.stock_service import StockService
from services.indicator_service import IndicatorService
from services.recommendation_service import RecommendationService
from services.pdf_service import PDFService

export_bp = Blueprint(
    "export",
    __name__,
    url_prefix="/api/export"
)


@export_bp.route("/pdf", methods=["GET"])
def export_pdf():

    history = StockService.get_history()

    indicators = IndicatorService.calculate(history)

    current = StockService.get_current()

    data = {
        **current,
        **indicators
    }

    recommendation = RecommendationService.generate(data)

    pdf_data = {
        **current,
        **indicators,
        **recommendation
    }

    filename = PDFService.generate(pdf_data)

    return send_file(
        filename,
        as_attachment=True
    )