from django.contrib import admin
from .models import Brand,ProductGroup,Product,Feature,ProductFeature,FeatureValue,ProductGallery
from django.db.models.aggregates import Count
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.http import HttpResponse
from django.core import serializers
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=("brand_title",)
    list_filter=("brand_title",)
    search_fields=("brand_title",)
    ordering=("brand_title",)

class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model=ProductGroup

def de_active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f"تعداد {res}غیرفعال شد "
    modeladmin.message_user(request,message)
    
def active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f"تعداد {res}فعال شد "
    modeladmin.message_user(request,message)
    
def export_to_json(modeladmin,request,queryset):
    response=HttpResponse(content_type="application/json")
    serializers.serialize("json",queryset,stream=response)
    return response

class GroupFilter(SimpleListFilter):
    title="گروه محصولات"
    parameter_name="Group"
    def lookups(self, request, model_admin):
        sub_group=ProductGroup.objects.filter(~Q(group_parent=None))
        group=[item.group_parent for item in sub_group]
        return [(item.id,item.group_title)for item in group]
        

    def queryset(self, request, queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
    
    
    
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=("group_title","is_active","group_parent","slug","register_date","update_date",)
    list_filter=(GroupFilter,)
    search_fields=("group_title",)
    ordering=("group_parent","group_title",)
    inlines=[ProductGroupInstanceInlineAdmin,]
    actions=[de_active_product_group,active_product_group,export_to_json]
    list_editable=["is_active",]

    
    
    
    
    def get_queryset(self,*args, **kwargs):
        qs=super(ProductGroupAdmin,self).get_queryset(*args, **kwargs)
        qs.annotate(sub_group=Count("groups"))
        return qs
    
    def count_sup_group(self,obj):
        return obj.sub_group
    
    
    count_sup_group.short_description="تعداد زیر گروها"  
    
def active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f"تعداد{res}کالا فعال شد" 
    modeladmin.message_user(request,message)
    
def de_active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f"تعدا{res}کالا غیر فعال شد" 
    modeladmin.message_user(request,message)

class productinlineAdmin(admin.TabularInline):
    model=ProductFeature 
    
class ProductgalleryInline(admin.TabularInline):
    model=ProductGallery   
    
@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    list_display=("product_name","price","brand","is_active","update_date","slug","display_product_group")
    list_filter=("brand","product_group")
    search_fields=("product_name",)
    ordering=("update_date","product_name",)
    actions=[active_product,de_active_product,]
    
    inlines=[productinlineAdmin,ProductgalleryInline,]
    
    def display_product_group(self,obj):
        return ",".join([group.group_title for group in obj.product_group.all()])
    
    
    
    
class FeatureValueInline(admin.TabularInline):
    model=FeatureValue  
    extra=3 
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=("feature_name","display_group","display_feature_values")
    list_filter=("feature_name",)
    search_fields=("feature_name",)
    ordering=("feature_name",) 
    inlines=[FeatureValueInline,]
    
    def display_group(self,obj):
        return ",".join([group.group_title for group in obj.product_group.all()]) 
    
    
    def display_feature_values(self,obj):
        return " , ".join([feature_value.value_title for feature_value in obj.feature_values.all()])
    
    display_feature_values.short_description = "مقادیر ویژگی‌ها"
    display_group.short_description = "گروه‌ها"


    
    
