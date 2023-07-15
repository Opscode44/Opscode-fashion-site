from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch
from PIL import Image
from io import BytesIO
from .models import Products, Product_Images, Customers, Contact, Banner_Images
import base64

def resize_to_thumbnail(image):
    image_thumbnail = Image.open(image)
    image_thumbnail = image_thumbnail.resize((150, 105))
    thumbnail_stream = BytesIO()
    image_thumbnail.save(thumbnail_stream, format='JPEG')
    thumbnail_stream.seek(0)

    image_thumbnail_base64 = base64.b64encode(thumbnail_stream.getvalue()).decode('utf-8')
    return image_thumbnail_base64

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            check_email = Customers.objects.filter(email = email).exists()
            if check_email:
                return JsonResponse({"subscribe_message":"This Email is already Subscribed to us, you must really like us to want to subscribe again. Thanks"})
            else:
                new_subcriber = Customers()
                new_subcriber.email = email
                new_subcriber.save()
                return JsonResponse({"subscribe_message":"You are successfully subscribed to us, don't worry we won't bore you with boring newsletters or updates"}) 
        else:
            return JsonResponse({"subscribe_message":"Please Enter an Email Address"})
    else:
        return("")


def index(request):
    #featured = Product_Images.objects.select_related('product').filter(product__featured = True, default = True)
    featured = Products.objects.filter(featured = True).prefetch_related(
        Prefetch('products', queryset=Product_Images.objects.filter(default = True), to_attr='default_image')
    )
    banner_images = Banner_Images.objects.all()
    return render(request, 'index.html', context={"featured":featured, "banner_images":banner_images})

def products(request):
    #all_products = Product_Images.objects.select_related('product').filter(default = True)
    all_products = Products.objects.all().prefetch_related(
        Prefetch('products', queryset=Product_Images.objects.filter(default = True), to_attr='default_image')
    )
    return render(request, 'products.html', context={"all_products":all_products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        check_email = Customers.objects.filter(email = email).exists()
        if check_email:
            new_customer = Customers.objects.get(email=email)
            if new_customer.name is None:
                new_customer.name = name
                new_customer.save()
        else:
            new_customer = Customers.objects.create(name = name, email = email)
            new_customer.save()
        
        new_message = Contact.objects.create(customer = new_customer, subject = subject, message = message)
        new_message.save()
        return JsonResponse({"result":"Thank you for contacting us, we will reachout to you ASAP"})

        

    return render(request, 'contact.html')

def single_product(request, id):
    item = Products.objects.get(id = id)
    item_images = Product_Images.objects.filter(product = item, default = False)
    thumbnail_list = []
    for image in item_images:
        image_thumbnail = resize_to_thumbnail(image.image_url)        
        thumbnail_list.append(image_thumbnail)

    #also_like_items = Product_Images.objects.select_related('product').filter(product__category = item.category,
    #                                                                          default = True)
    also_like_items = Products.objects.filter(category=item.category).prefetch_related(
        Prefetch('products', queryset=Product_Images.objects.filter(default=True), to_attr='default_image')
    )

    return render(request, 'single-product.html', context = {"item":item, "item_images":item_images, 
                                                             "also_like_items":also_like_items, "thumbnail_list":thumbnail_list})

def terms(request):
    return render(request, 'terms.html')
