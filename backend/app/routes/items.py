# app/routes/items.py
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.item import Item
from app.models.category import Category
from app.utils.response import success, error
from app.utils.upload import save_multiple_files
from sqlalchemy import or_

items_bp = Blueprint('items', __name__)

@items_bp.route('/', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    keyword = request.args.get('keyword', '')
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    condition = request.args.get('condition', type=int)
    sort = request.args.get('sort', 'newest')

    query = Item.query.filter(Item.status == 1)

    if keyword:
        query = query.filter(or_(
            Item.title.like(f'%{keyword}%'),
            Item.description.like(f'%{keyword}%')
        ))
    if category_id:
        query = query.filter(Item.category_id == category_id)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    if condition:
        query = query.filter(Item.condition == condition)

    if sort == 'price_asc':
        query = query.order_by(Item.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Item.price.desc())
    elif sort == 'popular':
        query = query.order_by(Item.view_count.desc())
    else:
        query = query.order_by(Item.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return success(data={
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    })

@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item_detail(item_id):
    item = Item.query.get(item_id)
    if not item:
        return error(msg="物品不存在", code=404)
    item.view_count += 1
    db.session.commit()
    return success(data=item.to_dict(detail=True))

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    user_id = int(get_jwt_identity())

    title = request.form.get('title')
    price = request.form.get('price')
    category_id = request.form.get('category_id')

    if not title:
        return error(msg="物品名称不能为空")
    if not price:
        return error(msg="价格不能为空")

    files = request.files.getlist('images')
    image_paths = save_multiple_files(files)

    item = Item(
        title=title,
        description=request.form.get('description', ''),
        price=float(request.form.get('price')),
        original_price=float(request.form.get('original_price')) if request.form.get('original_price') else None,
        category_id=int(category_id) if category_id else None,
        condition=int(request.form.get('condition', 1)),
        contact=request.form.get('contact', ''),
        location=request.form.get('location', ''),
        images=','.join(image_paths),
        user_id=user_id,
    )
    db.session.add(item)
    db.session.commit()

    return success(data=item.to_dict(), msg="发布成功", code=201)

@items_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    user_id = int(get_jwt_identity())
    item = Item.query.get(item_id)

    if not item:
        return error(msg="物品不存在", code=404)
    if item.user_id != user_id:
        return error(msg="无权修改", code=403)

    title = request.form.get('title')
    if title:
        item.title = title
    if request.form.get('price'):
        item.price = float(request.form.get('price'))
    if request.form.get('description'):
        item.description = request.form.get('description')
    if request.form.get('category_id'):
        item.category_id = int(request.form.get('category_id'))
    if request.form.get('condition'):
        item.condition = int(request.form.get('condition'))
    if request.form.get('contact'):
        item.contact = request.form.get('contact')
    if request.form.get('location'):
        item.location = request.form.get('location')
    if request.form.get('status'):
        item.status = int(request.form.get('status'))

    files = request.files.getlist('images')
    if files and files[0].filename:
        image_paths = save_multiple_files(files)
        item.images = ','.join(image_paths)

    db.session.commit()
    return success(data=item.to_dict(), msg="更新成功")

@items_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    user_id = int(get_jwt_identity())
    item = Item.query.get(item_id)

    if not item:
        return error(msg="物品不存在", code=404)
    if item.user_id != user_id:
        return error(msg="无权删除", code=403)

    db.session.delete(item)
    db.session.commit()
    return success(msg="删除成功")

@items_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_items():
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    status = request.args.get('status', type=int)

    query = Item.query.filter_by(user_id=user_id)
    if status is not None:
        query = query.filter_by(status=status)

    pagination = query.order_by(Item.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return success(data={
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    })
