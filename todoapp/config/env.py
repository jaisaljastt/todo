"""
Environment configuration for todoapp.
This file can be used to set environment-specific variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment detection
def get_environment():
    """Determine the current environment"""
    return os.environ.get('DJANGO_ENV', 'development').lower()

# Environment-specific settings
ENVIRONMENT = get_environment()

# You can add environment-specific logic here
if ENVIRONMENT == 'production':
    # Production-specific settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.production')
elif ENVIRONMENT == 'test':
    # Test-specific settings  
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.test')
else:
    # Development/local settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')
