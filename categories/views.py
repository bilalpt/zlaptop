from django.shortcuts import render,redirect
from .models import category
from django.contrib import messages



# Create your views here.



def categ(request):
    categories = category.objects.all()

    products = {
        'two': categories,

    }
    return render(request,'Adminpanel/category.html',products)

def search_category(request):

    if 'category' in request.GET:
        categ=request.GET['category']

        if categ.strip()=='':
            return redirect('category')

        if categ:
            cat=category.objects.filter(category_name__icontains=categ)

        products={
            'two':cat
            }

    return render(request,'Adminpanel/category.html',products)



#Add category

def addcategory(request):
    if request.method=='POST':
        category_name = request.POST['category_name']
        description   = request.POST['description']
        cart_img    = request.FILES.get('cart_img')

#validation
        if category_name.strip()=='' or description.strip()=='':
            messages.error (request, 'Please Fill in the blank')
            return redirect('addcategory')

        if not cart_img:
            messages.error(request,'image not found')
            return redirect('addcategory')
        
        if description.strip()=='':
            messages.error(request,'image not found')
            return redirect('addcategory')

#save   
        categor=category(category_name=category_name,description=description,cart_img=cart_img)
        categor.save()

        messages.success(request,'Category Added Successfully')

    return render(request,'Adminpanel/addcategory.html')

def edi_category(request,id):
    if request.method=='POST':
        category_name=request.POST.get('category_name')
        description=request.POST.get('description')
        cart_img=request.FILES.get('cart_img')
        cat=category.objects.get(id=id)

        cat.category_name=category_name
        cat.description=description
        cat.cart_img=cart_img
        cat.save()
        # return redirect('edi_category')

        
    cat=category.objects.get(id=id)    
    return render(request,'categories/edit_category.html',{'data':cat})


def delete_category(request,id):
    one=category.objects.get(id=id)
    one.delete()
    return redirect('category')
