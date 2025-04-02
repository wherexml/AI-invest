from app import db
from datetime import datetime

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # 股票代码
    name = db.Column(db.String(100), nullable=False)  # 股票名称
    market = db.Column(db.String(10), nullable=False)  # 市场: A股/港股
    price = db.Column(db.Float, nullable=True)  # 当前价格
    change_percent = db.Column(db.Float, nullable=True)  # 涨跌幅
    volume = db.Column(db.Float, nullable=True)  # 成交量
    turnover = db.Column(db.Float, nullable=True)  # 成交额
    pe_ratio = db.Column(db.Float, nullable=True)  # 市盈率
    pb_ratio = db.Column(db.Float, nullable=True)  # 市净率
    last_update = db.Column(db.DateTime, default=datetime.now)  # 最后更新时间
    alerts = db.relationship('Alert', backref='stock', lazy=True)

    def __repr__(self):
        return f"<Stock {self.code}: {self.name} - {self.price}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'market': self.market,
            'price': self.price,
            'change_percent': self.change_percent,
            'volume': self.volume,
            'turnover': self.turnover,
            'pe_ratio': self.pe_ratio,
            'pb_ratio': self.pb_ratio,
            'last_update': self.last_update.strftime('%Y-%m-%d %H:%M:%S') if self.last_update else None
        } 