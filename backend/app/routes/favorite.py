# app/routes/favorite.py
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.favorite import Favorite
from app.models.item import Item
from app.utils.response import success, error

favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = int(get_jwt_identity())
    page = 1
    favs = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()
    return success(data=[f.to_dict() for f in favs])

@favorite_bp.route('/<int:item_id>', methods=['POST'])
@jwt_required()
def add_favorite(item_id):
    user_id = int(get_jwt_identity())

    item = Item.query.get(item_id)
    if not item:
        return error(msg="物品不存在", code=404)

    existing = Favorite.query.filter_by(user_id=user_id, item_id=item_id).first()
    if existing:
        return error(msg="已经收藏过了")

    fav = Favorite(user_id=user_id, item_id=item_id)
    db.session.add(fav)
    db.session.commit()
    return success(msg="收藏成功")

@favorite_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(item_id):
    user_id = int(get_jwt_identity())
    fav = Favorite.query.filter_by(user_id=user_id, item_id=item_id).first()
    if not fav:
        return error(msg="未收藏该物品")
    db.session.delete(fav)
    db.session.commit()
    return success(msg="已取消收藏")

@favorite_bp.route('/check/<int:item_id>', methods=['GET'])
@jwt_required()
def check_favorite(item_id):
    user_id = int(get_jwt_identity())
    exists = Favorite.query.filter_by(user_id=user_id, item_id=item_id).first()
    return success(data={"is_favorited": bool(exists)})
