#!/bin/bash

# Navigate to the Django project directory
cd /home/pi/Node

# Activate the virtual environment
source envsmart/bin/activate

# Run the Django development server
python manage.py runserver 0.0.0.0:8000
