import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from apscheduler.schedulers.background import BackgroundScheduler # Removed APScheduler
import logging

# 加载环境变量 (可选, Vercel 会直接注入环境变量)
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)

# 配置数据库 - 从环境变量读取
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    # Vercel Postgres 使用 'postgres://' 而 SQLAlchemy 需要 'postgresql://'
    database_url = database_url.replace("postgres://", "postgresql://", 1)
elif not database_url:
    # 提供一个本地回退，以防万一，但在 Vercel 上 DATABASE_URL 必须设置
    print("警告: DATABASE_URL 环境变量未设置，将使用本地 SQLite 文件 (不适用于 Vercel)。")
    database_url = 'sqlite:///instance/invest_alert.db' # 注意路径可能需要调整
    # 确保 instance 文件夹存在 (仅本地需要)
    instance_path = os.path.join(app.instance_path)
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)


app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Vercel 通常不需要设置 SECRET_KEY 用于会话，除非你用了 Flask 的 session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_local_dev')

# 初始化数据库
db = SQLAlchemy(app)

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建定时任务调度器 - Removed APScheduler
# scheduler = BackgroundScheduler()

# 导入视图和模型 - 确保在 db 初始化之后导入
from app.models import alert, stock
from app.controllers import alert_controller, stock_controller # Removed cron_controller
from app.utils import stock_data

# 注册蓝图
app.register_blueprint(alert_controller.alert_bp)
app.register_blueprint(stock_controller.stock_bp)
# app.register_blueprint(cron_controller.cron_bp) # Removed cron blueprint registration

# 注意：在 Vercel 上，你不需要 app.run() 或者创建数据库表的代码在这里。
# Vercel 的构建过程或你的 wsgi.py 会处理启动。
# 数据库迁移/创建通常通过 Vercel 的部署钩子或手动完成。

# 本地开发时创建数据库表的辅助函数 (可选)
def create_tables_if_not_exist():
    with app.app_context():
        # 检查数据库连接和表是否存在可能更健壮
        # 但对于 SQLite，直接 create_all 通常是安全的
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            db.create_all()
            print("本地 SQLite 数据库表已检查/创建。")

# if __name__ == '__main__': # 这部分代码移到 wsgi.py 或本地运行脚本
#    create_tables_if_not_exist()
#    app.run(debug=True) 