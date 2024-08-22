from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, Usuario

jwt = JWTManager()

class AuthResource:
    def __init__(self):
        self.api = Blueprint('auth_api', __name__)
        self._register_routes()

    def _register_routes(self):
        self.api.add_url_rule('/register/', 'register', self.register, methods=['POST'])
        self.api.add_url_rule('/login/', 'login', self.login, methods=['POST'])
        self.api.add_url_rule('/protected/', 'protected', self.protected, methods=['GET'])

    def register(self):
        data = request.json
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Missing username or password"}), 400

        if Usuario.query.filter_by(username=data['username']).first():
            return jsonify({"msg": "Username already exists"}), 400

        new_user = Usuario(username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User created successfully"}), 201

    def login(self):
        data = request.json
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Missing username or password"}), 400

        user = Usuario.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    @jwt_required()
    def protected(self):
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id), 200
