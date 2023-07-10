from django.db import models
from categories.models import category
from django.contrib.auth.models import User

# from Adminpanel.models import brand

# Create your models here.

class brand(models.Model):
    brand_name = models.CharField(max_length=60,)
    slug          = models.SlugField(max_length=255,)
    brand_img      =models.ImageField(upload_to='photos/brand',blank=True)


    def __str__(self):
        return self.brand_name
        


class Product(models.Model):
    product_name   = models.CharField(max_length=200)
    brandname      = models.ForeignKey(brand,on_delete=models.CASCADE,blank=True, null=True)
    slug           = models.SlugField(max_length=255)
    description    = models.CharField(max_length=255,blank=True)
    price          = models.IntegerField(null=True)
    image          = models.ImageField(upload_to='photos/products')
    image1         = models.ImageField(upload_to='photos/products',null=True,blank=True)
    image2         = models.ImageField(upload_to='photos/products',null=True,blank=True)
    image3         = models.ImageField(upload_to='photos/products',null=True,blank=True)
    stock          = models.IntegerField(null=True)
    is_available   = models.BooleanField(default=True)
    category       = models.ForeignKey(category,on_delete=models.CASCADE,blank=True, null=True)
    create_date    = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now_add=True)
    specs          = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.product_name
    


# processor section

class Processor(models.Model):
    processor_list= models.CharField(max_length=20)

    def __str__(self):
        return self.processor_list




# variation section

class Variations(models.Model):
    vproduct   = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    Vprocessor = models.ForeignKey(Processor,on_delete=models.CASCADE,blank=True,null=True)
    quantity   = models.IntegerField(null=True)
    price      = models.IntegerField(null=True)



    def __str__(self):
        return f"{self.vproduct.product_name} - {self.Vprocessor.processor_list}"



    

class Cart(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False, default=1)
    created_at  = models.DateTimeField(auto_now_add=True)
    variations  = models.ForeignKey(Variations,on_delete=models.CASCADE)

    def __str__(self):
        return self.variations.vproduct.product_name



class profile_address(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name        = models.CharField(max_length=255,null=True)
    pincode     = models.CharField(max_length=255,null=True)
    phone       = models.CharField(max_length=14,null=True)
    locality    = models.CharField(max_length=255,null=True)
    address     = models.CharField(max_length=255,null=True)
    city        = models.CharField(max_length=255,null=True)
    landmark    = models.CharField(max_length=255,null=True)
    state       = models.CharField(max_length=255,null=True)
    order_notes = models.CharField(max_length=255,null=True)
    user_img    = models.ImageField(upload_to='photos/my_profile',null=True)



class billing_address(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name        = models.CharField(max_length=255,null=True)
    pincode     = models.CharField(max_length=255,null=True)
    phone       = models.CharField(max_length=14,null=True)
    locality    = models.CharField(max_length=255,null=True)
    address     = models.CharField(max_length=255,null=True)
    city        = models.CharField(max_length=255,null=True)
    landmark    = models.CharField(max_length=255,null=True)
    state       = models.CharField(max_length=255,null=True)
    order_notes = models.CharField(max_length=255,null=True)    







class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address = models.ForeignKey(billing_address, on_delete=models.CASCADE, null=True)
    total_amount = models.BigIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    mode_of_payment = models.CharField(max_length=50,blank=True, null=True)
    payment_id = models.CharField(max_length=250,null=True)
    tracking_no=models.CharField(max_length=250,null=True)
    message = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Ordered_Product(models.Model):
    order_id =  models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    vproduct  =  models.ForeignKey(Variations, on_delete=models.CASCADE,blank=True, null=True )
    quantity = models.BigIntegerField()
    amount   = models.DecimalField(max_digits=20, decimal_places=2 ,null=True) 
    sample =models.CharField(max_length=250,blank=True)
    time = models.DateField(auto_now_add=True,null=True, blank=True)


    STATUS = (
        ('Pending','Pending'),
        ('Out for Shiping','Out for Shiping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return', 'Return'),

    )
    status = models.CharField(choices=STATUS,default='Pending')



class Wishlist(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    vproduct=models.ForeignKey(Variations,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class Coupon(models.Model):
    coupon_code= models.CharField(max_length=50)
    discount = models.BigIntegerField()
    minimum_purchase  = models.BigIntegerField()
    is_active = models.BooleanField(default=False)


class CouponUsed(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE, blank=True, null=True)    




    

   





          