# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# import uuid




        





# class CustomUserManager(BaseUserManager):
#     """Define a model manager for User model with no username field."""

#     def _create_user(self, email,phone, password=None, **extra_fields):
#         """Create and save a User with the given email and password."""
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email,phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email,phone, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email,phone,password, **extra_fields)

#     def create_superuser(self, email,phone, password=None, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(email, phone,password, **extra_fields)
        


# class CustomUser(AbstractUser):
    
#     email = models.EmailField(_('email address'), unique=True)
#     phone = models.IntegerField(unique=True, verbose_name='Phone Number',blank=False, help_text='Enter 10 digits phone number')
    

#     objects = CustomUserManager()

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
   
    

#     objects = CustomUserManager()

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'



from django.contrib.auth.models import User
from django.db import models

class UserOTP(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True) 
    otp  =models.BigIntegerField()

class Phone(models.Model):

    # mobile = models.IntegerField()
    mobile = models.CharField(unique=True, max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE)




    
