"""
Local development settings for .
These settings are optimized for local development environment.
"""

from .base import *

# Debug mode for development
DEBUG = True

# Additional allowed hosts for local development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database configuration for local development
# Using SQLite for simplicity in local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Email configuration for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Additional development-specific settings
# Disable password validation for easier development
AUTH_PASSWORD_VALIDATORS = []

# Enable Django debug toolbar if installed
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
