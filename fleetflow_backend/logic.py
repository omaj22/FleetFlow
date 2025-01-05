from flask import Blueprint, render_template, url_for, flash, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import database, user_table, create_user, read_user
import logging
from flask_cors import CORS

logic_bp = Blueprint('auth', __name__)
CORS(logic_bp, supports_credentials=True)

@logic_bp.route('/get_session', methods=["GET"])
def get_session():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({
            "session": user_id
        }), 200
    return jsonify({
        "error": "No Session Found"
    }), 404


@logic_bp.route('/signup', methods=["POST"])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        return jsonify({
            "message": "Fill all Fields",
            "status": "Bad Request",
            "code": 400
        }), 400
    
    try:
        hashed_password = generate_password_hash(password)
    except Exception as e:
        logging.error(f"Hashing the Password gives error: {e}")
    
    try:
        create_user(username, email, hashed_password)
        return jsonify({
            "status": "Success",
            "message": "User Created Successfully",
            "code": "200"
        }), 200
    except Exception as e:
        return jsonify({
            "message": "An error ocured while creating the user",
            "status": "Internal Server Error",
            "code": 500
        }), 500

@logic_bp.route('/login', methods=["POST"])
def login():
    all_users = read_user()
    username_email = request.form.get('username') or request.form.get('email')
    password = request.form.get('password')
    
    if not username_email or not password:
        return jsonify({
            'message': 'Fill all the enteries',
            'status': 'Bad Request',
            'code': 400
        }), 400


    try:
        for user in all_users:
            if (username_email == user['username'] or username_email == user['email']) and check_password_hash(user['password'], password) :
                session['user_id'] = user['username']
                return jsonify({
                    "message": f"User with ID {user['id']} has Logged in Successfully",
                    "status": "Success",
                    "code": 200
                }), 200
        else:
            return jsonify({
                "message": "Wrong Details",
                "status": "Unauthorized",
                "code": "401"
            }), 401
    except Exception as e:
        logging.error(f"Fail to log in because: {e}")
        return jsonify({
            "message": "An error occured during Login",
            "status": "Internal Server Error",
            "code": 500
        }), 500


@logic_bp.route('/logout')
def logout():
    session.clear()
    return jsonify({
        "message": "Session Logged Out Successfully"
    }), 200

@logic_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return jsonify({
            "message": "You must login before accessing this page",
            "status": "Unauthorized",
            "code": "401"
        }), 401
    else:
        return jsonify({
            "message": "Welcome to the dashboard",
            "status": "Success",
            "code": 200
        }), 200