import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MAX_CONTENT_LENGTH = 1 * 1024 * 1024 * 1024  # 1GB
PCAP_FILE_PATH = os.path.join(PROJECT_ROOT, 'pcap_files')

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://localhost'
CELERY_BACKEND = 'amqp://'
