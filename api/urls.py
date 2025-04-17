from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, EmployeeViewSet, InventoryViewSet,
    SupplierViewSet, WarehouseViewSet, OrdersViewSet
)

# ✅ 创建路由
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'orders', OrdersViewSet)

# ✅ 配置 URL 路径
urlpatterns = [
    path('', include(router.urls)),
]
