import os
import random
import string


def randomkey(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024  # 1GB
PCAP_FILE_PATH = os.path.join(PROJECT_ROOT, 'pcap_files')

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://localhost'
CELERY_BACKEND = 'amqp://'

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'testdb.db')
SECRET_KEY = 'development-key'
