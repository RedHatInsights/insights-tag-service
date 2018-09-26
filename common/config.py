from types import SimpleNamespace
import os

DATABASE = SimpleNamespace(
    NAME=os.environ.get('DB_NAME', 'tagservice'),
    USER=os.environ.get('DB_USER', 'tagservice'),
    PASSWORD=os.environ.get('DB_PASSWORD', 'tagservice'),
    HOST=os.environ.get('DB_HOST', 'localhost'),
    PORT=os.environ.get('DB_PORT', '5746'),
)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
PORT = os.environ.get('PORT', 8080)
DEBUG = os.environ.get('DEBUG', True)
DB_POOL_SIZE = os.environ.get('DB_POOL_SIZE', 30)
DB_MAX_OVERFLOW = os.environ.get('DB_MAX_OVERFLOW', 100)
