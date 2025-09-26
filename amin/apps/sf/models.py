from django.db import models
from apps.products.models import Product
from apps.accounts.models import Customuser
from django.core.validators import MinValueValidator,MaxValueValidator
class Scoring(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="scoring_product",verbose_name="کالا")
    scoring_user=models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name="scorinf_user1",verbose_name="امتیاز دهنده")
    registerdate=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    score=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name="امتیاز")
    
    
    def __str__(self):
        return f"{self.product} - {self.scoring_user}"
    
    
    class Meta:
        verbose_name="امتیاز"
        verbose_name_plural="امتیازات"
        



class Favorite(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="favorite_product",verbose_name="کالا")
    favorite_user=models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name="favorite_user1",verbose_name="کاربر علاقه مند")
    register_date=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    
    def __str__(self):
        return f"{self.product} - {self.favorite_user}"

    class Meta:
        verbose_name="علاقه"
        verbose_name_plural="علاقه مندی ها"
        
        

from django.utils.html import mark_safe
from utils import FileUpload
from django.utils import timezone



class Slider(models.Model):
    slider_title1=models.CharField(max_length=500,null=True,blank=True,verbose_name="متن اول")
    slider_title2=models.CharField(max_length=500,null=True,blank=True,verbose_name="متن دوم")
    slider_title3=models.CharField(max_length=500,null=True,blank=True,verbose_name="متن سوم")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name='product_slider',verbose_name="اسلایدر محصول")
    file_upload=FileUpload("images","slides")
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name="تصویراسلاید")
    slider_link=models.URLField(max_length=200,null=True,blank=True,verbose_name="لینک")
    is_active=models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال/غیرفعال")
    register_date=models.DateTimeField(auto_now_add=True,verbose_name="تاریخ انتشار")
    published_date=models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update_date=models.DateTimeField(auto_now=True,verbose_name="تاریخ اخرین بروزرسانی")
    
    
    def __str__(self):
        return f"{self.slider_title1}"
    
    class Meta:
        verbose_name="اسلاید"
        verbose_name_plural="اسلایدها"
        
        
        
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style="width:80px;height:80px"/>')
    
    def link(self):
        return mark_safe(f'<a href="{self.slider_link}" target="_blank">link</a>')
    

