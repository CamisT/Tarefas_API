from flask import jsonify, current_app
from models import db

def setup_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(error):
        current_app.logger.error(f"Bad Request: {error}")
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found_error(error):
        current_app.logger.error(f"Not Found: {error}")
        return jsonify({"error": "Resource Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        current_app.logger.error(f"Server Error: {error}")
        db.session.rollback()
        return jsonify({"error": "Internal Server Error"}), 500
