import akshare as ak

# 获取A股历史数据
stock_zh_a_hist = ak.stock_zh_a_hist(symbol="300454", period="daily", adjust="qfq")
print(stock_zh_a_hist)

# 获取A股实时行情数据
stock_zh_a_spot = ak.stock_zh_a_spot()
print(stock_zh_a_spot)

# 获取港股实时数据
stock_hk_spot = ak.stock_hk_spot()
print(stock_hk_spot)



pip install -r requirements.txt --index-url https://pypi.org/simple

pip install akshare --upgrade --index-url https://mirrors.aliyun.com/pypi/simple