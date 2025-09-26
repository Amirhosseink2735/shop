from django.contrib import admin
from django.urls import path
import apps.search.views as vv
app_name="search"

urlpatterns = [
    path("search/",vv.Search.as_view(),name="search"),
    
    
]