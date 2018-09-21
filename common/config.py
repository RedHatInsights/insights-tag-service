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
