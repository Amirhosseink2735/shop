from django.shortcuts import render,redirect
from django.views import View
from .models import Favorite
from django.db.models import Q
from django.http import HttpResponse

class Whish_list(View):
    def get(self,request,*args, **kwargs):
        return render(request,"sf/whishlist.html")
    
    
    
    
def show_wish_list(request):
    user=request.user
    favorites=Favorite.objects.filter(Q(favorite_user_id=user.id))

    context={
        "favorites":favorites,
    }
    return render(request,"sf/show_wish_list.html",context)




def delete_favorites(request):
    product_id=request.GET.get("product_id")
    user=request.user
    Favorite.objects.filter(Q(favorite_user_id=user.id)&Q(product_id=product_id)).delete()
    
    return redirect("sf:show_wish_list")

def calc_favorite(request):
    user=request.user
    count=Favorite.objects.filter(Q(favorite_user_id=user.id)).count()
    print(count)
    return HttpResponse(count)

from .models import Slider

def get_slider(request):
    sliders=Slider.objects.filter(Q(is_active=True))
    return render(request,"sf/sliders.html",{"sliders":sliders})