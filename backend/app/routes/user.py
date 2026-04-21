# app/routes/user.py
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.response import success, error
from app.utils.upload import save_upload_file

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error(msg="用户不存在", code=404)
    return success(data=user.to_dict(include_private=True))

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error(msg="用户不存在", code=404)

    data = request.get_json()

    if 'nickname' in data and data['nickname']:
        user.nickname = data['nickname']
    if 'email' in data:
        user.email = data.get('email', '')
    if 'phone' in data:
        user.phone = data.get('phone', '')
    if 'campus' in data:
        user.campus = data.get('campus', '')
    if 'dorm' in data:
        user.dorm = data.get('dorm', '')

    db.session.commit()
    return success(data=user.to_dict(include_private=True), msg="更新成功")

@user_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error(msg="用户不存在", code=404)

    if 'avatar' not in request.files:
        return error(msg="请选择要上传的头像图片")

    file = request.files['avatar']
    if not file.filename:
        return error(msg="请选择要上传的头像图片")

    avatar_path = save_upload_file(file)
    if not avatar_path:
        return error(msg="仅支持 png/jpg/jpeg/gif/webp 格式图片")

    user.avatar = avatar_path
    db.session.commit()
    return success(data={"avatar": avatar_path}, msg="头像上传成功")
