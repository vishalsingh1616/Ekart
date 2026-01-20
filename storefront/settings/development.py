from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4=o9@xap(mx67=nev%v-n2_ggj=sla0wv6!glu(_3u$g0rx+e7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'USER': 'root',
        'PASSWORD': 'vs1234VS@',
        'HOST': 'localhost',
        'PORT': '3306',
        
        },
    }