from app import db
from datetime import datetime

CONDITION_TEXT = {
    1: '全新',
    2: '几乎全新',
    3: '有使用痕迹',
    4: '功能完好',
    5: '有明显磨损',
}

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, comment='物品名称')
    description = db.Column(db.Text, comment='物品描述')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='价格')
    original_price = db.Column(db.Numeric(10, 2), comment='原价（可选）')
    condition = db.Column(db.Integer, default=1, comment='新旧程度 1-5')
    images = db.Column(db.Text, comment='图片路径，逗号分隔')
    contact = db.Column(db.String(100), comment='联系方式')
    location = db.Column(db.String(100), comment='交易地点')
    status = db.Column(db.Integer, default=1, comment='状态: 1在售 2已售 0下架')
    view_count = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='items', lazy='joined')
    category = db.relationship('Category', backref='items', lazy='joined')

    def get_images_list(self):
        return self.images.split(',') if self.images else []

    def to_dict(self, detail=False):
        data = {
            'id': self.id,
            'title': self.title,
            'price': float(self.price) if self.price else 0,
            'original_price': float(self.original_price) if self.original_price else None,
            'condition': self.condition,
            'condition_text': CONDITION_TEXT.get(self.condition, '未知'),
            'images': self.get_images_list(),
            'cover': self.get_images_list()[0] if self.get_images_list() else None,
            'status': self.status,
            'view_count': self.view_count,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }
        if detail:
            data.update({
                'description': self.description,
                'contact': self.contact,
                'location': self.location,
                'user': self.user.to_dict() if self.user else None,
            })
        return data
