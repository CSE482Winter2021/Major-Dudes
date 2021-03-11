import os
import urllib

PROTOCOL = 'mongodb'
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 27017))
if 'DB_USER' in os.environ and 'DB_PASS' in os.environ:
    DB_USER = urllib.parse.quote_plus(os.environ['DB_USER'])
    DB_PASS = urllib.parse.quote_plus(os.environ['DB_PASS'])
else:
    DB_USER = None
    DB_PASS = None

_ENV = 'dev'
DB_NAME = f'majordudes-{_ENV}'

COL_NAME = f'majordudes-col-{_ENV}'
