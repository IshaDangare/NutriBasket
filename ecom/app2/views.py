from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout


from django.core.mail import send_mail
from django.conf import settings


def register(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        name = request.POST.get('name')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        context = {}

        if not uname or not name or not pass1 or not pass2:
            context['error'] = "All fields are required"
            return render(request, "auth/register.html", context)

        if pass1 != pass2:
            context['error'] = "Passwords do not match"
            return render(request, "auth/register.html", context)

        if User.objects.filter(username=uname).exists():
            context['error'] = "Username already exists"
            return render(request, "auth/register.html", context)

        user = User.objects.create_user(
            username=uname,
            first_name=name,
            password=pass1
        )
        user.save()

        return redirect("signin")

    return render(request, "auth/register.html")

def signin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        name = request.POST.get('name')
        pass1 = request.POST.get('pass1')
        context={}
        if uname=="" or pass1=="" or name=="":
            context['error'] = "Fields can't be empty"
            return render(request,"auth/signin.html",context)
        else:
            user = authenticate(username=uname, password=pass1)
            if user is not None:
                login(request,user)
                return redirect("index")
            else:
                context['error'] = "Invalid username or password"
                return render(request,"auth/signin.html",context)
    else:
        return render(request,"auth/signin.html")

def signout(request):
    logout(request)
    return redirect('index')

def contact_form_submission(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            subject,
            f"Name: {name}\nEmail: {email}\nMessage: {message}",
            settings.DEFAULT_FROM_EMAIL,
            ['isha192001@gmail.com'],  # Change to the recipient's email address
            fail_silently=False,
        )
        return HttpResponse('Your message has been sent. Thank you!')
    else:
        return HttpResponse('Method not allowed')

