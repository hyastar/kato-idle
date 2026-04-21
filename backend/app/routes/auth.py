# app/routes/auth.py
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.response import success, error

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    nickname = data.get('nickname', username)
    email = data.get('email', '')

    if not username or not password:
        return error(msg="用户名和密码不能为空")
    if len(password) < 6:
        return error(msg="密码长度至少6位")

    if User.query.filter_by(username=username).first():
        return error(msg="该用户名已被注册")

    user = User(username=username, nickname=nickname, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))

    return success(
        data={"token": token, "user": user.to_dict()},
        msg="注册成功",
        code=201
    )

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return error(msg="用户名和密码不能为空")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return error(msg="用户名或密码错误")

    if not user.is_active:
        return error(msg="账号已被禁用")

    token = create_access_token(identity=str(user.id))

    return success(data={"token": token, "user": user.to_dict()})

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error(msg="用户不存在", code=404)
    return success(data=user.to_dict(include_private=True))
