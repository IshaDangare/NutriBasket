#!/usr/bin/env python
"""Quick test to verify payment completion email sending."""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
sys.path.insert(0, r'c:\Users\rajhd\Downloads\nutribasket_project\ecom')

django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("PAYMENT EMAIL TEST - NutriBasket Payment Confirmation")
print("=" * 60)

print(f"\n📧 Email Configuration:")
print(f"   HOST: {settings.EMAIL_HOST}")
print(f"   PORT: {settings.EMAIL_PORT}")
print(f"   FROM: {settings.EMAIL_HOST_USER}")
print(f"   USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"   BACKEND: {settings.EMAIL_BACKEND}")

test_email = settings.EMAIL_HOST_USER
customer_name = "Test Customer"

# Simulate payment completion email
subject = "Payment Received - Order Pending"
message = f"""
Dear {customer_name},

We have received notification that you completed the payment.
We will check the payment and your product will be delivered soon.

Order status: Pending

Thank you for shopping with us!
"""

print(f"\n📨 Test Email Details:")
print(f"   TO: {test_email}")
print(f"   SUBJECT: {subject}")

try:
    print(f"\n⏳ Attempting to send email...")
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [test_email],
        fail_silently=False
    )
    print("✅ SUCCESS! Email sent successfully!")
    print("\n🎉 Payment confirmation emails will work after payment!")
except Exception as e:
    print(f"❌ FAILED to send email:")
    print(f"   Error: {type(e).__name__}: {str(e)}")
    print("\n⚠️  SOLUTION NEEDED:")
    print("   1. Go to: https://myaccount.google.com/apppasswords")
    print("   2. Select 'Mail' and 'Windows'")
    print("   3. Generate and copy the 16-character password")
    print("   4. Reply with the password and I'll update settings.py")
