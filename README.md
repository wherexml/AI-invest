# 股市投资提醒系统

一个基于 AKshare 的 Web 投资提醒软件，针对港股和 A 股市场。

## 功能特点

- 支持 A 股和港股市场
- 实时股票数据更新
- 自定义价格、涨跌幅等提醒设置
- 股票历史数据图表显示
- 自动监控股票价格变化

## 技术栈

- 后端：Flask
- 数据库：SQLite
- 前端：Bootstrap 5 + jQuery
- 数据源：AKshare
- 任务调度：APScheduler

## 安装要求

- Python 3.8+
- AKshare 1.11.0+
- Flask 2.3.0+
- Flask-SQLAlchemy 3.1.0+
- APScheduler 3.10.0+
- Pandas 2.0.0+
- Plotly 5.18.0+

## 安装步骤

1. 克隆项目仓库

```bash
git clone https://github.com/yourusername/stock-alert-system.git
cd stock-alert-system
```

2. 安装依赖包

```bash
pip install -r requirements.txt
```

3. 运行应用

```bash
python app.py
```

4. 在浏览器中访问 `http://localhost:5000`

## 使用指南

### 添加股票

1. 点击"股票列表"菜单
2. 在搜索栏输入股票代码或名称
3. 选择市场类型（A股或港股）
4. 点击"搜索"按钮
5. 在搜索结果中点击"添加"按钮

### 设置提醒

1. 进入股票详情页
2. 在"设置提醒"卡片中选择提醒类型、条件和数值
3. 点击"添加提醒"按钮
4. 提醒将在满足条件时自动触发

### 管理提醒

1. 点击"提醒列表"菜单查看所有提醒
2. 可以启用/禁用、重置或删除提醒

## 定时任务

系统包含两个定时任务：

- 每5分钟更新一次所有股票数据
- 每分钟检查一次所有活动提醒

## 数据源说明

本系统使用 AKshare 作为数据源，获取 A 股和港股的实时行情和历史数据。详情请参考 [AKshare 文档](https://akshare.akfamily.xyz)。

## 许可证

MIT 