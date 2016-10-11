from . import celery
from .config import *
from .models import *


@celery.task
def save_pcap(filename, pcap):
    p = Pcap(filename, pcap.filename)
    db.session.add(p)

    pcap.save(os.path.join(PCAP_FILE_PATH, filename))

    db.session.commit()

    return True
