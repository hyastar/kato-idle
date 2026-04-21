from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名/学号')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    nickname = db.Column(db.String(50), comment='昵称')
    email = db.Column(db.String(100), comment='邮箱')
    phone = db.Column(db.String(20), comment='手机号')
    avatar = db.Column(db.String(255), default='/static/uploads/default_avatar.png', comment='头像路径')
    campus = db.Column(db.String(50), comment='校区')
    dorm = db.Column(db.String(50), comment='宿舍号')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_private=False):
        data = {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname or self.username,
            'avatar': self.avatar,
            'campus': self.campus,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
        }
        if include_private:
            data.update({
                'email': self.email,
                'phone': self.phone,
                'dorm': self.dorm,
            })
        return data
