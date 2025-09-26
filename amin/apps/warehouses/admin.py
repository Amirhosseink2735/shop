from django.contrib import admin
from .models import WarehousesType,Warehouses

@admin.register(WarehousesType)
class WarehousesTyoeAdmin(admin.ModelAdmin):
    list_display=("id","warehouses_type_title")
    
    
    
@admin.register(Warehouses)
class WarehousesAdmin(admin.ModelAdmin):
    list_display=("product","price","qty","warehouses_type","registered_data")
