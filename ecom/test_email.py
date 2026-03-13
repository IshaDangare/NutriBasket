#!/usr/bin/env python
"""Test script to verify email configuration works."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
import sys
sys.path.insert(0, r'c:\Users\rajhd\Downloads\nutribasket_project\ecom')

django.setup()

from django.core.mail import send_mail
from django.conf import settings

# Test email configuration
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")

# Use the same email from settings (send to self)
test_to_email = settings.EMAIL_HOST_USER

try:
    print(f"\nAttempting to send test email to {test_to_email}...")
    send_mail(
        subject="NutriBasket - Test Email",
        message="This is a test email from NutriBasket. If you received this, email configuration is working!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[test_to_email],
        fail_silently=False
    )
    print("✓ Email sent successfully!")
except Exception as e:
    print(f"✗ Failed to send email:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nCommon issues:")
    print("1. Gmail might be blocking due to 'Less secure app access' - go to https://myaccount.google.com/lesssecureapps")
    print("2. Or use an App Password instead of your regular password - go to https://myaccount.google.com/apppasswords")
    print("3. Check EMAIL_HOST_PASSWORD is correct in settings.py")

