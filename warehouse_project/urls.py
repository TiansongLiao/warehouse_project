from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# 设置默认路由
router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'orders', views.OrdersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # ✅ 通过 DRF 的路由来处理 API 请求
    path('api/', include('api.urls')),  # 其他自定义 API 路由
    path('api/auth/', include('api.urls_auth')),  # 自定义认证视图
    path('api-auth/', include('rest_framework.urls')),  # 支持 DRF 浏览器登录

    # ✅ 新增 Excel 上传的路由
    path('database/', views.UploadExcelView.as_view(), name='database'),  # 新增的上传路由
]