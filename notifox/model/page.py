from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, DateTime

from notifox.model.meta import Base

class Page(Base):
	__tablename__ = "page"

	id = Column(Integer, primary_key=True)
	name = Column(Text()) # Label for convenience
	url = Column(Text()) # Longer than anyone needs ever.
	xpath = Column(String(512)) # XPath
	date_added = Column(DateTime())
	last_crawled = Column(DateTime())
	user_id = Column(Integer, ForeignKey('user.id'))
