from app import create_app, db

app = create_app()

def init_categories():
    """初始化分类数据（只在没有数据时执行）"""
    from app.models.category import Category
    if Category.query.count() == 0:
        categories = [
            Category(name='教材书籍', icon='Reading', sort_order=1),
            Category(name='电子产品', icon='Monitor', sort_order=2),
            Category(name='生活用品', icon='House', sort_order=3),
            Category(name='服装鞋包', icon='Goods', sort_order=4),
            Category(name='运动器材', icon='Football', sort_order=5),
            Category(name='数码配件', icon='Camera', sort_order=6),
            Category(name='学习文具', icon='Edit', sort_order=7),
            Category(name='其他', icon='More', sort_order=8),
        ]
        db.session.add_all(categories)
        db.session.commit()
        print("分类数据初始化完成")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_categories()
        print("数据库表已初始化")
    app.run(debug=True, host='0.0.0.0', port=5000)
