from multiprocessing import cpu_count
from os import environ

bind = '0.0.0.0:' + environ.get('PORT', '8003')
max_requests = 1000
timeout = 300
workers = (2 * cpu_count()) + 1
wsgi_app = 'wsgi:app'