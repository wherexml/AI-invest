from app import db
from datetime import datetime

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 类型: price, change_percent, volume, etc.
    condition = db.Column(db.String(10), nullable=False)  # 条件: >, <, >=, <=, ==
    value = db.Column(db.Float, nullable=False)  # 条件值
    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    is_triggered = db.Column(db.Boolean, default=False)  # 是否已触发
    last_triggered = db.Column(db.DateTime, nullable=True)  # 最后触发时间
    created_at = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间

    def __repr__(self):
        return f"<Alert {self.id}: {self.stock.code} {self.type} {self.condition} {self.value}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'stock_id': self.stock_id,
            'stock_code': self.stock.code if self.stock else None,
            'stock_name': self.stock.name if self.stock else None,
            'type': self.type,
            'condition': self.condition,
            'value': self.value,
            'is_active': self.is_active,
            'is_triggered': self.is_triggered,
            'last_triggered': self.last_triggered.strftime('%Y-%m-%d %H:%M:%S') if self.last_triggered else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 