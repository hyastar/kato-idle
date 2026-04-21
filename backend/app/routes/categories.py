# app/routes/categories.py
from flask import Blueprint
from app.models.category import Category
from app.utils.response import success

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.sort_order.asc()).all()
    return success(data=[c.to_dict() for c in categories])
