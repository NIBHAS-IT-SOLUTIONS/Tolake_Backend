from pathlib import Path
import mimetypes
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-4)pss#u+j-$&@d1y8^q_@pkgl6-u%y1jp-=47kfk)0ak=$x5)*'
DEBUG = False
ALLOWED_HOSTS = ['tolake.in']  # Update to ['tolake.in'] in production

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'houseboat',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ALLOW_ALL_ORIGINS = False  # Disable this for production
CORS_ALLOWED_ORIGINS = [
    "https://tolake.in",  # ✅ Allow only your WordPress site
    "https://www.tolake.in",
    "https://nibhas.pythonanywhere.com",
]

# CORS_ALLOW_METHODS = [
#     "GET",
#     "POST",
#     "PUT",
#     "PATCH",
#     "DELETE",
#     "OPTIONS",
# ]

# REST framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # You can optionally add:
        # 'rest_framework.authentication.TokenAuthentication',
    ],
}

# URL config
ROOT_URLCONF = 'tolake.urls'

# Templates config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'tolake.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # Only needed if you have app-level static
STATIC_ROOT = BASE_DIR / "staticfiles"   # Used in collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Templates directory
TEMPLATES_DIR = BASE_DIR / 'templates'
# Ensure the templates directory exists
if not TEMPLATES_DIR.exists():
    os.makedirs(TEMPLATES_DIR)
# Ensure the static directory exists
if not (BASE_DIR / 'static').exists():
    os.makedirs(BASE_DIR / 'static')
# Ensure the media directory exists
if not MEDIA_ROOT.exists():
    os.makedirs(MEDIA_ROOT)
# Ensure the staticfiles directory exists
if not STATIC_ROOT.exists():
    os.makedirs(STATIC_ROOT)
# Ensure the templates directory exists
if not TEMPLATES_DIR.exists():
    os.makedirs(TEMPLATES_DIR)
# Static files storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# Media files storage
MEDIAFILES_STORAGE = 'django.core.files.storage.FileSystemStorage'
# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Default session engine
# CSRF settings
CSRF_COOKIE_SECURE = True  # Use secure cookies for CSRF in production
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
CSRF_TRUSTED_ORIGINS = [
    "https://tolake.in",
    "https://www.tolake.in",
]
# Security settings
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent content type sniffing
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
SECURE_HSTS_SECONDS = 3600  # Enable HTTP Strict Transport Security for 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Preload HSTS in browsers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'  # Referrer policy
# Session settings
SESSION_COOKIE_SECURE = True  # Use secure cookies for sessions in production
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Email settings for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
ADMIN_EMAIL = 'admin@tolake.in'
# ---------------- JS MIME Fix ---------------- #
mimetypes.add_type("application/javascript", ".js", True)
