from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, DateTime

from notifox.model.meta import Base

class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    name = Column(Text()) # Label for convenience
    url = Column(Text()) # Longer than anyone needs ever.
    xpath = Column(String(512)) # XPath
    content = Column(Text())
    date_added = Column(DateTime())
    last_crawled = Column(DateTime())
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name, url, xpath, user_id):
        self.name = name
        self.url = url
        self.xpath = xpath
        self.user_id = user_id
        self.content = ''
        self.date_added = datetime.utcnow()
        self.last_crawled = datetime.utcnow()

    def __repr__(self):
        return "<Page(%s)>" % self.id
