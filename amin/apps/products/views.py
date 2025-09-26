from django.shortcuts import render,redirect
from django.db.models import Q
from django.views import View
from .models import Product,ProductGroup,Brand
from django.shortcuts import render,get_object_or_404
from django.db.models import Q,Count
from django.http import HttpResponse


def NewProduct(request):
    products=Product.objects.filter(Q(is_active=True)).order_by("-register_date")[:4]
    return render(request,"products/newproduct.html",{"products":products})


def Popular_product_group(request):
    Product_groups=ProductGroup.objects.filter(Q(is_active=True)& ~Q(group_parent=None)).annotate(count=Count("products_of_group")).order_by("-count")
    return render(request,"products/popular_group.html",{"product_groups":Product_groups})

def Chepeast_products(request):
    products=Product.objects.filter(Q(is_active=True)).order_by("price")[:8]
    return render(request,"products/chepeast.html",{"products":products})



def product_detail(request,slug):
    product=get_object_or_404(Product,slug=slug)
    product_gallery=product.gallery_images.all()
    feature=product.product_feature.all()
    

    context={
        "product":product,
        "p_gallery":product_gallery,
        "feature":feature
        
    }
    
    return render(request,"products/product_detail.html",context)

def get_product_group(request):
    product_group=ProductGroup.objects.filter(Q(is_active=True))[:6]
    return render(request,"products/groupforhead.html",{"product_group":product_group})



class Products_of_group(View):
    def get(self,request,slug):
        product_group=get_object_or_404(ProductGroup,slug=slug)
        products=Product.objects.filter(Q(is_active=True)&Q(product_group=product_group))
        
        brand_list=request.GET.getlist("brand")
        if brand_list:
            products=products.filter(Q(brand__id__in=brand_list))

        context={
            "products":products,
            "slug":slug,
        }
        return render(request,"products/product_for_group.html",context)
    





def get_brand_for_filter(request,slug):
    products_group=get_object_or_404(ProductGroup,slug=slug)
    brand_list_id=products_group.products_of_group.filter(is_active=True)\
        .values("brand_id")
    brands=Brand.objects.filter(pk__in=brand_list_id).annotate(count=Count("product_of_brands")).order_by("-count")   
    context={
        "brands":brands,
        
    }
    return render(request,"products/get_brand.html",context)
    
    
def group_for_filter(request):
    product_group=ProductGroup.objects.filter(Q(is_active=True))\
        .annotate(count=Count("products_of_group")).order_by("-count")
    return render(request,"products/group_filter.html",{"products_group":product_group})


from apps.sf.models import Favorite
def add_favorites(request):
    user=request.user
    product_id=request.GET.get("product_id")
    flag=Favorite.objects.filter(Q(product_id=product_id)&Q(favorite_user_id=user.id)).exists()
    if (not flag):
        Favorite.objects.create(
            favorite_user_id=user.id,
            product_id=product_id
        )
        
    return HttpResponse("محصول با موفقیت به علاقه مندی ها اضافه شد")

from .campare import CampareProduct

def add_campare1(request):
    product_id=request.GET.get("product_id")
    campare=CampareProduct(request)
    campare.add_to_campare_product(product_id)
    return HttpResponse("محصول با موفقیت به لیست مقایسه اضاقه شد ")
    

class Get_compare(View):
    def get(self,request,*args, **kwargs):
        compare=CampareProduct(request)
        return render(request,"products/compare.html",{"compare":compare})
    
    
def campare_tebel(request):
    compare=CampareProduct(request)
    products=[]
    for product_id in compare:
        product=Product.objects.get(Q(id=product_id)) 
        products.append(product)
    features=[]
    for product in products:
        for item in product.product_feature.all():
            if item.feature not in features:
                features.append(item.feature)
    context={
        "products":products,
        "features":features
    }
                
    return render(request,"products/campare_tabel.html",context)


def delete_from_favorite(request):
    product_id=request.GET.get("product_id")
    campare=CampareProduct(request)
    campare.delete_from_campare_product(product_id)
    return redirect("pro:campare_tebel")


def get_products_group_for_headers(request):
    products_group=ProductGroup.objects.filter(Q(is_active=True)&~Q(group_parent=None)).annotate(count=Count("products_of_group")).order_by("-count")[:6]
    return render(request,"products/get_productgroup_headers.html",{"products_group":products_group})
        
    
    
def get_product_for_header(request):
    products=Product.objects.filter(Q(is_active=True)).order_by("-register_date")    
    return render(request,"products/products_for_headers.html",{"products":products})
        
from apps.discount.models import DiscountBasketDetails  

def get_product_with_discount(request):
    products=Product.objects.filter(Q(is_active=True)&~Q(discount_basket_details2=None))[:3]
    
    
    return render(request,"products/product_discount.html",{"products":products})

def new_products_group(request):
    product_groups=ProductGroup.objects.filter(Q(is_active=True)).order_by("-register_date")
    return render(request,"products/new_products_group.html",{"product_groups":product_groups})
