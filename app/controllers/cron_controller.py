import os
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from app.utils.stock_data import update_all_stocks, check_alerts as check_alerts_util # 重命名导入以避免名称冲突

cron_bp = Blueprint('cron', __name__, url_prefix='/api/cron')

# --- 安全装饰器 ---
def require_cron_secret(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求参数或环境变量获取期望的 Secret
        expected_secret = os.environ.get('CRON_SECRET')
        provided_secret = request.args.get('secret')

        # 如果未设置环境变量或未提供 secret 或 secret 不匹配
        if not expected_secret or not provided_secret or expected_secret != provided_secret:
            current_app.logger.warning(f"Cron endpoint {request.path} called with invalid or missing secret.")
            return jsonify(message="Unauthorized"), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Cron Job 端点 ---
@cron_bp.route('/update_stocks', methods=['POST', 'GET']) # Vercel Cron 通常用 GET，但允许 POST 可能方便测试
@require_cron_secret
def trigger_update_stocks():
    """触发所有股票数据的更新。"""
    current_app.logger.info("Cron job: 开始更新所有股票数据...")
    try:
        update_all_stocks()
        current_app.logger.info("Cron job: 股票数据更新成功。")
        return jsonify(message="Stock update started successfully."), 200
    except Exception as e:
        current_app.logger.error(f"Cron job: 更新股票数据时出错: {e}", exc_info=True)
        return jsonify(message=f"Error starting stock update: {e}"), 500

@cron_bp.route('/check_alerts', methods=['POST', 'GET'])
@require_cron_secret
def trigger_check_alerts():
    """触发警报检查。"""
    current_app.logger.info("Cron job: 开始检查警报...")
    try:
        # 注意：check_alerts_util 可能需要 app context 来访问数据库
        # 在 Flask 1.1+ 中，视图函数自动具有应用上下文
        # 如果在 check_alerts_util 内部需要，确保它使用了 with app.app_context():
        check_alerts_util()
        current_app.logger.info("Cron job: 警报检查成功。")
        return jsonify(message="Alert check started successfully."), 200
    except Exception as e:
        current_app.logger.error(f"Cron job: 检查警报时出错: {e}", exc_info=True)
        return jsonify(message=f"Error starting alert check: {e}"), 500

# 可以在这里添加其他需要的定时任务端点 