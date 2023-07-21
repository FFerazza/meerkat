from multiprocessing import cpu_count
from os import environ

bind = '0.0.0.0:' + environ.get('PORT', '8003')
max_requests = 1000
timeout = 600
threads = 4
workers = (2 * cpu_count()) + 1
wsgi_app = 'wsgi:app'
worker_class = 'sync'
loglevel = 'debug'
accesslog = '/tmp/hydra_gunicorn.log'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  '/tmp/hydra_gunicorn_error.log'