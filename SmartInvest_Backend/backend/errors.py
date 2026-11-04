from flask import jsonify


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "status": "error",
            "message": "Endpoint tidak ditemukan."
        }), 404


    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "status": "error",
            "message": "Internal Server Error."
        }), 500


    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "status": "error",
            "message": "Bad Request."
        }), 400