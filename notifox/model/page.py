from sqlalchemy import Column
from sqlalchemy.types import Integer, String

from notifox.model.meta import Base

class Page(Base):
	__tablename__ = "page"

	id = Column(Integer, primary_key=True)
	name = Column(String(256)) # Label for convenience
	url = Column(String(65536)) # Longer than anyone needs ever.

