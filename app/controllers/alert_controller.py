from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import logging
from app import db
from app.models.alert import Alert
from app.models.stock import Stock
from app.utils.stock_data import check_alert_condition

alert_bp = Blueprint('alert', __name__, url_prefix='/alert')
logger = logging.getLogger(__name__)

@alert_bp.route('/')
def index():
    """提醒列表页"""
    alerts = Alert.query.all()
    return render_template('alert/index.html', alerts=alerts)

@alert_bp.route('/add', methods=['GET', 'POST'])
def add():
    """添加提醒"""
    if request.method == 'POST':
        stock_id = request.form.get('stock_id')
        alert_type = request.form.get('type')
        condition = request.form.get('condition')
        value = request.form.get('value')
        
        # 参数验证
        if not all([stock_id, alert_type, condition, value]):
            return jsonify({'success': False, 'message': '参数不完整'})
        
        try:
            stock = Stock.query.get(stock_id)
            if not stock:
                return jsonify({'success': False, 'message': '股票不存在'})
            
            # 验证提醒类型
            valid_types = ['price', 'change_percent', 'volume', 'turnover', 'pe_ratio', 'pb_ratio']
            if alert_type not in valid_types:
                return jsonify({'success': False, 'message': '不支持的提醒类型'})
            
            # 验证条件
            valid_conditions = ['>', '<', '>=', '<=', '==']
            if condition not in valid_conditions:
                return jsonify({'success': False, 'message': '不支持的条件类型'})
            
            # 创建提醒
            alert = Alert(
                stock_id=stock_id,
                type=alert_type,
                condition=condition,
                value=float(value),
                is_active=True,
                is_triggered=False
            )
            
            db.session.add(alert)
            db.session.commit()
            
            # 立即检查提醒条件
            is_triggered = check_alert_condition(alert)
            if is_triggered:
                alert.is_triggered = True
                db.session.commit()
            
            return jsonify({'success': True, 'message': '添加成功', 'alert': alert.to_dict()})
        
        except Exception as e:
            logger.error(f"添加提醒出错: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'message': f'添加失败: {str(e)}'})
    
    # GET请求
    stocks = Stock.query.all()
    return render_template('alert/add.html', stocks=stocks)

@alert_bp.route('/<int:alert_id>')
def detail(alert_id):
    """提醒详情页"""
    alert = Alert.query.get_or_404(alert_id)
    return render_template('alert/detail.html', alert=alert)

@alert_bp.route('/toggle/<int:alert_id>', methods=['POST'])
def toggle(alert_id):
    """启用/禁用提醒"""
    alert = Alert.query.get_or_404(alert_id)
    
    try:
        alert.is_active = not alert.is_active
        db.session.commit()
        return jsonify({'success': True, 'message': '状态已更新', 'is_active': alert.is_active})
    except Exception as e:
        logger.error(f"切换提醒状态出错: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'})

@alert_bp.route('/reset/<int:alert_id>', methods=['POST'])
def reset(alert_id):
    """重置已触发的提醒"""
    alert = Alert.query.get_or_404(alert_id)
    
    try:
        alert.is_triggered = False
        db.session.commit()
        return jsonify({'success': True, 'message': '提醒已重置'})
    except Exception as e:
        logger.error(f"重置提醒出错: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'重置失败: {str(e)}'})

@alert_bp.route('/delete/<int:alert_id>', methods=['POST'])
def delete(alert_id):
    """删除提醒"""
    alert = Alert.query.get_or_404(alert_id)
    
    try:
        db.session.delete(alert)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        logger.error(f"删除提醒出错: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'}) 