import os
from types import SimpleNamespace


_REDIS = SimpleNamespace(
    **dict(
        HOST=os.environ.get('REDIS_HOST', '127.0.0.1'),
        PORT=os.environ.get('REDIS_PORT', '6379')
    )
)
_REDIS_URL = f'redis://{_REDIS.HOST}:{_REDIS.PORT}'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': _REDIS_URL,
    }
}

CELERY_BROKER_URL = _REDIS_URL
CELERY_RESULT_BACKEND = _REDIS_URL

CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

BROKER_CONNECTION_RETRY = True
