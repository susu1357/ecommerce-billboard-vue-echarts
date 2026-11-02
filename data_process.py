import pandas as pd

# 读取数据集，编码适配OnlineRetail
df = pd.read_csv("OnlineRetail.csv", encoding="unicode_escape")
# 开始清洗数据
# 删掉负值
df = df[ (df["Quantity"] > 0) & (df["UnitPrice"] > 0) ]
# 转换日期格式
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
print(df["InvoiceDate"].dtype)
# 增加单笔金额
df["Sales"]=df["Quantity"]*df["UnitPrice"]

# 确认清洗完成
print("清洗后总行数：", len(df))
print("数量最小值：", df["Quantity"].min())
print("单价最小值：", df["UnitPrice"].min())
print("销售额列存在：", "Sales" in df.columns)

# 看板的几个重要指标
total_sales = df["Sales"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].dropna().nunique()
total_products = df["StockCode"].nunique()

print("总销售额：", round(total_sales, 2))
print("订单总数：", total_orders)
print("客户数量：", total_customers)
print("商品种类数：", total_products)

df["year_month"] = df["InvoiceDate"].dt.to_period("M")
monthly_sales = df.groupby("year_month")["Sales"].sum()
monthly_order_cnt = df.groupby("year_month")["InvoiceNo"].nunique()
monthly_customer_cnt = df.groupby("year_month")["CustomerID"].nunique()
monthly_df = pd.concat(
    [
        monthly_sales.rename("sales_amount"),
        monthly_order_cnt.rename("order_count"),
        monthly_customer_cnt.rename("customer_count")
    ],
    axis=1
).reset_index()
# 把year_month从Period转为字符串，方便接口返回
monthly_df["year_month"] = monthly_df["year_month"].astype(str)
print(monthly_df)

country_sales = df.groupby("Country")["Sales"].sum()
country_df = country_sales.rename("sales_amount").reset_index().sort_values("sales_amount",ascending=False)

# 销量最高的 TOP 商品
goods_sales = df.groupby("StockCode")["Quantity"].sum()
goods_df = goods_sales.rename("quantity_total").reset_index().sort_values("quantity_total",ascending=False)

# 最后转换成列表字典，给外部导入 
monthly_data = monthly_df.to_dict(orient="records")
country_data = country_df.to_dict(orient="records")
goods_data = goods_df.to_dict(orient="records")

