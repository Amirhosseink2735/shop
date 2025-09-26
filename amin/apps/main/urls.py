from django.contrib import admin
from django.urls import path
import apps.main.views as vv
app_name="main"

urlpatterns = [
    path("",vv.index,name="index"),
    
    
]
