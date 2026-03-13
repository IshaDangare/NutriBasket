"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('product/',views.product,name="product"),
    path('services/',views.services,name="services"),
    path('cart/',views.cart,name="cart"),
    path('addtocart/<int:product_id>',views.addtocart,name="addtocart"),
    path("updateqty/<qv>/<product_id>",views.updateqty, name="updateqty"),
    path("remove_from_cart/<int:product_id>",views.remove_from_cart, name="remove_from_cart"),
    path("remove_from_order/<int:product_id>",views.remove_from_order, name="remove_from_order"),
    path('showorders',views.showorders,name="showorders"),
    path('contactus/',views.contactus,name="contactus"),
 
    path('calculator/', views.nutrition_calculator, name='nutrition_calculator'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('get_calories/', views.get_calories, name='get_calories'),

    path('payment_complete/', views.payment_complete, name='payment_complete'),

    path('dairyproductlistview/',views.dairyproductlistview,name="dairyproductlistview"),
    path('meatproductlistview/',views.meatproductlistview,name="meatproductlistview"),
    path('organicfoodlistview/',views.organicfoodlistview,name="organicfoodlistview"),
    path('fruitslistview/',views.fruitslistview,name="fruitslistview"),
   
    path('makepayment/', views.makepayment, name='makepayment'),

    path('placeorder/',views.placeorder,name="placeorder"),

    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
