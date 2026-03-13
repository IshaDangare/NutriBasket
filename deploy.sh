#!/bin/bash
# Quick local setup script for NutriBasket
set -e

if [ -z "$VIRTUAL_ENV" ]; then
  python3 -m venv venv
  source venv/bin/activate
fi
pip install --upgrade pip
pip install -r requirements.txt
python ecom/manage.py migrate
python ecom/manage.py collectstatic --noinput
python ecom/manage.py runserver
