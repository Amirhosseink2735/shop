from django.db import models
from apps.products.models import Product
from apps.accounts.models import Customuser

class WarehousesType(models.Model):
    warehouses_type_title=models.CharField(max_length=50,verbose_name="نوع انبار")
    
    def __str__(self):
        return self.warehouses_type_title

    class Meta:
        verbose_name="نوع انبار"
        verbose_name_plural="انواع روش انبار"
        

class Warehouses(models.Model):
    warehouses_type=models.ForeignKey(WarehousesType,on_delete=models.CASCADE,related_name="warehouses",verbose_name="انبار")
    user_registred=models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name="warehouseuser_registered",verbose_name="کسی که پبت کردع")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="earehouse_products",verbose_name="کالا")
    qty=models.IntegerField(verbose_name="تعداد")
    price=models.IntegerField(verbose_name="قیمت واحد",null=True,blank=True)
    registered_data=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت")
    
    def __str__(self):
        return  f"{self.warehouses_type} - {self.product}"
    
    class Meta:
        verbose_name='انبار'
        verbose_name_plural="انبارها"