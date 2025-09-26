from django.db import models
from apps.accounts.models import Customer
from django.utils import timezone
import uuid
from apps.products.models import Product


class PaymentType(models.Model):
    payment_title=models.CharField(max_length=50,verbose_name="نوع پرداخت")
    
    
    def __str__(self):
        return self.payment_title
    
    
    class Meta:
        verbose_name="نوع پرداخت"
        verbose_name_plural="انواع روش پرداخت"
        


class Order(models.Model):
    customer=models.ForeignKey(Customer, verbose_name="مشتری",related_name="orders",on_delete=models.CASCADE)
    register_date=models.DateField(default=timezone.now,verbose_name="تاریخ درج سفارش")
    update_date=models.DateField(auto_now=True,verbose_name="تاریخ ویرایش سفارش")
    is_finaly=models.BooleanField(default=False,verbose_name="نهایی شده")
    order_code=models.UUIDField(unique=True,default=uuid.uuid4,editable=False,verbose_name="کد تولیدی برای سفارش")
    discount=models.IntegerField(blank=True,null=True,default=0,verbose_name="تخفیف روی فاکتور")
    description=models.TextField(blank=True,null=True,verbose_name="توضیحات")
    payment_type=models.ForeignKey(PaymentType,on_delete=models.CASCADE,default=None,null=True,blank=True,related_name="payment_types",verbose_name="نوع پرداخت")
    
    
    def __str__(self):
        return f"{self.customer}\t{self.id}\t{self.is_finaly}"
    
    
    
    def get_order_total_price(self):
        t=0
        for item in self.orders_details1.all():
            t=t+item.product.price*item.qty     
        return t       
    
    def get_name_of_products(self):
        p=[]
        for item in self.orders_details1.all():
            p.append(item.product.product_name)
        return ",".join(p)    
    
    
    class Meta:
        verbose_name="سفارش"
        verbose_name_plural="سفارشات"
        
        

class OrderDetails(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="orders_details1",verbose_name="سفارش")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="orders_details2",verbose_name="کالا")
    qty=models.PositiveIntegerField(default=1,verbose_name="تعداد")
    price=models.IntegerField(verbose_name="قیمت کالا در فاکتور")
    
    def __str__(self):
        return f"{self.order}\t{self.product}\t{self.qty}\t{self.price}"
