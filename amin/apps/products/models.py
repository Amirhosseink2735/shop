from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum,Q

class Brand(models.Model):
    brand_title=models.CharField(max_length=100,verbose_name="نام برند")
    file_upload=FileUpload("images","brand")
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name="تصویر کالا")
    slug=models.SlugField(max_length=200,null=True)
    
    def __str__(self):
        return self.brand_title
    
    
    class Meta:
        verbose_name="برند"
        verbose_name_plural='برندها'
        
        
        
class ProductGroup(models.Model):
    group_title=models.CharField(max_length=100,verbose_name="عنوان گروه کالا")
    file_upload=FileUpload("images","product_group")
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name="تصویر گروه کالا")
    description=models.TextField(blank=True,null=True,verbose_name="توضیحات گروه کالا")
    is_active=models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال/غیر فعال")
    group_parent=models.ForeignKey('productGroup',on_delete=models.CASCADE,verbose_name="والد گروه کالا",blank=True,null=True,related_name="groups")
    slug=models.SlugField(max_length=200,null=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    published_date=models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update_date=models.DateTimeField(auto_now=True,verbose_name="اخرین بروزرسانی")
    
    def __str__(self):
        return self.group_title
    
    class Meta:
        verbose_name="گروه کالا"
        verbose_name_plural="گروهای کالاها"
        
class Feature(models.Model):
    feature_name=models.CharField(max_length=100,verbose_name="نام ویزگی")
    product_group=models.ManyToManyField(ProductGroup,verbose_name="گروه کالا",related_name='features_of_groups')
    def __str__(self):
        return self.feature_name
    class Meta:
        verbose_name="ویزگی"
        verbose_name_plural="ویزگی ها"
from django.utils import timezone  
from middlewares.middlewares import RequestMiddleware        
class Product(models.Model):
    product_name=models.CharField(max_length=500,verbose_name="نام کالا")
    description=models.TextField(blank=True,null=True,verbose_name="توضیحات کالا")
    s_description=models.TextField(null=True,blank=True,verbose_name="خلاصه توضیحات محصول")
    file_upload=FileUpload("images","product")
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name="تصویر کالا")
    price=models.PositiveIntegerField(default=0,verbose_name= "قیمت کالا")
    product_group=models.ManyToManyField(ProductGroup,verbose_name="گروه کالا",related_name="products_of_group")       
    brand=models.ForeignKey(Brand,verbose_name="برند کالا",on_delete=models.CASCADE,null=True,related_name="product_of_brands")
    is_active=models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال/غیر فعال")
    slug=models.SlugField(max_length=200,null=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    published_date=models.DateTimeField(auto_now=True,verbose_name="تارخ اخرین بروزرسانی")
    features=models.ManyToManyField(Feature,through="productFeature")
    update_date=models.DateTimeField(auto_now=True,verbose_name="تاریخ اخرین بروز رسانی ")
    
    def get_absolute_url(self):
        return reverse("pro:product_detail", kwargs={"slug": self.slug})
    
    
    def get_price_by_discount(self):
        l1=[]
        for dbd in self.discount_basket_details2.all():
            if(dbd.discount_basket.is_active==True and
                      dbd.discount_basket.start_date<=timezone.now() and
                      dbd.discount_basket.end_date>=timezone.now()):
                l1.append(dbd.discount_basket.discount)
            
        discount=0
        if len(l1)>0:
            discount=max(l1)

        return self.price-(self.price*discount/100)
    
    
    def get_number_product(self):
        sum1=self.earehouse_products.filter(warehouses_type_id=1).aggregate(Sum("qty"))
        sum2=self.earehouse_products.filter(warehouses_type_id=2).aggregate(Sum("qty"))
        
        input=0
        if sum1["qty__sum"]!=None:
            input=sum1["qty__sum"]
        output=0
        if sum2["qty__sum"]!=None:  
            output=sum2["qty__sum"]            
        return input-output
    
    
    
    def get_wishlist(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        
        flag=self.favorite_product.filter(favorite_user_id=request.user.id).exists()

        return flag
    
    
    def get_discount(self):
        discount=0
        l1=[]
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active==True and dbd.discount_basket.start_date<=timezone.now()
                and dbd.discount_basket.end_date>=timezone.now()):
                l1.append(dbd.discount_basket.discount)
                
        if len(l1)>0:
            discount=max(l1)
            print(discount)
            
        return discount

    
    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name="کالا"
        verbose_name_plural="کالاها"
        

        
        
class FeatureValue(models.Model):
    value_title=models.CharField(max_length=100,verbose_name="مقدار ویزگی")
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name="ویزگی",related_name="feature_values")
    
    def __str__(self):
        return f"{self.id}  {self.value_title}"
    
    class Meta:
        verbose_name="مقدار ویزگی"
        verbose_name_plural="مقدار ویزگی ها"

class ProductFeature(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="کالا",related_name="product_feature")
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name="ویزگی")
    value=models.CharField(max_length=100,verbose_name="مقدارویزگی کالا")
    filter_value=models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name="مقدار فیلتر")
    
    def __str__(self):
        return f"{self.product} - {self.feature} : {self.value}"
    
    
    class Meta:
        verbose_name="ویزگی محصول"
        verbose_name_plural="ویزگی های محصولات"
        
        
        
class ProductGallery(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="کالا",related_name="gallery_images")
    file_upload=FileUpload("images","product_gallery")
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name="تصویر کالا")
    
    
    class Meta:
        verbose_name="تصویر"
        verbose_name_plural="تصاویر"    

