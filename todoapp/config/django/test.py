from .base import *
import os

# Database settings for CI environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('TEST_DB_NAME', 'todo'),
        'HOST': os.environ.get('TEST_DB_HOST', '127.0.0.1'),  # Use IP instead of 'localhost' to force TCP connection
        'PORT': os.environ.get('TEST_DB_PORT', '3306'),       # Explicitly set the port
        'USER': os.environ.get('TEST_DB_USER', 'root'),
        'PASSWORD': os.environ.get('TEST_DB_PASSWORD', 'root')
    }
}
