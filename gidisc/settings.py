"""
Django settings for gidisc project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import json
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+yjq24c)_md$9i8123-9$l%gx&urcaitt-w6qfa=h#f*gouy5&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'main_prj',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gidisc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'gidisc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

import os
import sys

# Lấy đường dẫn của thư mục `common_web`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lùi lên một cấp để đến thư mục cha chứa `gidisc` và `secret_key`
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Đảm bảo Django tìm thấy `gidisc`
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Định nghĩa đường dẫn file Firebase JSON
SECRET_KEY_DIR = os.path.join(PARENT_DIR, "secret_key")
FIREBASE_CRED_PATH = os.path.join(SECRET_KEY_DIR, "gidisc_firebase.json")


# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CRED_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()


GEMINI_API_PATH = os.path.join(SECRET_KEY_DIR, "gemini_api.json")
try:
    with open(GEMINI_API_PATH, "r") as file:
        data = json.load(file)
        GEMINI_API_KEY = data.get("geminikey", None)  # Lấy API key
except FileNotFoundError:
    GEMINI_API_KEY = None
    print("⚠️ Lỗi: Không tìm thấy file gemini_api.json")
except json.JSONDecodeError:
    GEMINI_API_KEY = None
    print("⚠️ Lỗi: File gemini_api.json không đúng định dạng JSON")

# Kiểm tra nếu API key bị thiếu
if not GEMINI_API_KEY:
    raise ValueError("❌ API Key không hợp lệ hoặc chưa được cấu hình!")
# cred = credentials.Certificate(FIREBASE_CRED_PATH)
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
