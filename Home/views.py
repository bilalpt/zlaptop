from django.shortcuts import render,redirect
from Adminpanel.models import Product,brand,Cart,profile_address, Order, Ordered_Product,Processor,billing_address,Wishlist,Coupon,CouponUsed
from Adminpanel.models import Variations
from categories.models import category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError


# Pdf
from io import BytesIO
from django.template.loader import get_template
from django.conf import settings
import os
import uuid






# Create your views here.

def index(request):
    return render(request,'index.html')

#home

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log')
def home(request):
    products= Product.objects.all().order_by('id')

    variated_products=Variations.objects.all()[:4]
    cat = category.objects.all().order_by('id')[:4]
    bran=brand.objects.all().order_by('id')[:4]
    context = {
        'one':variated_products,
        'key':cat,
        'brand':bran,
        'product':products,

    }
    return render(request,'Home/home.html',context)

#productAAHL
def productAAHL(request):
    cat=category.objects.all().order_by('id')
    category_id = request.GET.get('category')

    if category_id:
        pro = Product.objects.filter(category=category_id)
        if not pro:
            single_product=Variations.objects.all().order_by('id')
            cat=category.objects.all().order_by('id')

            context={
                'one':single_product,
                'cat':cat,
            }
            messages.error(request,'No item available in this Brand')
            return render(request, 'Home/productAAHL.html',context)
        for product in pro:
            product_id = product.id
            single_product=Variations.objects.filter(vproduct = product_id).order_by('id')
    else:
        single_product=Variations.objects.all().order_by('id')
    
    
    context={
        'one':single_product,
        'cat':cat,
    }
    return render(request,'Home/productAAHL.html',context)

def search_product(request):

    if 'keyword' in request.GET:
        prod=request.GET['keyword']
        if prod.strip()=='':
            messages.error(request,'No result found please try again ')

        if prod:
            products=Variations.objects.filter(vproduct__product_name__icontains=prod)
            cat=category.objects.all().order_by('id')


        context={
            'one':products,
            'cat':cat
        }

    return render(request,'Home/productAAHL.html',context)
 



def footer(request):
    return render(request,'footer.html')

def commonheader(request):
    return render(request,'commonheader.html')




def product_details(request,product_id, pr=None):
   
    if pr !=0 :
        variant=Variations.objects.get(id=pr)
        page = 2
    else:
        variant=Variations.objects.filter(vproduct__id=product_id)
        page=1 
           
    product = Product.objects.get(id=product_id)
    try:
        processor=Processor.objects.all()






        # products=Product.objects.get(id=product_id)

        try:
            p = Cart.objects.get(user=request.user, product_id = product_id)
        except:
            p = None
        if p:
            qnty = p.product_qty
        else:
            qnty = 0

    except Exception as e:
        raise







    context={
        'product_details': variant,
        'quantity': qnty,
        'processor':processor,
        'product': product,
        'page': page,
        

    }
    return render(request,'Home/product_details.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log')

def my_profile(request):
    user=User.objects.get(username= request.user)
    # if request.user.is_authenticated:
    profile=profile_address.objects.all()
    one={
        'user':user,
        'profile':profile,
        
    }
    return render(request,'Home/myprofile.html',one)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log')


def edit_profile(request):
    user=User.objects.get(username= request.user)
    one1={
        'user':user
    }

    if request.method=='POST':
        fname=request.POST.get('name')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')

        user.username=fname
        user.last_name=lname
        user.email=email

        user.save()
        return redirect('my_profile')


    return render(request,'Home/edit_profile.html',one1)

def shipping_address(request):

    a = profile_address.objects.filter(user=request.user)

    one={
        'a':a,
    }

    return render(request,'Home/shipping_address.html',one)

def new_address(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            name=request.POST.get('name')
            pincode=request.POST.get('pincode')
            phone=request.POST.get('phone')
            locality=request.POST.get('locality')
            address=request.POST.get('address')
            city=request.POST.get('city')
            landmark=request.POST.get('landmark')
            state=request.POST.get('state')
            order_notes=request.POST.get('order_notes')
            user_img=request.POST.get('user_img')


            one=profile_address(user=request.user,name=name,pincode=pincode,phone=phone,locality=locality,address=address,city=city,landmark=landmark,state=state,order_notes=order_notes,user_img=user_img)
            one.save()

            return redirect('shipping_address')




    return render(request,'Home/new_address.html')

def delete_address(request,id):
    a = profile_address.objects.get(id=id)
    a.delete()
    return redirect('shipping_address')


def edit_addres(request,id):

    if request.method=='POST':
        if request.user.is_authenticated:
            name=request.POST.get('name')
            pincode=request.POST.get('pincode')
            phone=request.POST.get('phone')
            locality=request.POST.get('locality')
            address=request.POST.get('address')
            city=request.POST.get('city')
            landmark=request.POST.get('landmark')
            state=request.POST.get('state')
            order_notes=request.POST.get('order_notes')

            edit=profile_address.objects.get(id=id)
            edit.name=name
            edit.pincode=pincode
            edit.phone=phone
            edit.locality=locality
            edit.address=address
            edit.city=city
            edit.landmark=landmark
            edit.state=state
            edit.order_notes=order_notes
            edit.save()
            return redirect('shipping_address')


    edit=profile_address.objects.get(id=id)
    dict={
        'edit':edit
    }



    return render(request,'Home/edit_address.html',dict)



#place order address

def placeaddress(request):
    
    if request.method=='POST':
            if request.user.is_authenticated:
                name=request.POST.get('name')
                pincode=request.POST.get('pincode')
                phone=request.POST.get('phone')
                locality=request.POST.get('locality')
                address=request.POST.get('address')
                city=request.POST.get('city')
                landmark=request.POST.get('landmark')
                state=request.POST.get('state')
                order_notes=request.POST.get('order_notes')

                one=billing_address(user=request.user,name=name,pincode=pincode,phone=phone,locality=locality,address=address,city=city,landmark=landmark,state=state,order_notes=order_notes)
                one.save()

            return redirect('checkout1')
    return render(request,'Home/place_address.html')

def editbillingadd(request,id):
    if request.method=='POST':
        if request.user.is_authenticated:
            name=request.POST.get('name')
            pincode=request.POST.get('pincode')
            phone=request.POST.get('phone')
            locality=request.POST.get('locality')
            address=request.POST.get('address')
            city=request.POST.get('city')
            landmark=request.POST.get('landmark')
            state=request.POST.get('state')
            order_notes=request.POST.get('order_notes')

            edit=billing_address.objects.get(id=id)
            edit.name=name
            edit.pincode=pincode
            edit.phone=phone
            edit.locality=locality
            edit.address=address
            edit.city=city
            edit.landmark=landmark
            edit.state=state
            edit.order_notes=order_notes
            edit.save()
            return redirect('checkout1')


    edit=billing_address.objects.get(id=id)
    dict={
        'edit':edit
    }
    return render(request,'Home/edit_biling_adress.html',dict)


def delete_billaddress(request,id):
    a = billing_address.objects.get(id=id)
    a.delete()
    return redirect('checkout1')






    




def cart(request):

    return redirect('/')



def checkout1(request):


    mcart=Cart.objects.filter(user=request.user)
    sub_total=0
    shipping = 40
    for items in mcart:
        if items.variations.vproduct.offers:
            sub_total+= items.product_qty*items.variations.offer_price()
        else:    
            sub_total+= items.product_qty*items.variations.price

    grand_total = sub_total + shipping


    a = billing_address.objects.filter(user=request.user)

    

    context={
        'a':a,
        'cart':mcart,
        'sub_total' : sub_total,
        'grand_total' : grand_total,
        'shipping': shipping,
    }

    if request.method=='POST':
        payment_mode=request.POST.get('payment')
        new_totaal = request.POST.get('new_totaal')
        address_id=request.POST.get('address')
        print(payment_mode,address_id,'sifan')
        # if payment_mode != 'Cash on delivery':
        #         messages.error(request,'please select Cash on delivery')
        #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        
        
        if not address_id:
                messages.error(request,'please select Address')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
        address = billing_address.objects.get(id=address_id)
        qty = 0
        if new_totaal:
            grand_total=new_totaal
        order=Order(user=request.user, address= address, total_amount=grand_total, mode_of_payment=payment_mode)
        order.save()
        for item in mcart:
            object=Ordered_Product(order_id=order, vproduct= item.variations, quantity= item.product_qty)
            object.save()
            # var = Ordered_Product.vproduct.quantity - Ordered_Product.quantity
            # var.save()
            item.delete()
        if payment_mode == 'Razorpay':
            return JsonResponse({'status' : "Yout order has been placed successfully"})
            
        
        return render(request,'Home/success_page.html',{'order':order,'products':Ordered_Product.objects.filter(order_id=order.id,),'sub_total' : sub_total})

            


    



    return render(request,'Home/checkout1.html',context)


def razorpay(request):

    cart=Cart.objects.filter(user=request.user)
    total_Price=0
    for items in cart:
        total_Price+= items.product_qty*items.variations.price
    return JsonResponse({'total_Price':total_Price})    


    




#category products
def category_products(request):
    return render(request,'Home/category_products.html')




# order success
def success(request):

    return render(request,'Home/success_page.html')


def order_history(request):
    if request.user.is_authenticated:

        order_history=Ordered_Product.objects.filter(order_id__user=request.user).order_by('-id')
    context={

        'order':order_history

    }
    return render(request,'Home/order_history.html',context)


def vieworderdetails(request,id):
    order=Ordered_Product.objects.filter(id=id)

    context={
        'order':order
    }
    return render(request,'Home/view_order_details.html',context)



def addtocart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            product_id=int(request.POST.get('product_id'))
            print("bilal")
            print(product_id)

            check=Variations.objects.get(id=product_id)

            if (check):
                if (Cart.objects.filter(user=request.user.id,variations_id=product_id)):
                    print('baxter')

                    return JsonResponse({'status':"Product already in cart"})

                else:
                    product_qty=int(request.POST.get('product_qty'))
                    if check.quantity >=product_qty:


                        Cart.objects.create(user=request.user,variations_id=product_id, product_qty=product_qty)
                        
                        return JsonResponse({'status':"product added successfully"})
                    else:
                        return JsonResponse({'status':"Only"+ str(check.quantity)+"quantity available"})
                            

            else:
                return JsonResponse ({'status':"No such Product found"})   


        else:
            return JsonResponse({'status' : "Login to continue"})    
        
    return redirect('/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log')
def mycart(request):

    mycart=Cart.objects.filter(user=request.user)
    # for item in mycart:
    #     if item.product_qty > item.variations.quantity:
    #         return JsonResponse({'status': "not allowed"})



    
    mycartitem=Cart.objects.filter(user=request.user)
    sub_total=0
    shipping = 40
    for items in mycartitem:
        if items.variations.vproduct.offers:
            sub_total+= items.product_qty*items.variations.offer_price()
        else: 
            sub_total+= items.product_qty*items.variations.price

    grand_total = sub_total + shipping
    context={
        'cart':mycartitem,
        'sub_total' : sub_total,
        'grand_total' : grand_total,
        'shipping': shipping,
    }


    return render(request,'Home/mycart.html',context)



def updatecart(request):

    if request.method=='POST':
        product_id=int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user.id,variations_id=product_id)):
            prod_qty=int(request.POST.get('product_qty'))
            cart=Cart.objects.get(user=request.user.id,variations_id=product_id)
            cart.product_qty=prod_qty
            cart.save()

            mcart=Cart.objects.filter(user=request.user)
            one=0
            shipping = 40


            for items in mcart:
                if items.variations.vproduct.offers:
                    one+= items.product_qty*items.variations.offer_price()
                    sub_total=one+shipping
                else:
                    one+= items.product_qty*items.variations.price
                    sub_total=one+shipping
                if items.product_qty == 10:
                    return JsonResponse({'status':"Only allowed this quantity", 'new_total': sub_total,})
                else:
                    
                    return JsonResponse({'status':"Updated Successfully", 'new_total': sub_total,})

   
        
    return redirect('/')    


def deletecartitem(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                cart_item = Cart.objects.get(variations_id=product_id, user=request.user)
                cart_item.delete()
                return JsonResponse({'status': 'Deleted Successfully'})
            except Cart.DoesNotExist:
                return JsonResponse({'status': 'Cart item not found'}, status=404)

    return redirect('/')

# profile picture

def profile_picture(request):
    return render(request,'Home/profile_picture.html')

#wish_list
def wishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    context={
        'wishlist':wishlist

    }
    return render(request,'Home/wishlist.html',context)

def addwishlist(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            product_id=request.POST.get('product_id')
            product_check=Variations.objects.get(id=product_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user,vproduct_id=product_id)):
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, vproduct_id=product_id)
                    return JsonResponse({'status':"Product added to wishlist"})
            else:
                return JsonResponse({'status':"Login to continue"})    
        else:
            return JsonResponse({'status':"Login to continue"}) 

    return redirect('/')

def deletewishlidtitem(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            product_id=int(request.POST.get('product_id'))

            if(Wishlist.objects.filter(user=request.user,vproduct_id=product_id)):
                wishlistitem = Wishlist.objects.filter(vproduct_id=product_id)
                wishlistitem.delete()
                return JsonResponse({'status':"Product removed from wishlist"})
            else:
                return JsonResponse({'status':"Product not found in wishlist"})
            
        else:
            return JsonResponse ({'status':"Login to continue"})    


def cancel_order(request,cancel_id):
   customer = request.user
   ord_prod = Ordered_Product.objects.get(id=cancel_id)
   ord_prod.status = 'Cancelled' 
   if ord_prod.order_id.mode_of_payment != "COD":
        amout = int(ord_prod.vproduct.price)
        print(amout,"sifan")
        customer.wallet = customer.wallet +amout
   ord_prod.vproduct.quantity += ord_prod.quantity
   ord_prod.order_id.total_amount -= amout
   ord_prod.order_id.save()
   ord_prod.vproduct.save()
   ord_prod.save()
   customer.save()


   messages.error(request,'Order Cancelled..!!')
   if ord_prod.order_id.mode_of_payment != "COD":
        messages.error(request,'Amount Refunded to your Wallet..!!')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 



def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        order_total = request.POST.get('order_total')
        order_total = float(order_total)
        coupon = Coupon.objects.filter(coupon_code=coupon_code).first()

        if coupon:
            coupon_used = CouponUsed.objects.filter(order__user=request.user,coupon__id=coupon.id)
            if coupon_used:
                return JsonResponse({'status': 'Coupon already used..'})
            else:
                if order_total>coupon.minimum_purchase:
                    new_total = order_total - coupon.discount
                    return JsonResponse({'status': 'Coupon Applied..!!','new_total':new_total,'coupon_discount':coupon.discount, 'coupon_code':coupon_code})
                else:
                   return JsonResponse({'status': 'You can not use this coupon..'}) 
        else:
            return JsonResponse({'status': 'Coupon does not exist..'})

    

    # invoice download

def invoicedownload(request,id):
    order=Ordered_Product.objects.filter(id=id)

    context={
        'order':order
    }
    return render(request,'Home/invoicedownload.html',context)



# Reset Password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log')
def reset_password(request):
   curr_pass = request.POST.get('curr_pass')
   new_pass1 = request.POST.get('new_pass')
   new_pass2 = request.POST.get('new_pass2')
   
   user = request.user
  
   if check_password(curr_pass,user.password ):
       if new_pass1 == new_pass2:
            try:
                validate_password(new_pass1)
            except ValidationError as e:
                # Handle the validation error
                error_message = ', '.join(e.messages)
                messages.error(request, error_message)
                return render(request,'Home/myprofile.html')
            user.set_password(new_pass1)
            user.save()
            messages.success(request,"Password Updated Successfully, Login Now..!")    
            return redirect('log')
       else:
            messages.success(request,"Passwords Missmatch..")    
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
           
   else:
        messages.success(request,"Please enter your correct password")    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




