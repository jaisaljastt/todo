"""
Production settings for AWS deployment
"""
from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts for production
ALLOWED_HOSTS = [
    '13.53.41.170',  # EC2 public IP
    'localhost',
    '127.0.0.1',
]

# Database configuration for AWS RDS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('RDS_DB_NAME'),  # rds_db_name in .env
        'USER': os.environ.get('RDS_USERNAME'),  # rds_username in .env
        'PASSWORD': os.environ.get('RDS_PASSWORD'),  # rds_password in .env
        'HOST': os.environ.get('RDS_HOSTNAME'),  # rds_hostname in .env
        'PORT': os.environ.get('RDS_PORT', '3306'),  # rds_port in .env
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Collected static files directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Your project's static files
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP server
EMAIL_PORT = 587  # Gmail SMTP port
EMAIL_USE_TLS = True  # Required for Gmail
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  # Your Gmail address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # Your app password
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')  # Sender's email address


# Logging configuration for console output
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

