import akshare as ak
import pandas as pd
from datetime import datetime
import time
import logging
from app import db
from app.models.stock import Stock
from app.models.alert import Alert

logger = logging.getLogger(__name__)

def get_a_stock_data(code):
    """获取A股实时数据"""
    try:
        # 获取个股实时行情
        df = ak.stock_zh_a_spot_em()
        # 查找指定代码的股票
        stock_data = df[df['代码'] == code].iloc[0] if not df[df['代码'] == code].empty else None
        
        if stock_data is not None:
            return {
                'code': code,
                'name': stock_data['名称'],
                'price': float(stock_data['最新价']),
                'change_percent': float(stock_data['涨跌幅']),
                'volume': float(stock_data['成交量']),
                'turnover': float(stock_data['成交额']),
                'pe_ratio': float(stock_data['市盈率']) if '市盈率' in stock_data and pd.notna(stock_data['市盈率']) else None,
                'pb_ratio': float(stock_data['市净率']) if '市净率' in stock_data and pd.notna(stock_data['市净率']) else None,
                'last_update': datetime.now()
            }
        return None
    except Exception as e:
        logger.error(f"获取A股数据出错: {code}, 错误: {str(e)}")
        return None

def get_hk_stock_data(code):
    """获取港股实时数据"""
    try:
        # 获取港股实时行情
        df = ak.stock_hk_spot_em()
        # 港股代码需要处理前导0
        if not code.startswith('0'):
            code_to_search = code
        else:
            code_to_search = code
        
        stock_data = df[df['代码'] == code_to_search].iloc[0] if not df[df['代码'] == code_to_search].empty else None
        
        if stock_data is not None:
            return {
                'code': code,
                'name': stock_data['名称'],
                'price': float(stock_data['最新价']),
                'change_percent': float(stock_data['涨跌幅']),
                'volume': float(stock_data['成交量']),
                'turnover': float(stock_data['成交额']),
                'pe_ratio': float(stock_data['市盈率']) if '市盈率' in stock_data and pd.notna(stock_data['市盈率']) else None,
                'pb_ratio': float(stock_data['市净率']) if '市净率' in stock_data and pd.notna(stock_data['市净率']) else None,
                'last_update': datetime.now()
            }
        return None
    except Exception as e:
        logger.error(f"获取港股数据出错: {code}, 错误: {str(e)}")
        return None

def update_stock(stock):
    """更新单个股票数据"""
    try:
        if stock.market == 'A股':
            data = get_a_stock_data(stock.code)
        elif stock.market == '港股':
            data = get_hk_stock_data(stock.code)
        else:
            logger.error(f"未知市场类型: {stock.market}")
            return
        
        if data:
            stock.price = data['price']
            stock.change_percent = data['change_percent']
            stock.volume = data['volume']
            stock.turnover = data['turnover']
            stock.pe_ratio = data['pe_ratio']
            stock.pb_ratio = data['pb_ratio']
            stock.last_update = data['last_update']
            db.session.commit()
            logger.info(f"已更新股票: {stock.code} {stock.name}, 价格: {stock.price}")
        else:
            logger.warning(f"无法获取股票数据: {stock.code} {stock.name}")
    except Exception as e:
        logger.error(f"更新股票出错: {stock.code}, 错误: {str(e)}")
        db.session.rollback()

def update_all_stocks():
    """更新所有股票数据"""
    logger.info("开始更新所有股票...")
    stocks = Stock.query.all()
    for stock in stocks:
        update_stock(stock)
        # 防止请求频率过高
        time.sleep(0.5)
    logger.info(f"股票更新完成, 共 {len(stocks)} 只")

def check_alert_condition(alert):
    """检查警报条件是否满足"""
    stock = alert.stock
    if not stock:
        return False
    
    value = getattr(stock, alert.type, None)
    if value is None:
        return False
    
    if alert.condition == '>':
        return value > alert.value
    elif alert.condition == '<':
        return value < alert.value
    elif alert.condition == '>=':
        return value >= alert.value
    elif alert.condition == '<=':
        return value <= alert.value
    elif alert.condition == '==':
        return value == alert.value
    return False

def check_alerts():
    """检查所有活动警报"""
    logger.info("开始检查警报...")
    alerts = Alert.query.filter_by(is_active=True, is_triggered=False).all()
    triggered_count = 0
    
    for alert in alerts:
        if check_alert_condition(alert):
            alert.is_triggered = True
            alert.last_triggered = datetime.now()
            triggered_count += 1
            # 此处可添加通知功能 (邮件、短信等)
            logger.info(f"警报触发: {alert}")
    
    if triggered_count > 0:
        db.session.commit()
        logger.info(f"已触发 {triggered_count} 个警报")
    else:
        logger.info("无警报触发")

def get_stock_history(code, market, days=30):
    """获取股票历史数据"""
    try:
        if market == 'A股':
            # 获取A股历史数据
            df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                  start_date=(datetime.now() - pd.Timedelta(days=days)).strftime('%Y%m%d'),
                                  end_date=datetime.now().strftime('%Y%m%d'), 
                                  adjust="qfq")
            if not df.empty:
                df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'amplitude', 'change_percent', 'change', 'turnover_rate']
                df['date'] = pd.to_datetime(df['date'])
                return df
        
        elif market == '港股':
            # 获取港股历史数据
            df = ak.stock_hk_hist(symbol=code, period="daily", 
                                start_date=(datetime.now() - pd.Timedelta(days=days)).strftime('%Y%m%d'),
                                end_date=datetime.now().strftime('%Y%m%d'), 
                                adjust="")
            if not df.empty:
                df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'change_percent', 'change']
                df['date'] = pd.to_datetime(df['date'])
                return df
        
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"获取历史数据出错: {code}, 错误: {str(e)}")
        return pd.DataFrame() 