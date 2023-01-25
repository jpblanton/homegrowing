"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import datetime

from environs import Env
from celery.schedules import crontab

import config.tasks

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    # 3rd party
    "crispy_forms",
    "crispy_bootstrap5",
    "rest_framework",
    "bootstrap5",
    # local
    "accounts.apps.AccountsConfig",
    "pages.apps.PagesConfig",
    "monitoring.apps.MonitoringConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "EST"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s %(name)-28s %(levelname)-8s %(message)s"}
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/code/logs/{:%Y-%m-%d}.log".format(datetime.now()),
            "formatter": "default",
        },
    },
    "root": {"handlers": ["file"], "level": "DEBUG"},
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # new
CRISPY_TEMPLATE_PACK = "bootstrap5"

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

CELERY_BEAT_SCHEDULE = {
    "humidity_rolling_avg": {
        "task": "monitoring.tasks.climate_monitoring",
        "schedule": crontab(minute="*/1"),
        "args": ("humidity",),
    },
    "temperature_rolling_avg": {
        "task": "monitoring.tasks.climate_monitoring",
        "schedule": crontab(minute="*/1"),
        "args": ("temperature",),
    },
}

# custom settings variables
# this below is what the switch signal goes on
# "tent1/humidifier/power"
# gotta figure out how to organize these better
# can't be repeating the same thing 3 times
MQTT_TOPIC_SUBS = [
    "tent1/DHT22-1/humidity",
    "tent1/DHT22-1/temperature",
    "tent1/DHT22-2/humidity",
    "tent1/DHT22-2/temperature",
    "tent1/humidifier/status",
    "tent1/humidifier/power",
    "tent1/AHT20-1/humidity",
    "tent1/AHT20-1/temperature",
    "tent1/fan1/status",
    "tent1/fan2/status",
    "tent1/fan1/power",
    "tent1/fan2/power",
    "tent1/light/status",
    "tent1/light/lux",
]

MQTT_TOPICS = {
    "tent1_DHT22-1_humidity": "tent1/DHT22-1/humidity",
    "tent1_DHT22-1_temperature": "tent1/DHT22-1/temperature",
    "tent1_DHT22-2_humidity": "tent1/DHT22-2/humidity",
    "tent1_DHT22-2_temperature": "tent1/DHT22-2/temperature",
    "tent1_humidifier_status": "tent1/humidifier/status",
    "tent1_humidifier_power": "tent1/humidifier/power",
    "tent1_AHT20-1_humidity": "tent1/AHT20-1/humidity",
    "tent1_AHT20-1_temperature": "tent1/AHT20-1/temperature",
    "tent1_fan1_status": "tent1/fan1/status",
    "tent1_fan2_status": "tent1/fan2/status",
    "tent1_fan1_power": "tent1/fan1/power",
    "tent1_fan2_power": "tent1/fan2/power",
    "tent1_light_status": "tent1/light/status",
    "tent1_light_lux": "tent1/light/lux",
}

MQTT_TOPICS_DICT = {
    "tent1": {
        "DHT22-1": {
            "humidity": "tent1/DHT22-1/humidity",
            "temperature": "tent1/DHT22-1/temperature",
        },
        "DHT22-2": {
            "humidity": "tent1/DHT22-2/humidity",
            "temperature": "tent1/DHT22-2/temperature",
        },
        "humidifier": {
            "status": "tent1/humidifier/status",
            "power": "tent1/humidifier/power",
        },
        "AHT20-1": {
            "humidity": "tent1/AHT20-1/humidity",
            "temperature": "tent1/AHT20-1/temperature",
        },
        "light": {
            "lux": "tent1/light/lux",
            "status": "tent1/light/status",
        },
        "fan1": {
            "status": "tent1/fan1/status",
            "power": "tent1/fan1/power",
        },
        "fan2": {
            "status": "tent1/fan2/status",
            "power": "tent1/fan2/power",
        },
    }
}


HUMIDIFIER_DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/991805750894678166/tdCOKUCjqY-dYqGDOGfNPJ7k6xPdd01W6zdzPdnZAcplC1YUa-pcZd0FgxdpkpQA9qJB"
TEMPERATURE_DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/991807283870826596/S9oTsSjKwYrweS6OkHecgEudIOZqb4vswTbZG4dR_oHAiaucDSYBiD-55WK-VPuRhq3D"
HUMIDITY_DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/991807385469452328/-7qdVvapWdxOu8I9MNGxSqgJr9UVnvVW302PQQfZ5aE8vmWXJBbMBnhvTtfPjHeyD4fw"
