from . import celery
from .config import *
from .models import *


@celery.task
def save_pcap(filename, pcap):
    p = Pcap(filename, pcap.filename, pcap.size)
    db.session.add(p)
    db.session.commit()

    pcap.save(os.path.join(PCAP_FILE_PATH, filename))

    return True
