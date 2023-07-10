from django.contrib import admin
from django.urls import include,path
from .import views

urlpatterns = [

    path('addproduct',views.addproduct,name='addproduct'),
    path('ads',views.ads,name='ads'),
    path('cupon',views.cupon,name='cupon'),
    path('customers',views.customers,name='customers'),
    path('custtransaction',views.custtransaction,name='custtransaction'),
    #Dash board
    path('dashboard',views.dashboard,name='dashboard'),
    #sales report
    path('salesreport',views.salesreport,name='salesreport'),


    path('edit/<int:id>',views.edit,name='edit'),
    path('orderdetails',views.orderdetails,name='orderdetails'),
    path('product',views.products,name='product'),
    path('superuser',views.superuser,name='superuser'),
    path('common',views.common,name='common'),
    path('deleteproduct/<int:id>',views.delete,name='deleteproduct'),
    path('customer_block/<int:user_id>',views.customer_block,name='customer_block'),

    path('addbrand',views.addbrand,name='addbrand'),
    path('bdetails',views.brand_details,name='bdetails'),
    path('edit_brand/<int:edit_id>',views.edit_brand,name='edit_brand'),
    path('delete_brand/<int:del_id>',views.delete_brand,name='delete_brand'),

    # search result
    path('product_search',views.product_search,name='product_search'),
    path('search_customers',views.search_customers,name='search_customers'),
    path('brand_search',views.brand_search,name='brand_search'),

    #variations
    path('variations',views.variations,name='variations'),

    path('order_manage',views.ordermanage,name='order_manage'),

    #Admin_login
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('Alogout',views.Alogout,name='Alogout'),

    path('update_status/<int:id>',views.update_status,name='update_status'),


    #varient
    path('varieant',views.varieant,name='varieant'),
    path('deletevarient<int:id>',views.deletevarient,name='deletevarient'),
    path('editvarieant<int:id>',views.editvarieant,name='editvarieant')









]