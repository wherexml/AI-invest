from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import akshare as ak
import pandas as pd
import logging
from app import db
from app.models.stock import Stock
from app.utils.stock_data import update_stock, get_stock_history

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')
logger = logging.getLogger(__name__)

@stock_bp.route('/')
def index():
    """股票列表页"""
    stocks = Stock.query.all()
    return render_template('stock/index.html', stocks=stocks)

@stock_bp.route('/add', methods=['GET', 'POST'])
def add():
    """添加股票"""
    if request.method == 'POST':
        code = request.form.get('code')
        market = request.form.get('market')
        
        # 检查股票是否已存在
        existing = Stock.query.filter_by(code=code).first()
        if existing:
            return jsonify({'success': False, 'message': '股票已存在'})
        
        # 根据市场类型获取股票信息
        try:
            if market == 'A股':
                # 获取A股数据
                df = ak.stock_zh_a_spot_em()
                stock_info = df[df['代码'] == code]
                if stock_info.empty:
                    return jsonify({'success': False, 'message': '未找到该A股股票'})
                
                name = stock_info.iloc[0]['名称']
                price = float(stock_info.iloc[0]['最新价'])
                
            elif market == '港股':
                # 获取港股数据
                df = ak.stock_hk_spot_em()
                stock_info = df[df['代码'] == code]
                if stock_info.empty:
                    return jsonify({'success': False, 'message': '未找到该港股股票'})
                
                name = stock_info.iloc[0]['名称']
                price = float(stock_info.iloc[0]['最新价'])
            
            else:
                return jsonify({'success': False, 'message': '不支持的市场类型'})
            
            # 创建股票记录
            stock = Stock(
                code=code,
                name=name,
                market=market,
                price=price
            )
            db.session.add(stock)
            db.session.commit()
            
            # 更新完整股票信息
            update_stock(stock)
            
            return jsonify({'success': True, 'message': '添加成功', 'stock': stock.to_dict()})
        
        except Exception as e:
            logger.error(f"添加股票出错: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'message': f'添加失败: {str(e)}'})
    
    return render_template('stock/add.html')

@stock_bp.route('/<int:stock_id>')
def detail(stock_id):
    """股票详情页"""
    stock = Stock.query.get_or_404(stock_id)
    
    # 获取历史数据
    history_df = get_stock_history(stock.code, stock.market, days=30)
    
    # 将历史数据转为列表
    history = []
    if not history_df.empty:
        for _, row in history_df.iterrows():
            history.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'open': float(row['open']),
                'close': float(row['close']),
                'high': float(row['high']),
                'low': float(row['low']),
                'volume': float(row['volume']),
                'change_percent': float(row['change_percent'])
            })
    
    return render_template('stock/detail.html', stock=stock, history=history)

@stock_bp.route('/update/<int:stock_id>')
def update(stock_id):
    """手动更新股票信息"""
    stock = Stock.query.get_or_404(stock_id)
    
    try:
        update_stock(stock)
        return jsonify({'success': True, 'message': '更新成功', 'stock': stock.to_dict()})
    except Exception as e:
        logger.error(f"更新股票出错: {str(e)}")
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'})

@stock_bp.route('/delete/<int:stock_id>', methods=['POST'])
def delete(stock_id):
    """删除股票"""
    stock = Stock.query.get_or_404(stock_id)
    
    try:
        db.session.delete(stock)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        logger.error(f"删除股票出错: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

@stock_bp.route('/search', methods=['POST'])
def search():
    """搜索股票"""
    keyword = request.form.get('keyword', '')
    market = request.form.get('market', 'A股')
    
    try:
        if market == 'A股':
            # 搜索A股
            df = ak.stock_zh_a_spot_em()
            result = df[(df['代码'].str.contains(keyword)) | (df['名称'].str.contains(keyword))]
            
        elif market == '港股':
            # 搜索港股
            df = ak.stock_hk_spot_em()
            result = df[(df['代码'].str.contains(keyword)) | (df['名称'].str.contains(keyword))]
            
        else:
            return jsonify({'success': False, 'message': '不支持的市场类型'})
        
        # 转换为列表
        stocks = []
        for _, row in result.iterrows():
            stocks.append({
                'code': row['代码'],
                'name': row['名称'],
                'price': float(row['最新价']),
                'change_percent': float(row['涨跌幅'])
            })
        
        return jsonify({'success': True, 'stocks': stocks})
    
    except Exception as e:
        logger.error(f"搜索股票出错: {str(e)}")
        return jsonify({'success': False, 'message': f'搜索失败: {str(e)}'}) 