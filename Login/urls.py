from django.contrib import admin
from django.urls import include,path
from .import views

urlpatterns = [
    path('log',views.log,name='log'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('mobileregister',views.mobileregister,name='mobileregister'),
    path('mobileotp',views.mobileotp,name='mobileotp'),
    # Forgot Pass
    path('forgot_password',views.forgot_password,name='forgot_password'),


]