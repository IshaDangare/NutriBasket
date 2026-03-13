from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import logging
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import random
import razorpay
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from .utils import load_nutrition_data

logger = logging.getLogger(__name__)

# common helper to populate nutrition attributes on cart items

def _annotate_cart_with_nutrition(cart_items):
    nutrition_data = load_nutrition_data()
    for item in cart_items:
        name = item.product_id.product_name.lower()
        if name in nutrition_data:
            data = nutrition_data[name]
            item.calories = data["calories"] * item.qty
            item.protein = data["protein"] * item.qty
            item.carbs = data["carbs"] * item.qty
            item.fat = data["fat"] * item.qty
        else:
            item.calories = 0
            item.protein = 0
            item.carbs = 0
            item.fat = 0

# Create your views here.
def index(request):
    # allproduct = Product.objects.all()
    # context={'allproduct':allproduct}
    return render(request,"index.html")

def product(request):
    allproduct = Product.objects.all()
    context={'allproduct':allproduct}
    return render(request,"product.html",context)

def dairyproductlistview(request):
    if request.method == "GET":
        allproduct = Product.prod.get_dairyproduct_list()
        context = {'allproduct':allproduct}
        return render(request,"product.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render(request,"product.html",context)
    
def meatproductlistview(request):
    if request.method == "GET":
        allproduct = Product.prod.get_meatproduct_list()
        context = {'allproduct':allproduct}
        return render(request,"product.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render(request,"product.html",context)
    
def organicfoodlistview(request):
    if request.method == "GET":
        allproduct = Product.prod.get_organicfood_list()
        context = {'allproduct':allproduct}
        return render(request,"product.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render(request,"product.html",context)
    
def fruitslistview(request):
    if request.method == "GET":
        allproduct = Product.prod.get_fruits_list()
        context = {'allproduct':allproduct}
        return render(request,"product.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render(request,"product.html",context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)
    
def aboutus(request):
    return render(request,"about.html")

def contactus(request):
    return render(request,"contact.html")
    
def services(request):
    return render(request,"services.html")


def cart(request):
    """Render the shopping cart and annotate each line with nutrition info.

    The customer must be authenticated in the original logic, but the previous
    implementation attempted to handle anonymous users by still querying
    `request.user.id`.  We'll keep the same structure but always compute the
    nutrition details whether or not the user is logged in; the lookup simply
    ignores user metadata when ``user`` is ``None``.
    """

    user = request.user if request.user.is_authenticated else None
    allcarts = Cart.objects.filter(user_id=user.id if user else None)
    total_price = sum(x.product_id.price * x.qty for x in allcarts)
    length = len(allcarts)

    # add calories/protein/etc fields to each cart item
    _annotate_cart_with_nutrition(allcarts)

    context = {
        "cart_items": allcarts,
        "total": total_price,
        "items": length,
    }
    if user:
        context["username"] = user.username

    return render(request, "cart.html", context)

def addtocart(request,product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    allproduct = get_object_or_404(Product,product_id=product_id)
    cart_item,created = Cart.objects.get_or_create(product_id=allproduct, user_id = user)
    if not created:
        cart_item.qty +=1
    else:
        cart_item.qty = 1
    cart_item.save()
    return redirect('cart')

def updateqty(request,qv,product_id):
    allcarts = Cart.objects.filter(product_id=product_id)
    if qv=="1":
        total = allcarts[0].qty + 1
        allcarts.update(qty=total)
    else:
        if allcarts[0].qty>1:
            total = allcarts[0].qty - 1
            allcarts.update(qty=total)
        else:
            allcarts = Cart.objects.filter(product_id = product_id)
            allcarts.delete()
    return redirect('cart')

def remove_from_cart(request,product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    cart_item = Cart.objects.filter(product_id=product_id, user_id = user)
    cart_item.delete()
    return redirect("cart")


def remove_from_order(request,product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    cart_item = Cart.objects.filter(product_id=product_id, user_id = user)
    cart_item.delete()
    return redirect("cart")

def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    allcarts = Cart.objects.filter(user_id = user)
    total_price = 0
    for x in allcarts:
        total_price += x.product_id.price * x.qty
        
    length = len(allcarts)
    context = {}
    context['cart_items'] = allcarts
    context['total'] = total_price
    context['items'] = length
    context['username'] = user

    return render(request,'placeorder.html',context)

    

def showorders(request):
    if request.user.is_authenticated:
        user = request.user
        allorders = Order.objects.filter(user_id=user)
        totalprice = 0

        for x in allorders:
            totalprice = totalprice + x.product_id.price * x.qty
            # annotate order with computed amount for template
            x.amount = x.product_id.price * x.qty
            length = len(allorders)

        context = {
            "username" : user,
            "allorders" : allorders,
            'totalprice' : totalprice,
            # 'length' : length,
        }
        return render(request, "showorders.html", context)
    else:
        # Redirect unauthenticated users to login page
        return redirect('/app2/signin/')

def makepayment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        subject = "Payment Received - Order Confirmation"
        message = f"""
Dear {name},

Thank you for your payment.

We will check your payment details and process your order soon.
Your product will be delivered shortly.

Thank you for shopping with us!

Best regards,
NutriBasket Team
"""

        try:
            result = send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            logger.info(f"Confirmation email sent successfully to {email}")
            context = {'success': True, 'email': email}
            return render(request, 'success.html', context)
        except Exception as e:
            logger.error(f"Failed to send confirmation email to {email}: {str(e)}", exc_info=True)
            context = {'success': False, 'error': str(e), 'email': email}
            return render(request, 'success.html', context)

    return render(request, 'makepayment.html')


def payment_complete(request):
    """Handle the "I Have Completed Payment" action:

    - Move cart items into `Order` records with status 'pending'
    - Send a confirmation email to the provided email address
    - Clear the cart for the user
    """
    if request.method != 'POST':
        return redirect('cart')

    name = request.POST.get('name')
    email = request.POST.get('email')

    user = request.user if request.user.is_authenticated else None

    # get cart items for this user (or anonymous rows where user_id is null)
    cart_items = Cart.objects.filter(user_id=user.id if user else None)

    if not cart_items:
        # nothing to do
        return redirect('cart')

    # create order rows
    orders_created = []
    for ci in cart_items:
        o = Order.objects.create(
            user_id=user,
            product_id=ci.product_id,
            qty=ci.qty,
            status='pending'
        )
        orders_created.append(o)

    # clear cart
    cart_items.delete()

    # send confirmation email
    subject = "Payment Received - Order Pending"
    message = f"""
Dear {name or (user.username if user else 'Customer')},

We have received notification that you completed the payment.
We will check the payment and your product will be delivered soon.

Order status: Pending

Thank you for shopping with us!
"""
    try:
        logger.info(f"Sending payment confirmation email to {email} from {settings.EMAIL_HOST_USER}")
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER, 
            [email], 
            fail_silently=False
        )
        logger.info(f"Email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}", exc_info=True)
        print(f"Email error: {e}")

    return redirect('showorders')

def nutrition_calculator(request):
    result = None
    
    if request.method == "POST":
        food_name = request.POST.get("food")
        quantity = float(request.POST.get("quantity"))

        try:
            food = Food.objects.get(name=food_name)

            factor = quantity / 100

            result = {
                "calories": food.calories_per_100g * factor,
                "protein": food.protein_per_100g * factor,
                "carbs": food.carbs_per_100g * factor,
                "fat": food.fat_per_100g * factor,
            }
        except Food.DoesNotExist:
            result = "Food not found"

    return render(request, "calculator.html", {"result": result})


def get_calories(request):
    """Return nutrition information for a product read from product.text.

    Expects a GET parameter ``name`` with the product name.  Response is a
    small JSON blob or a 404 when the name isn't found.
    """

    name = request.GET.get("name", "").strip().lower()
    if not name:
        return JsonResponse({"error": "Missing name"}, status=400)

    data = load_nutrition_data().get(name)
    if not data:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse(data)

API_KEY = "your_api_key"

def get_food_data(food_name):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data


# Password Reset Views
def password_reset_request(request):
    """Display form to request password reset."""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset link
            reset_link = f"{request.build_absolute_uri('/password_reset_confirm/')}{uid}/{token}/"
            
            # Send email
            subject = "Password Reset Request"
            message = f"""
Dear {user.username},

We received a request to reset your password. Click the link below to reset it:

{reset_link}

This link will expire in 24 hours.

If you didn't request this, ignore this email.

Thank you,
NutriBasket Team
"""
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                logger.info(f"Password reset email sent to {email}")
                return render(request, 'password_reset_sent.html', {'email': email})
            except Exception as e:
                logger.error(f"Failed to send password reset email: {e}")
                return render(request, 'password_reset_request.html', {'error': 'Failed to send email. Please try again.'})
        except User.DoesNotExist:
            # Don't reveal if email exists (security best practice)
            return render(request, 'password_reset_sent.html', {'email': email})
    
    return render(request, 'password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    """Reset password using token."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password2 and password1 == password2:
                user.set_password(password1)
                user.save()
                logger.info(f"Password reset successful for user {user.username}")
                return render(request, 'password_reset_complete.html')
            else:
                return render(request, 'password_reset_confirm.html', {'error': 'Passwords do not match.'})
        
        return render(request, 'password_reset_confirm.html')
    else:
        return render(request, 'password_reset_invalid.html')