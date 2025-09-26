from django.shortcuts import render,redirect
from django.views import View
from apps.products.models import Product
from .forms import SearchForm
from django.db.models import Q
from django.contrib import messages


class Search(View):
    def get(self,request,*args, **kwargs):
        form=SearchForm()
        return render(request,"search/search.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=SearchForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            products=Product.objects.filter(Q(product_name__icontains=cd["search_field"])&Q(is_active=True))[:8]

            messages.success(request,"محصولات منطبق","success")
            return render(request,"search/search_result.html",{"products":products})
        else:
            messages.error(request,"فرم معتبر نمیباشد","danger")
            return redirect("search:search")
