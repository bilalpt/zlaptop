from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserOTP
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout as dj_logout
from .mixins import send_otp,verify_otp
from Login.models import Phone

# verification email
from .models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError




# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method=='POST':
        get_otp = request.POST.get('otp')

        if get_otp:
            get_email = request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                login(request,usr)
                messages.success(request,'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.error(request,'You enterd a wrong otp try again fail again')
                return render(request,'Login/signup.html',{'otp':True,'usr':usr})
            

        else:

            fname=request.POST['firstname']
            lname=request.POST['lastname']
            email=request.POST['Email']
            pass1=request.POST['Password']
            pass2=request.POST['Confirm Password']

#validation
            if fname.strip()==''or lname.strip()==''or email.strip()=='' or pass1.strip()=='' or pass2.strip()=='':
                messages.error(request,"Feild can't be blank") 
                return redirect('signup')
            if pass1!=pass2:
                messages.error(request,"Password dosn't match")
                return redirect('signup')
            
            if User.objects.filter(username=fname).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already takon')
                return redirect('signup')
            
            user=User.objects.create_user(username=fname,last_name=lname,email=email,password=pass1)
            user.is_active=False
            user.save()

            user_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=user, otp=user_otp) 

            mess=f'Hello\t{user.first_name},\nOTP to verify your account for Shopzee is {user_otp}\nHappy Shopping..!!'
            send_mail(
                    "Welcome to Shopzee, Verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
            messages.error(request,"Please enter OTP and Finish the registration..!!")
            return render(request,'Login/signup.html',{'otp':True,'usr':user})
            
            
    return render(request,'Login/signup.html')

# def log(request):
#     return render(request,'Login/login.html')


#Login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log(request):
    print('check')
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('home')
        else:
            return redirect('log')
    if request.method =="POST":
        fname = request.POST['Name']
        pass1 = request.POST['Password']
        user =authenticate(username=fname,password=pass1)
        print(user,'us')

# Validation
        if fname.strip() == '' or pass1.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('log')
        if user is not None:
            
            if request.user.is_superuser:
                auth.login(request, user)
                return redirect('home')
            else:
               auth.login(request, user)
               return redirect('home')
        else:
            messages.error(request, "Your usename or password is Incorrect")
            return redirect('log')
    return render(request,'Login/login.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='log')
# def home(request):
#     return render(request,'home.html')

# Logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log')
def logout(request):
    dj_logout(request)
    return redirect('log')

def mobileregister(request):
    
        if request.method=='POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            phone = request.POST['phone']
            password = request.POST['Password']
            confirm_password = request.POST['Confirm_Password']
            if password == confirm_password:
                if Phone.objects.filter(mobile=phone).exists():
                    print('phone no taken')
                    messages.error(request, 'Phone already taken!!')
                    return redirect('mobileregister')
                else:
                    user = User.objects.create_user(username=first_name,last_name=last_name,password=password)
                    user.save()
                    user.is_active = False
                    user.save()
                    print(user,'user')
                    new = Phone.objects.create(mobile=phone,user=user)
                    new.save()
                    print(new)
                    request.session['mobile'] = phone
                    request.session['username'] = first_name
                    strphone = int(phone)
                    send_otp(strphone)
                    return redirect('mobileotp')
            else:
                print('password do not match')
                messages.error(request, 'password do not match!!')
                return redirect('mobileregister')

    

            
        return render (request,'Login/mobile_signup.html')


def mobileotp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        phone = request.session['mobile']
        verify = verify_otp(phone,otp)
        username = request.session['username']
        user = User.objects.get(username=username)
        print(user)
        print(verify,'check')
        if verify:
            user.is_active = True
            user.save()
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect OTP, try again!!')
            print('incorrect otp')
            return redirect('mobileotp')




    return render(request,'Login/mobile_otp.html')




