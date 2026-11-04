from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt

from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")

    if not fullname or not email or not password:
        return jsonify({
            "status": "error",
            "message": "Semua field wajib diisi."
        }), 400

    existing = User.query.filter_by(email=email).first()

    if existing:
        return jsonify({
            "status": "error",
            "message": "Email sudah digunakan."
        }), 409

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        fullname=fullname,
        email=email,
        password=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Register berhasil."
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "status": "error",
            "message": "Email tidak ditemukan."
        }), 401

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        return jsonify({
            "status": "error",
            "message": "Password salah."
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "status": "success",
        "token": token,
        "user": {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email
        }
    })