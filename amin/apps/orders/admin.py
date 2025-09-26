from django.contrib import admin
from .models import Order,OrderDetails


class OrderDetailsInline(admin.TabularInline):
    model=OrderDetails
    extra=3

@admin.register(Order)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display=["customer","register_date","is_finaly","discount"]
    inlines=[OrderDetailsInline,]

