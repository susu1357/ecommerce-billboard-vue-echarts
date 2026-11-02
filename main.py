# 引入 FastAPI、引入处理好的数据、写接口
from fastapi import FastAPI
from data_process import monthly_data, country_data, goods_data
from fastapi.middleware.cors import CORSMiddleware
# 创建 FastAPI 服务实例
app = FastAPI(title="电商销售数据分析看板接口")
# 跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 第一个接口
@app.get("/api/monthly")
def get_monthly_data():
    return {
        "code": 200,
        "msg": "success",
        "data": monthly_data
    }

# 第二个接口
@app.get("/api/country")
def get_country_data():
    return {
        "code": 200,
        "msg": "success",
        "data": country_data
    }

# 第三个接口
@app.get("/api/goods")
def get_goods_data():
    return {
        "code": 200,
        "msg": "success",
        "data": goods_data
    }

