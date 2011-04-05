"""The application's model objects"""
from notifox.model.meta import Session, Base

from notifox.model.user import User
from notifox.model.page import Page

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
