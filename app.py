import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import datetime
import time
import logging
from dotenv import load_dotenv

# 初始化Flask应用
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invest_alert.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入模型和控制器 (将在后面创建)
from app.models.alert import Alert
from app.models.stock import Stock
from app.controllers.alert_controller import alert_bp
from app.controllers.stock_controller import stock_bp
from app.utils.stock_data import update_all_stocks, check_alerts

# 注册蓝图
app.register_blueprint(alert_bp)
app.register_blueprint(stock_bp)

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 创建定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(update_all_stocks, 'interval', minutes=5)
scheduler.add_job(check_alerts, 'interval', minutes=1)

# 启动应用
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建数据库表
    
    # 启动定时任务
    scheduler.start()
    
    # 启动Flask应用
    app.run(debug=True) 