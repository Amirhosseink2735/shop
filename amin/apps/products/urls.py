from django.urls import path
import apps.products.views as vv

app_name="pro"

urlpatterns = [
    path("newproduct/",vv.NewProduct,name="newpro"),
    path("pop_group/",vv.Popular_product_group,name="pop_group"),
    path("chepeast_pro/",vv.Chepeast_products,name="chepeast_pro"),
    path("product_detail/<slug:slug>",vv.product_detail,name="product_detail"),
    path("products_of_group/<slug:slug>",vv.Products_of_group.as_view(),name="products_of_group"),
    path("get_brand/<slug:slug>",vv.get_brand_for_filter,name="get_brand"),
    path("group_for_filter/",vv.group_for_filter,name="group_for_filter"),
    path("add_favorite/",vv.add_favorites,name="add_favorite"),
    path("add_campare1/",vv.add_campare1,name="add_campare1"),
    path("get_compare/",vv.Get_compare.as_view(),name="get_compare"),
    path("campare_tebel/",vv.campare_tebel,name="campare_tebel"),
    path("delete_favorite/",vv.delete_from_favorite,name="delete_favorite"),
    path("get_products_group_for_headers/",vv.get_products_group_for_headers,name="get_products_group_for_headers"),
    path("get_product_for_header/",vv.get_product_for_header,name="get_product_for_header"),
    path("get_product_with_discount/",vv.get_product_with_discount,name="get_product_with_discount"),
    path("new_products_group/",vv.new_products_group,name="new_products_group"),
    
    
]
