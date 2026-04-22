from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 SECURITY
SECRET_KEY = 'django-insecure-g6@wi6^1w=giq28qz#eld@mf@uvfruxxkg%#f5_e6)@m)2!tpz'

DEBUG = True
ALLOWED_HOSTS = []


# 📦 APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.admissions',
    'apps.attendance',
    'apps.accounts',
]


# ⚙️ MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 🔗 URL CONFIG
ROOT_URLCONF = 'csc_crm.urls'


# 🎨 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# 🚀 WSGI
WSGI_APPLICATION = 'csc_crm.wsgi.application'


# 🗄️ DATABASE (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'csc_crm_db',
        'USER': 'root',
        'PASSWORD': 'Gopika@0808',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# 🔐 PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 🌍 LANGUAGE & TIME
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# 📁 STATIC
STATIC_URL = 'static/'


# 🔑 DEFAULT PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================================
# 📧 EMAIL CONFIG (FINAL WORKING)
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'gopikas04082005@gmail.com'

# 🔥 IMPORTANT: Replace with your Gmail App Password
EMAIL_HOST_PASSWORD = 'ixqmfouunkhegpbq'