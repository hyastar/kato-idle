from app import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'item_id', name='uq_user_item_cart'),
    )

    user = db.relationship('User', backref='cart_items')
    item = db.relationship('Item', backref='in_carts')

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item': self.item.to_dict() if self.item else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }
