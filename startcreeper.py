import threading
from Queue import Queue

from creeper.creeper import Creeper
from creeper.exceptions import NoXPathException

import paste.deploy
from notifox.config.environment import load_environment
from notifox.model.meta import Session, Base
from notifox.model.page import Page
from notifox.model.user import User

MAX_THREADS = 5

if __name__ == "__main__":
    load_environment({}, paste.deploy.appconfig('config:development.ini', relative_to='.'))
    q = Queue()
    while True:
        pages = Session.query(Page).all()
        for page in pages:
            # Only allow MAX_THREADS number of creepers creepin' at a time.
            while threading.active_count() > MAX_THREADS:
                pass
            creeper = Creeper(page)
            creeper.start()
        Session.commit()
