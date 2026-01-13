from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError


def create_shop_database(db_name):
    with connections['default'].cursor() as cursor:
        cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4")

    settings.DATABASES[db_name] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': 'root',
        'PASSWORD': settings.DATABASES['default']['PASSWORD'],
        'HOST': 'localhost',
        'PORT': '3306',
    }
