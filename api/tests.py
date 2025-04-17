from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Supplier, Warehouse, Inventory


class RestockTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 创建 Supplier 和 Warehouse
        self.supplier = Supplier.objects.create(Name="Test Supplier", Contact_Details="test@supplier.com", Product_List="Widgets")
        self.warehouse = Warehouse.objects.create(Aisle="A1", Shelf="S1", Capacity=100)

        # 创建一个 Inventory 项，初始库存少于补货线
        self.item = Inventory.objects.create(
            Name="Test Item",
            Category="Tools",
            Quantity=5,
            Restock_Level=20,
            Location_ID=self.warehouse,
            Supplier_ID=self.supplier
        )

    def test_restock_api(self):
        # 补货前数量应为 5
        self.assertEqual(self.item.Quantity, 5)

        # 发起补货请求
        response = self.client.post(f'/api/inventory/{self.item.pk}/restock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 刷新 item，验证数量 +20
        self.item.refresh_from_db()
        self.assertEqual(self.item.Quantity, 25)

        # 再次调用补货（已高于 Restock_Level）
        response = self.client.post(f'/api/inventory/{self.item.pk}/restock/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 再次刷新，数量不应再变
        self.item.refresh_from_db()
        self.assertEqual(self.item.Quantity, 25)
