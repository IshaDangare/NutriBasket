from django.urls import path
from app2 import views
urlpatterns = [
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    path('register/',views.register,name="register"),
    path('contact_form_submission/',views.contact_form_submission,name="contact_form_submission")

]
