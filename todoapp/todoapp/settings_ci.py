from .settings import *

# Database settings for CI environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'todo',
        'HOST': '127.0.0.1',  # Use IP instead of 'localhost' to force TCP connection
        'PORT': '3306',       # Explicitly set the port
        'USER': 'root',
        'PASSWORD': 'root'
    }
}