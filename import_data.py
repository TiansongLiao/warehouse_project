import pandas as pd
from warehouse_project.api.models import Customers
  # 使用项目路径来引用模型


# 读取 Excel 文件
df = pd.read_excel('C:/Users/Chris/OneDrive/Desktop/database.xlsx')

# 遍历数据并保存到数据库
for index, row in df.iterrows():
    customer = Customers(
        Name=row['Name'],
        Contact_Details=row['Contact_Details'],
        Address=row['Address']
    )
    customer.save()

print("Data imported successfully.")
