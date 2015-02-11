from celery.signals import setup_logging
from ptero_common.logging_configuration import configure_celery_logging
import celery
import os


TASK_PATH = 'ptero_shell_command.implementation.celery_tasks'


app = celery.Celery('PTero-shell-command-celery', include=TASK_PATH)


app.conf['CELERY_ROUTES'] = (
    {
        TASK_PATH + '.shell_command.ShellCommandTask': {'queue': 'fork'},
        'ptero_common.celery.http.HTTP': {'queue': 'http'},
    },
)


_DEFAULT_CELERY_CONFIG = {
    'CELERY_BROKER_URL': 'amqp://localhost',
    'CELERY_RESULT_BACKEND': 'redis://localhost',
    'CELERY_ACCEPT_CONTENT': ['json'],
    'CELERY_ACKS_LATE': True,
    'CELERY_RESULT_SERIALIZER': 'json',
    'CELERY_TASK_SERIALIZER': 'json',
    'CELERY_TRACK_STARTED': True,
    'CELERYD_PREFETCH_MULTIPLIER': 10,
}
for var, default in _DEFAULT_CELERY_CONFIG.iteritems():
    if var in os.environ:
        app.conf[var] = os.environ[var]
    else:
        app.conf[var] = default


@setup_logging.connect
def setup_celery_logging(**kwargs):
    configure_celery_logging('SHELL_COMMAND')
