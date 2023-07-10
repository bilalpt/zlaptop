from django.contrib import admin
from .models import Product
from .models import brand
from .models import *




# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category','modified_date', 'is_available')
    prepopulated_feilds = {'slug':('product_name',)}



admin.site.register(Product,ProductAdmin)
admin.site.register(brand)
admin.site.register(Cart)
admin.site.register(profile_address)
admin.site.register(Processor)
admin.site.register(Variations)
admin.site.register(Ordered_Product)
admin.site.register(Order)
admin.site.register(billing_address)
admin.site.register(Coupon)




