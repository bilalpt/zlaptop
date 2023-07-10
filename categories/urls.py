from django.contrib import admin
from django.urls import include,path
from .import views

urlpatterns = [
    path('category',views.categ,name='category'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('edi_category/<int:id>',views.edi_category,name='edi_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('search_category',views.search_category,name='search_category'),




]