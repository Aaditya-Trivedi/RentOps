from django.conf import settings
from django.db import connections
from django.core.management import call_command


def create_shop_database_and_tables(db_name):
    # 1. Create database
    with connections['default'].cursor() as cursor:
        cursor.execute(
            f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

    # 2. Add DB dynamically
    settings.DATABASES[db_name] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': settings.DATABASES['default']['USER'],
        'PASSWORD': settings.DATABASES['default']['PASSWORD'],
        'HOST': 'localhost',
        'PORT': '3306',
    }

    # 3. Run migrations for shops apps
    call_command('migrate', database=db_name, run_syncdb=True)
