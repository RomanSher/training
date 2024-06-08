import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'NAME': os.environ.get('DB_NAME', 'marketplace_dev'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '12wqasxz'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
}
