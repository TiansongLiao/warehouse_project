from django.db import models

# 供应商模型
class Supplier(models.Model):
    Supplier_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, db_index=True)  # 添加索引来加速查询
    Contact_Details = models.CharField(max_length=200)
    Product_List = models.TextField()

    def __str__(self):
        return self.Name

# 仓库模型
class Warehouse(models.Model):
    Location_ID = models.AutoField(primary_key=True)
    Aisle = models.CharField(max_length=20, db_index=True)  # 为仓库的Aisle字段添加索引
    Shelf = models.CharField(max_length=20)
    Capacity = models.IntegerField()

    def __str__(self):
        return f"Warehouse {self.Location_ID}"

# 员工模型
class Employee(models.Model):
    Employee_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Role = models.CharField(max_length=50)
    Assigned_Area = models.CharField(max_length=50, blank=True, null=True)
    Location_ID = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.Name

# 客户模型
class Customers(models.Model):
    Customer_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Contact_Details = models.CharField(max_length=200)
    Address = models.TextField()

    def __str__(self):
        return self.Name

# 库存模型
class Inventory(models.Model):
    Item_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, db_index=True)  # 添加索引来加速查询
    Category = models.CharField(max_length=50)
    Quantity = models.IntegerField()
    Location_ID = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    Supplier_ID = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Restock_Level = models.IntegerField(default=10)  # 自动补货水平

    class Meta:
        indexes = [
            models.Index(fields=['Name', 'Category']),  # 为 Name 和 Category 添加联合索引
        ]

    def __str__(self):
        return self.Name

# 订单模型
class Orders(models.Model):
    Order_ID = models.AutoField(primary_key=True)
    Customer_ID = models.ForeignKey(Customers, on_delete=models.CASCADE)
    Item_ID = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
        ],
    )
    Order_Date = models.DateField()
    Employee_ID = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.Order_ID}"