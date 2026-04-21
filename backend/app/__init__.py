from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.routes.auth import auth_bp
    from app.routes.items import items_bp
    from app.routes.user import user_bp
    from app.routes.cart import cart_bp
    from app.routes.favorite import favorite_bp
    from app.routes.categories import categories_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(favorite_bp, url_prefix='/api/favorite')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"code": 404, "msg": "接口不存在", "data": None}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"code": 500, "msg": "服务器内部错误", "data": None}), 500

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"code": 413, "msg": "上传文件太大（最大16MB）", "data": None}), 413

    return app
