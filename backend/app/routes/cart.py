# app/routes/cart.py
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.cart import CartItem
from app.models.item import Item
from app.utils.response import success, error

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = int(get_jwt_identity())
    items = CartItem.query.filter_by(user_id=user_id).order_by(CartItem.created_at.desc()).all()
    return success(data={
        "items": [c.to_dict() for c in items],
        "total_count": len(items)
    })

@cart_bp.route('/<int:item_id>', methods=['POST'])
@jwt_required()
def add_to_cart(item_id):
    user_id = int(get_jwt_identity())

    item = Item.query.get(item_id)
    if not item:
        return error(msg="物品不存在", code=404)
    if item.status != 1:
        return error(msg="该物品已下架或已售出")

    existing = CartItem.query.filter_by(user_id=user_id, item_id=item_id).first()
    if existing:
        return error(msg="该物品已在购物车中")

    cart_item = CartItem(user_id=user_id, item_id=item_id)
    db.session.add(cart_item)
    db.session.commit()
    return success(msg="已加入购物车")

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = int(get_jwt_identity())
    cart_item = CartItem.query.filter_by(user_id=user_id, item_id=item_id).first()
    if not cart_item:
        return error(msg="购物车中没有该物品")
    db.session.delete(cart_item)
    db.session.commit()
    return success(msg="已从购物车移除")

@cart_bp.route('/', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = int(get_jwt_identity())
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return success(msg="购物车已清空")
