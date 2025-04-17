from django.contrib import admin
from .models import Customers, Inventory, Supplier, Warehouse, Employee, Orders

admin.site.register(Customers)
admin.site.register(Inventory)
admin.site.register(Supplier)
admin.site.register(Warehouse)
admin.site.register(Employee)
admin.site.register(Orders)
