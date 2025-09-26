from django.shortcuts import render,get_object_or_404,redirect
from .shop_cart import shopcart
from django.views import View
from apps.products.models import Product,ProductGroup
from django.http import HttpResponse
from apps.accounts.models import Customer,Customuser
from .models import OrderDetails,Order,PaymentType
from apps.discount.models import Coupon
from .forms import OrderForm,Cupon_Code
from django.contrib import messages
from django.db.models import Q      
from django.utils import timezone 
from django.contrib.auth.mixins import LoginRequiredMixin 



class Show_shop_cart(View):
    def get(self,request,*args, **kwargs):
        shop_cart=shopcart(request)
        total_price=shop_cart.clc_total_price()
        delivery=25000
        if total_price>500000:
            delivery=0
        tax=0.09
        jame_kol=delivery+tax+total_price
        context={
            "shop_cart":shop_cart,
            "tax":tax,
            "delivery":delivery,
            "total_price":total_price,
            "jame_kol":jame_kol,
        }
        return render(request,"orders/cart.html",context)
    
def show_shop_cart1(request):
    shop_cart=shopcart(request)
    return render(request,"orders/show_shop_cart.html",{"shop_cart":shop_cart})   
    
    
def add_to_shopcart(request):
    product_id=request.GET.get("product_id")
    qty=request.GET.get("qty")
    product=get_object_or_404(Product,id=product_id)
    shop_cart=shopcart(request)
    shop_cart.add_to_shop_cart(product,qty)
    
    return HttpResponse("محصول با موفقیت اضافه شد")



def delete_from_shopcart(request):
    product_id=request.GET.get("product_id")
    product=get_object_or_404(Product,id=product_id)
    shop_cart=shopcart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart1")


def check_out1(request):
    

    shop_cart=shopcart(request)
    user=request.user
    try:
        customer=Customer.objects.get(user=user)
    except:
        customer=Customer.objects.create(user=user)
    order=Order.objects.create(
        customer=customer,
            
    )
    for item in shop_cart:
        OrderDetails.objects.create(
            order=order,
            product=item["product"],
            qty=item["qty"],
            price=item["price"]
        )

    
    return redirect("orders:check_out",order.id)



class Check_Out(View):
    def get(self,request,order_id):
        shop_cart=shopcart(request)
        order=get_object_or_404(Order,id=order_id)
        form=OrderForm()
        copun_form=Cupon_Code()
        total_price=shop_cart.clc_total_price()
        delivery=25000
        if total_price>500000:
            delivery=0
        tax=0.09
        jame_kol=delivery+tax+total_price
        if order.discount>0:
            jame_kol=delivery+tax+total_price-(delivery+tax+total_price*order.discount/100)
            
        
        context={
            "shop_cart":shop_cart,
            "form":form,
            "jame_kol":jame_kol,
            "copun_form":copun_form,
            "order":order,
        }
        return render(request,"orders/checkout.html",context)
    

   
    
def get_copuncode(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    form=Cupon_Code(request.POST)
    if form.is_valid():
        cd=form.cleaned_data
        discount=0
        try:
            copoun_code=Coupon.objects.get(coupon_code=cd["copoun_code"])
            if copoun_code.start_date<=timezone.now() and copoun_code.end_date>=timezone.now() and copoun_code.is_active==True:
                order.discount=copoun_code.discount
                order.save()
                messages.success(request,"کوپن با موفقیت اعمال شد","success")
                return redirect("orders:check_out",order.id)
            else:
                order.discount=discount
                order.save()
                messages.error(request,"کوپن معتبر نیست ","danger")
                return redirect("orders:check_out",order.id)
        except:
            messages.error(request,"کوپن پیدا نشد","danger")
            return redirect("orders:check_out",order.id)
    else:
        messages.error(request,"فرم نامعتبر است","danger")
        return redirect("orders:check_out",order.id)
        