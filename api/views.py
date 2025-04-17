from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import pandas as pd

from .models import Customers, Employee, Inventory, Supplier, Warehouse, Orders
from .serializers import (
    CustomerSerializer,
    EmployeeSerializer,
    InventorySerializer,
    SupplierSerializer,
    WarehouseSerializer,
    OrderSerializer
)

# 客户视图
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

# 员工视图
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# 库存视图
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=True, methods=['post'])
    def restock(self, request, pk=None):
        item = self.get_object()
        if item.Quantity < item.Restock_Level:
            item.Quantity += 20
            item.save()
            return Response({
                "status": "restocked",
                "new_quantity": item.Quantity
            })
        else:
            return Response({
                "status": "no need to restock",
                "current_quantity": item.Quantity
            })

# 供应商视图
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

# 仓库视图
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

# 订单视图
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

# 上传 Excel 文件视图
# ✅ 修复外键对象赋值问题
class UploadExcelView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file is None:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            xls = pd.ExcelFile(file)

            df_warehouse = pd.read_excel(xls, 'Warehouse')
            for _, row in df_warehouse.iterrows():
                Warehouse.objects.update_or_create(
                    Location_ID=row['Location_ID'],
                    defaults={
                        'Aisle': row['Aisle'],
                        'Shelf': row['Shelf'],
                        'Capacity': row['Capacity']
                    }
                )

            df_supplier = pd.read_excel(xls, 'Supplier')
            for _, row in df_supplier.iterrows():
                Supplier.objects.update_or_create(
                    Supplier_ID=row['Supplier_ID'],
                    defaults={
                        'Name': row['Name'],
                        'Contact_Details': row['Contact_Details'],
                        'Product_List': row['Product_List']
                    }
                )

            df_customers = pd.read_excel(xls, 'Customers')
            for _, row in df_customers.iterrows():
                Customers.objects.update_or_create(
                    Customer_ID=row['Customer_ID'],
                    defaults={
                        'Name': row['Name'],
                        'Contact_Details': row['Contact_Details'],
                        'Address': row['Address']
                    }
                )

            df_inventory = pd.read_excel(xls, 'Inventory')
            for _, row in df_inventory.iterrows():
                Inventory.objects.update_or_create(
                    Item_ID=row['Item_ID'],
                    defaults={
                        'Name': row['Name'],
                        'Category': row['Category'],
                        'Quantity': row['Quantity'],
                        'Location_ID': Warehouse.objects.get(Location_ID=row['Location_ID']),
                        'Supplier_ID': Supplier.objects.get(Supplier_ID=row['Supplier_ID'])
                    }
                )

            df_employee = pd.read_excel(xls, 'Employee')
            for _, row in df_employee.iterrows():
                Employee.objects.update_or_create(
                    Employee_ID=row['Employee_ID'],
                    defaults={
                        'Name': row['Name'],
                        'Role': row['Role'],
                        'Assigned_Area': row['Assigned_Area']
                    }
                )

            df_order = pd.read_excel(xls, 'Order')
            for _, row in df_order.iterrows():
                Orders.objects.update_or_create(
                    Order_ID=row['Order_ID'],
                    defaults={
                        'Customer_ID': Customers.objects.get(Customer_ID=row['Customer_ID']),
                        'Item_ID': Inventory.objects.get(Item_ID=row['Item_ID']),
                        'Quantity': row['Quantity'],
                        'Status': row['Status'],
                        'Order_Date': row['Order_Date']
                    }
                )

            return Response({'message': '✅ All data imported or updated successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'❌ 处理文件出错: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
