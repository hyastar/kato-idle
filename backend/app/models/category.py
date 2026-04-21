from app import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, comment='分类名称')
    icon = db.Column(db.String(100), comment='分类图标（Element Plus 图标名）')
    sort_order = db.Column(db.Integer, default=0, comment='排序权重')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'sort_order': self.sort_order,
        }
