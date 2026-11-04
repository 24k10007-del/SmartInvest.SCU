from flask import Blueprint, jsonify

from services.history_service import HistoryService

history_bp = Blueprint(

    "history",

    __name__,

    url_prefix="/api/history"

)


@history_bp.route("", methods=["GET"], strict_slashes=False)
def history():

    return jsonify(

        HistoryService.get_all()

    )