from django.urls import path
import apps.sf.views as vv
app_name="sf"

urlpatterns = [
    path("wishlist/",vv.Whish_list.as_view(),name="wishlist"),
    path("show_wish_list/",vv.show_wish_list,name="show_wish_list"),
    path("delete_favorite/",vv.delete_favorites,name="delete_favorite"),
    path("calc_favorite/",vv.calc_favorite,name="calc_favorite"),
    path("get_slider/",vv.get_slider,name="get_slider"),

    
    
]
