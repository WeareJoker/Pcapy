from . import celery
from .config import *


@celery.task
def save_pcap(filename, pcap):

    pcap.save(os.path.join(PCAP_FILE_PATH, filename))

    return "Done"
