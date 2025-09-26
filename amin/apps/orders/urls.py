from django.contrib import admin
from django.urls import path
import apps.orders.views as vv
app_name="orders"

urlpatterns = [
    path("shop_cart/",vv.Show_shop_cart.as_view(),name="shop_cart"),
    path("add_to_shopcart/",vv.add_to_shopcart,name="add_to_shopcart"),
    path("delete_from_shopcart/",vv.delete_from_shopcart,name="delete_from_shopcart"),
    path("delete_from_shopcart/",vv.delete_from_shopcart,name="delete_from_shopcart"),
    path("show_shop_cart1/",vv.show_shop_cart1,name="show_shop_cart1"),
    path("check_out1/",vv.check_out1,name="check_out1"),
    path("Check_Out/<int:order_id>",vv.Check_Out.as_view(),name="check_out"),
    path("get_copuncode/<int:order_id>",vv.get_copuncode,name="get_copuncode"),
    
    
    
]
