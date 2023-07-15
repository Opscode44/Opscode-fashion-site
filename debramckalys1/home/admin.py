from django.contrib import admin
from .models import Products, Product_Images, Categories, Customers, Contact, Banner_Images

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')

class Product_ImagesInline(admin.StackedInline):
    model = Product_Images
    
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    inlines = [Product_ImagesInline]

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_num', 'address')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('customer', 'subject', 'message')

class Banner_ImagesAdmin(admin.ModelAdmin):
    list_display = ('id','image_url')

admin.site.register(Products, ProductsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Banner_Images, Banner_ImagesAdmin)