from django.db import models
#from django_resized import ResizedImageField

class Categories(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2085)
    price = models.FloatField()
    stock = models.IntegerField(default=5)
    category = models.ForeignKey(Categories, related_name='category', null=True, on_delete=models.SET_NULL)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Customers(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=False)
    phone_num = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=2085, null=True)

    def __str__(self):
        return self.email

class Contact(models.Model):
    customer = models.ForeignKey(Customers, related_name='customer', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=2085)

    def __str__(self):
        return self.subject

class Product_Images(models.Model):
    name = models.CharField(max_length=255, null=True)
    product = models.ForeignKey(Products, related_name='products', on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to="images/")
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Banner_Images(models.Model):
    image_url = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.image_url)
