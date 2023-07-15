from django.urls import path
from . import views

#app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('products/<id>/', views.single_product, name='singleproduct'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('terms', views.terms, name='terms')
]