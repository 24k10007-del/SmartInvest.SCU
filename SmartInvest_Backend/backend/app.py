from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database import db

from models.user import User

from routes.auth_routes import auth_bp
from routes.stock_routes import stock_bp
from routes.dashboard_routes import dashboard_bp
from models.history import History
from routes.history_routes import history_bp
from routes.export_routes import export_bp
from errors import register_error_handlers

from logger import logger


app = Flask(__name__)


# Load Config
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Init Database
db.init_app(app)

# Init JWT
jwt = JWTManager(app)

register_error_handlers(app)

# Logger
@app.before_request
def before():
    logger.info(f"{request.method} {request.path}")

# Register Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(history_bp)
app.register_blueprint(export_bp)

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "FinTech Stock Backend Running 🚀"
    }
    
@app.route("/api/health")
def health():
    return {
        "status": "ok",
        "service": "FinTech Stock Backend",
        "database": "connected",
        "version": "1.0.0",
        "author": "Mario Saputra"
    }, 200

@app.route("/api")
def api():

    return {

        "project": "Financial Technology",

        "company": "PT Telkom Indonesia (Persero) Tbk",

        "backend": "Flask",

        "database": "MySQL",

        "version": "1.0.0",

        "developer": "Mario Saputra"

    }
    
@app.route("/api/info")
def info():

    return {

        "stock": "TLKM.JK",

        "analysis": "Technical Indicator",

        "recommendation": "BUY / HOLD / SELL",

        "market": "Indonesia Stock Exchange"

    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    
