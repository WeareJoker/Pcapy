from . import celery
from .config import *
from .models import *
from pcapy import open_offline


@celery.task(bind=True)
def db_test(self):
    self.update_state(state='START')
    import time
    time.sleep(3)
    self.update_state(state='Finish')
    print(self)
    print(Pcap.query.all())
    return True
