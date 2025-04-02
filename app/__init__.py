from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# 初始化Flask应用
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invest_alert.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建定时任务调度器
scheduler = BackgroundScheduler()

# 导入视图和模型
from app.models import alert, stock
from app.controllers import alert_controller, stock_controller
from app.utils import stock_data

# 注册蓝图
app.register_blueprint(alert_controller.alert_bp)
app.register_blueprint(stock_controller.stock_bp) 