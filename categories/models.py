from django.db import models

# Create your models here.

class category(models.Model):
    category_name = models.CharField(max_length=60,)
    slug          = models.SlugField(max_length=255,)
    description   = models.CharField(max_length=255)
    cart_img      =models.ImageField(upload_to='photos/categories',null=True)

    # class Meta:
    #     verbos_name='category'
    #     verbos_name_plural ='categories'

    def __str__(self):
        return self.category_name    
    

       


