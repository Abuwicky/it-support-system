import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "your-super-secret-key-change-this-in-production"  # Change this!

DEBUG = True

ALLOWED_HOSTS = []

# ==================== INSTALLED APPS ====================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",  # Django REST Framework (for APIs)
    "channels",  # Real-time features (WebSockets)
    "rest_framework_simplejwt",  # JWT Authentication for Next.js frontend
    "corsheaders",  # CORS headers for Next.js frontend
    # Our app
    "tickets",  # Our IT Support app
]

# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Must be before CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "itsupport.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "itsupport.wsgi.application"
ASGI_APPLICATION = "itsupport.asgi.application"  # Important for Channels (WebSockets)

# ==================== DATABASE ====================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Use PostgreSQL in production
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==================== AUTHENTICATION ====================
AUTH_USER_MODEL = "tickets.CustomUser"  # We will use our own User model

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# ==================== CHANNELS (Real-time) ====================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  # Make sure Redis is running
        },
    },
}

# ==================== STATIC & MEDIA ====================
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ==================== FILE UPLOAD SETTINGS ====================
# Allow larger files (screenshots can be up to 10MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ==================== CELERY SETTINGS ====================
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Nairobi"  # Change if your timezone is different

# Optional: Email backend (use Gmail or your company SMTP in production)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Example - change later
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"  # ← Change
EMAIL_HOST_PASSWORD = "your-app-password"  # ← Change
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# In production you will change this to S3/Cloudinary

# For development only
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ==================== CORS (Cross-Origin Resource Sharing) ====================
# Allow the Next.js dev server and production frontend to call the API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
