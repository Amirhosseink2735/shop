from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager
from django.utils import timezone
from utils import FileUpload



class customusermanager(BaseUserManager):
    def create_user(self,mobile_number,name="",family='',email=None,gender=None,active_code=None,password=None):
        user=self.model(
            mobile_number=mobile_number,
            email=BaseUserManager.normalize_email(email),
            name=name,
            family=family,
            gender=gender,
            active_code=active_code,
        )
        user.set_password(password)
        user.save()
        return user
 

    def create_superuser(self,mobile_number,email,name,family,password):
        user=self.create_user(
            mobile_number=mobile_number,
            name=name,
            family=family,
            email=email, 
            password=password,
        )
        user.is_admin=True
        user.is_active=True
        user.is_superuser=True
        user.save()
        return user





    
    
class Customuser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=12,unique=True,verbose_name="شماره موبایل")
    email=models.EmailField(max_length=200,blank=True)
    name=models.CharField(max_length=50,blank=True)
    family=models.CharField(max_length=50,blank=True)
    GENDER_CHOICES=(("True","مرد"),("False","زن"))
    gender=models.CharField(max_length=50,blank=True,choices=GENDER_CHOICES,default="True",null=True)
    register_date=models.DateField(default=timezone.now)
    is_active=models.BooleanField(default=False)
    active_code=models.CharField(max_length=100,null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    
    USERNAME_FIELD="mobile_number"
    REQUIRED_FIELDS=["email","name","family"]
    def __str__(self):
        return self.name+" "+self.family
    @property
    def is_staff(self):
        return self.is_admin
    
    
    objects=customusermanager()
    
    
    
    

        
class Customer(models.Model):
    user=models.OneToOneField(Customuser,on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(max_length=11,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    file_upload=FileUpload("images","customer")
    image_name=models.ImageField(upload_to=file_upload.upload_to,null=True,blank=True,verbose_name="تصویر پروفایل")
    
    
    def __str__(self):
        return f"{self.user}"