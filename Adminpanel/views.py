from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from Adminpanel.models import Product,brand,Variations,Processor,Ordered_Product,Order, Offers
from categories.models import category
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime,timedelta

# Admin Login

from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout as dj_logout

# Create your views here.

def addproduct(request):
    one=None


    if request.method=='POST':
        pname=request.POST.get('Product_name')
        brandname=request.POST.get('brandname')
        description=request.POST.get('description')
        price=request.POST.get('price')
        image=request.FILES.get('image')
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        # stock=request.POST.get('stock')
        specs=request.POST.get('specs')


        # stock=request.POST.get('stock')
        categ=request.POST.get('category')
        if pname=='' or brandname=='' or description=='' or specs=='' or price=='':
            messages.error(request,'please fill in the blanks')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        
        if not image:
            messages.error(request,'Please Add image')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        


        if int(price)<1:
            messages.error(request,'Please enter valuable amount')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


        
        catego = category.objects.get(id=categ)
        brnd = brand.objects.get(id=brandname)

        one=Product(product_name=pname,brandname=brnd,description=description,image=image,category=catego,image1=image1,image2=image2,image3=image3,price=price,specs=specs)
        one.save()

        messages.success( request,'Product  Added Successfully ')

        
        return redirect('addproduct')

        

    cat = category.objects.all().order_by('id')
    brnd = brand.objects.all().order_by('id')
    con={
        'A': cat,
        'B': brnd,
        
        }

    return render(request,'Adminpanel/addproduct.html',con)

def edit(request,id):
    if request.method=='POST':
        pname=request.POST.get('Product_name')
        brandname=request.POST.get('brandname')
        description=request.POST.get('description')
        price=request.POST.get('price')
        image=request.FILES.get('image')
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        specs=request.POST.get('specs')
        offer_id = request.POST.get('offers')
        categor=request.POST.get('category')




        # stock=request.POST.get('stock')
        if pname=='' or brandname=='' or description=='' or specs=='' or price=='':
            messages.error(request,'please fill in the blanks')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        
        if not image:
            messages.error(request,'Please Add image')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        


        if int(price)<1:
            messages.error(request,'Please enter valuable amount')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

        if offer_id:
            offer= Offers.objects.get(id=offer_id)
        else:
            offer=None  
        try:
            cat = category.objects.get(id=categor)
            bbrand= brand.objects.get(id=brandname)
        except:
            cat = None
            bbrand = None    


        a=Product.objects.get(id=id)

        a.product_name=pname
        a.brandname=bbrand
        a.description=description
        a.price=price
        a.image=image
        a.image1=image1
        a.image2=image2
        a.image3=image3 
        a.offers=offer
        a.specs=specs
        # a.stock=stock
        a.category=cat

        a.save()
        return redirect('product')
    
    cat = category.objects.all()
    brnd = brand.objects.all().order_by('id')



    a=Product.objects.get(id=id)  
    context={
        'cat':cat,
        'brnd':brnd,
        'product':a,
        'offers': Offers.objects.all().order_by('id')

    }
    return render(request,'Adminpanel/edit.html',context)

def delete(request,id):    
    dell=Product.objects.get(id=id)
    dell.delete()
    return redirect('product')
    

def ads(request):
    return render(request,'Adminpanel/ads.html')

def cupon(request):
    return render(request,'Adminpanel/cupon.html')

def customers(request):



    user=User.objects.filter(is_superuser=False)

        

    context={
        'customers':user 
    }

    return render(request,'Adminpanel/customers.html',context)


def search_customers(request):

    if 'custom' in request.GET:
        cust=request.GET['custom']

        if cust.strip()=='':
            messages.error(request,'No result found please try again ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        

        if customers:
            customer=User.objects.filter(username__icontains=cust)

        context={
            'customers':customer,

        }



    return render(request,'Adminpanel/customers.html',context)

    




def customer_block(request,user_id):
    user_details=User.objects.get(id=user_id)
    if user_details.is_active:
        user_details.is_active=False
        user_details.save()
    else:
        user_details.is_active= True
        user_details.save()
    return redirect('customers')    


def custtransaction(request):
    return render(request,'Adminpanel/customertransaction.html')

#Dashboard

def dashboard(request):
    delivered_items = Ordered_Product.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.order_id.total_amount

    top_selling = Ordered_Product.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = Ordered_Product.objects.all().order_by('-id')[:5]

    today = datetime.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    orders = Order.objects.filter(time__gte=four_days_ago, time__lte=today)

    sales_by_day = orders.annotate(day=TruncDay('time')).values('day').annotate(total_sales=Sum('total_amount')).order_by('day')
    sales_dates = Order.objects.annotate(sale_date=Cast('time', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':User.objects.count(),
        'sales':Ordered_Product.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'Adminpanel/dashboard.html',context)
from datetime import datetime, timedelta
#sales report
def salesreport(request):
    # if not request.user.is_superuser:
    #     return redirect('adminsignin')
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect(salesreport)
            
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = Ordered_Product.objects.filter(order_id__time__date=date_obj.date())
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'Adminpanel/salesreport.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect(salesreport)

        order_items = Ordered_Product.objects.filter(order_id__time__date__gte=start_date, order_id__time__date__lte=end_date)
        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date)
        else:
            messages.error(request, 'No data found')
    return render(request,'Adminpanel/salesreport.html',context)


def orderdetails(request):
    return render(request,'Adminpanel/orderdetails.html')

def products(request):
    
    products= Product.objects.all().filter(is_available=True)
    cat = category.objects.all().order_by('id')


    dict = {
        'one':products,
        'A':cat,


    }
    return render(request,'Adminpanel/products.html',dict)

def superuser(request):
    return render(request,'Adminpanel/superuser.html')

def common(request):

    return render(request,'Adminpanel/common.html')

def addbrand(request):
    if request.method=='POST':
        bname=request.POST.get('brand_name')
        bimage=request.FILES.get('brand_img')
        if bname=='':
            messages.error(request,' Please Fill the blank ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        
        if not bimage:
            messages.error(request,'Please Add Image')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        brands=brand(brand_name=bname,brand_img=bimage)
        brands.save()

        messages.success(request,'Brand Added Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        


    return render(request,'Adminpanel/addbrand.html')

def brand_details(request):
    bran=brand.objects.all()
    return render(request,'Adminpanel/brand_details.html',{'brand':bran})

def brand_search(request):

    if 'brand_search' in request.GET:
        
        brands=request.GET['brand_search']

        if brands.strip()=='':
            return redirect('bdetails')

        if brands:
            search_brand=brand.objects.filter(brand_name__icontains=brands)

            context={
                'brand':search_brand

            }

    return render(request,'Adminpanel/brand_details.html',context)


def edit_brand(request,edit_id):
    if request.method=='POST':
        bname=request.POST.get('brand_name')
        bimage=request.FILES.get('brand_img')

        if bname=='':
            messages.error(request,' Please Fill the blank ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        
        if not bimage:
            messages.error(request,'Please Add Image')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        

        bran=brand.objects.get(id=edit_id)
        bran.brand_name=bname
        bran.brand_img=bimage
        bran.save()

        messages.success(request,'Brand edited Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        



    bran=brand.objects.get(id=edit_id)    
    return render(request,'Adminpanel/edit_brand.html',{'brand':bran})

def delete_brand(request,del_id):
    one=brand.objects.get(id=del_id)
    one.delete()
    return redirect('bdetails')



def product_search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']

        if keyword.strip()=='':
            messages.error(request,'No result found please try again ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        

        
        if keyword:

            searchresult=Product.objects.filter(product_name__icontains=keyword)

        context={
            'one':searchresult,

        }
    return render(request,'Adminpanel/products.html',context)


def variations(request):


    if request.method=='POST':
        product   = request.POST.get('product')
        processor = request.POST.get('processor')
        quantity  = request.POST.get('quantity')
        price     = request.POST.get('price')



        product_list   = Product.objects.get(id=product)
        processor_list = Processor.objects.get(id=processor)


        one=Variations(vproduct=product_list,Vprocessor=processor_list,quantity=quantity,price=price)
        one.save()
        return redirect('variations')

    product_li=Product.objects.all().order_by('id')
    processor_li=Processor.objects.all().order_by('id')

        

    data={
        'product_name':product_li,
        'processor':processor_li,
            
    }
        

    return render(request,'Adminpanel/addvariants.html',data)
        
    
def ordermanage(request):

    order=Ordered_Product.objects.all()
    A=Ordered_Product.objects.all()


    context={
        'order':order,
        'A':A,

    }

    return render(request,'Adminpanel/order_manage.html',context) 



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):

    if request.method=="POST":
        fname = request.POST['Name']
        pass1 = request.POST['Password']
        user =authenticate(username=fname,password=pass1)

# Validation
        if fname.strip() == '' or pass1.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('adminlogin')
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('common')
        else:
            messages.error(request, "Your usename or password is Incorrect")
            return redirect('adminlogin')
        

    return render(request,'Adminpanel/Admin_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='adminlogin')
def Alogout(request):
    dj_logout(request)
    return redirect('adminlogin')



def update_status(request,id):
    order_item = Ordered_Product.objects.get(id=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        order_item.status = status
        order_item.save()
        return redirect('order_manage')
    


def varieant(request):

    varieant=Variations.objects.all()
    context={
        'varieant':varieant
    }
    return render(request,'Adminpanel/varient_listing.html',context)   

def deletevarient(request,id):
    a=Variations.objects.get(id=id)
    a.delete()

    return redirect('varieant')

def editvarieant(request,id):

    if request.method=='POST':
        product   = request.POST.get('product')
        processor = request.POST.get('processor')
        quantity  = request.POST.get('quantity')
        price     = request.POST.get('price')


        if int(quantity)<1:
            messages.error(request,'Please enter valuable amount')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


        if int(price)<1:
            messages.error(request,'Please enter valuable amount')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

        one=Variations.objects.get(id=id)

        one.vproduct.product_name=product
        one.Vprocessor.processor_list=processor
        one.quantity=quantity
        one.price=price
        one.save()

        return redirect('varieant')
    
    product_li=Product.objects.all()
    processor_li=Processor.objects.all()
    
    one=Variations.objects.get(id=id)

    data={
        'product_name':product_li,
        'processor':processor_li,
            
    }




    return render(request,'Adminpanel/editvarieant.html',data)


def salesinvoice(request):
    return render(request,'Adminpanel/salesinvoice.html')
    

def offers_list(request):
    if request.method == 'POST':
        offr_id = request.POST.get('offer_id')
        offr_name=  request.POST.get('name')
        discount=  request.POST.get('discount')
        start_date=  request.POST.get('start_date')
        end_date=  request.POST.get('end_date')
        
        offer = Offers.objects.get(id=offr_id)
       
        if offr_name:
            offer.name =offr_name
        if discount:
            offer.discount =discount
        if start_date:
            offer.start_date =start_date   
        if end_date:
            offer.end_date =end_date
            
        offer.save() 
        
        messages.success(request, 'New update added successfully')            
        return render(request, 'Adminpanel/offers_list.html', {'offers': Offers.objects.all().order_by('id')})
        
        
    return render(request, 'Adminpanel/offers_list.html', {'offers': Offers.objects.all().order_by('id')})


def add_offer(request):
        offr_name=  request.POST.get('name')
        discount=  request.POST.get('discount')
        start_date=  request.POST.get('start_date')
        end_date=  request.POST.get('end_date')
        
        if not start_date:
            messages.success(request, 'Date Field cant be empty..!')
            return redirect('offers_list')
        if not end_date:
            messages.success(request, 'Date Field cant be empty..!')
            return redirect('offers_list')
            
        if offr_name:
            offr_name= offr_name.strip()
            exist = Offers.objects.filter(name= offr_name)
            if exist:
                messages.success(request, 'Offer name already exist..!')
                return redirect('offers_list')
            if discount: 
                Offers.objects.create(name=offr_name, discount= discount, start_date= start_date, end_date= end_date)
                return redirect('offers_list') 
            else:
                messages.success(request, 'Please Specify a discount..!')
                return redirect('offers_list')  
                    
        else:
            messages.success(request, 'Offer should have a name..!')
            return redirect('offers_list')
  