from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Customuser,Customer
from .forms import RegisterUserForm,LoginUserForm,Forgot,Verify,Changepass,Delete_user_form,Verify_for_delete_user_form
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import create_random_code
from django.contrib import messages
from django.db.models import Q
from apps.orders.models import OrderDetails,Order
from apps.sf.models import Favorite

class RegisterUserView(View):
    def get(self,request,*args, **kwargs):
        form=RegisterUserForm()
        return render(request,"accounts/register.html",{"form":form})
    
    
    def post(self,request,*args, **kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            active_code=create_random_code(5)
            try:
                Customuser.objects.create_user(
                    mobile_number=cd["mobile_number"],
                    password=cd["password2"],
                    active_code=active_code
                )
                request.session["user_session"]={
                    "mobile_number":cd["mobile_number"],
                    "active_code":active_code,
                
                }
                messages.success(request,"با موفقیت ثبت نام کردید لطفا وارد شوید","success")
                return redirect("main:index")
            except:
                messages.error(request,"این شماره موبایل قبلا ثبت نام کرده ایت","danger")
                return redirect("main:index")
        else:
            messages.error(request,"فرم معتبر نمیباشد","danger")
            return redirect("main:index")
        
        
        
class LoginUserView(View):
    def get(self,request,*args, **kwargs):
        form=LoginUserForm()
        return render(request,"accounts/login.html",{"form":form})
    
    
    def post(self,request,*args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            try:
                db_user=Customuser.objects.get(mobile_number=cd["mobile_number"])           
                db_user.is_active=True
                db_user.save()
            except:
                messages.error(request,"کاربر وجو ندارد","danger")
                return redirect("main:index")
            user=authenticate(username=cd["mobile_number"],password=cd["password1"])
            if user:
                

                login(request,user)
                next_url=request.GET.get("next")
                if next_url:
                    messages.success(request,"با موفقیت وارد شدید","success")
                    return redirect("main:index")
                else:
                    messages.success(request,"با موفقیت وارد شدید","success")
                    return redirect("main:index")
            else:                    
                    messages.error(request,"کاربر پیدا نشد","danger")
                    return redirect("main:index")
        else:
            messages.error(request,"فرم معتبر نمیباشد","danger")
            return redirect("main:index")
        
        
        
class LogoutUserView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        messages.error(request,"خارج شدید","danger")
        return redirect("main:index")
    
    
class Changepass1(View):
    def get(self,request,*args, **kwargs):
        form=Changepass()
        return render(request,"accounts/changepassword.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=Changepass(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user_session=request.session["user_session"]
            user=get_object_or_404(Customuser,mobile_number=user_session["mobile_number"])
            if user:
                user.set_password(cd["password1"])
                user.save()
                messages.success(request,"رمز عبور با موفقیت تغییر کرد","success")
                return redirect("accounts:login")
            else:
                messages.error(request,"کاربر وجود ندارد")
                return redirect("main:index")
        else:
            messages.error(request,"فرم معتبر نیست ","danger")
            return redirect("accounts:Changepass")

    

class VerifyUser(View):
    def get(self,request,*args, **kwargs):
        form=Verify()
        return render(request,"accounts/verify.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=Verify(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user_session=request.session["user_session"]
            user=get_object_or_404(Customuser,mobile_number=user_session["mobile_number"])
            if user:
                if user.active_code==cd["active_code"]:
                    user.active_code=create_random_code(5)
                    user.save()
                    messages.success(request,"رمز عبور جدید و تکرار ان را وارد کنید","success")
                    return redirect("accounts:Changepass")
                else:
                    messages.error(request,"کد فعالسازی را درست وارد کنید","danger")
                    return redirect("accounts:verify")
            else:
                messages.error(request," همجین کاربری وجود ندارد","danger")
                return redirect("accouts:register")     
        else:
            messages.error(request," فرم معتبر نیست ")
            return redirect("main:index")              
                
            
    
    
    
    
    
    
            
    
    
class Forgot_Pssword(View):
    def get(self,request,*args, **kwargs):
        form=Forgot()
        return render(request,"accounts/forgot.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=Forgot(request.POST)
        if form.is_valid():
            
            cd=form.cleaned_data
            user=get_object_or_404(Customuser,mobile_number=cd["mobile_number"])
            if user:
                request.session["user_session"]={
                    "mobile_number":cd["mobile_number"]
                }
                messages.success(request,"لطفا کد فعالسازی را ارسال کنید","success")
                return redirect("accounts:verify")
                
            else:
                messages.error(request,"کاربر پیدا نشد لطفا ابتدا پبت نام کنید","danger")
                return redirect("accounts:register")
        else:
            messages.error(request,"فرم معتبر نیست ","danger")
            return redirect("main:index")
    
    
    
    
class UserPanel(View):
    def get(self,request,*args, **kwargs):
        user=request.user
        favorite_count=Favorite.objects.filter(favorite_user=user).count()
        try:
            customer=Customer.objects.get(user=user)
            order_count=Order.objects.filter(customer=customer).count()
            
            user_info={
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "mobile_number":customer.phone_number,
                "order_count":order_count,
                "favorite_count":favorite_count
            }
            
        except:
            user_info={
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "favorite_count":favorite_count
            }
        
        return render(request,"accounts/userpanel.html",{"user_info":user_info})   
    
    
def last_orders(request):
    user=request.user
    customer=Customer.objects.get(Q(user=user))
    orders=Order.objects.filter(Q(customer=customer))[:8]
 
    
    return render(request,"accounts/panel_orders.html",{"orders":orders})    



def user_panel_favorite(request):                                   
    favorites=Favorite.objects.filter(Q(favorite_user=request.user))
    
    return render(request,"accounts/userpanel_fav.html",{"favorites":favorites})     


class Security(View):
    def get(self,request,*args, **kwargs):
        
        context={
           "name":request.user.name,
           "family":request.user.family
       } 
        
        return render(request,"accounts/security.html",context)


class Verify_for_delete_user(View):
    def get(self,request,*args, **kwargs):
        form=Verify_for_delete_user_form()     
        
        return render(request,"accounts/verify_for_delete_user.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=Verify_for_delete_user_form(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user_session=request.session["user_session"]
            db_user=Customuser.objects.get(mobile_number=user_session["mobile_number"])
            if db_user:
                if db_user.active_code==cd["active_code"]:
                    db_user=Customuser.objects.get(mobile_number=user_session["mobile_number"]).delete()


                    messages.success(request,"کاربربا موفقیت حذف شد","success")
                    logout(request)
                    return redirect("main:index")
            else:
                messages.error(request,"کاربری یافت نشد","danger")
                return redirect("accounts:security")
        else:
            messages.error(request,"فرم نامعتبر است","danger")
            return redirect("accounts:security")

   
    
class Delete_user(View):
    def get(self,request,*args, **kwargs):
        form=Delete_user_form()
        return render(request,"accounts/delete_user.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=Delete_user_form(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            request.session['user_session']={
                "mobile_number":cd["mobile_number"],
            }
            messages.success(request,"لطفا کد فعالسازی را وارد کنید")
            return redirect("accounts:verify_for_delete_user")
        else:
            messages.error(request,"فرم معتبر نمی باشد")
            return redirect("accounts:delete_user")
        
        
def handler404(request,exception):
    return render(request,"accounts/404.html",status=404)
        
        
        
        
        
        
        
        