from app import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'item_id', name='uq_user_item_favorite'),
    )

    user = db.relationship('User', backref='favorites')
    item = db.relationship('Item', backref='favorited_by')

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item': self.item.to_dict() if self.item else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }
