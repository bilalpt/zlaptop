from django.contrib import admin
from django.urls import include,path
from . import views

urlpatterns = [
    path('index',views.index,name='index'),
    path('home',views.home,name='home'),
    path('footer',views.footer,name='footer'),
    path('commonheader',views.commonheader,name='commonheader'),
    path('product_details/<int:product_id>/<int:pr>',views.product_details,name='product_details'),
    path('my_profile',views.my_profile,name='my_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),


    path('cart',views.cart,name='cart'),
    # path('cart',views.cart,name='cart'),
    path('mycart',views.mycart,name='mycart'),
    path('deletecartitem',views.deletecartitem,name='deletecartitem'),


    path('shipping_address',views.shipping_address,name='shipping_address'),
    path('new_address',views.new_address,name="new_address"),

    path('delete_address/<int:id>',views.delete_address,name='delete_address'),
    path('edit_addres/<int:id>',views.edit_addres,name='edit_addres'),

    #checkout
    path('checkout1',views.checkout1,name='checkout1'),
    path('razorpay',views.razorpay,name='razorpay'),


    #category products
    path('category_products',views.category_products,name='category_products'),

    #productAAHL
    path('productAAHL',views.productAAHL,name='productAAHL'),


    # success

    path('success',views.success,name='success'),

    # order history

    path('order_history',views.order_history,name='order_history'),

    # order_derails

    path('vieworderdetails/<int:id>',views.vieworderdetails,name='vieworderdetails'),


    #Add to cart
    path('Addtocart',views.addtocart,name='Addtocart'),

    #update cart

    path('updatecart',views.updatecart,name='updatecart'),


    # shipping address button

    path('placeaddress',views.placeaddress,name='placeaddress'),
    path('editbillingadd/<int:id>',views.editbillingadd,name='editbillingadd'),
    path('delete_billaddress/<int:id>',views.delete_billaddress,name='delete_billaddress'),


    #profile picture

    path('profile_picture',views.profile_picture,name='profile_picture'),

    #wishlist
    path('wishlist',views.wishlist,name='wishlist'),
    path('addwishlist',views.addwishlist,name='addwishlist'),
    path('deletewishlidtitem',views.deletewishlidtitem,name='deletewishlidtitem'),


    #wallet
    path('cancel_order/<int:cancel_id>',views.cancel_order,name='cancel_order'),

    #coupon
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
    

    # invoicedonload

    path('invoicedownload/<int:id>',views.invoicedownload,name='invoicedownload'),

    #reset pass
    path('reset_password',views.reset_password,name='reset_password'),
    
 

    



]