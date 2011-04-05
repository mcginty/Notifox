from sqlalchemy import Column
from sqlalchemy.types import Integer, String

from notifox.model.meta import Base

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	password = Column(String(100))
	email = Column(String(100))

	def __init__(self, name='', email=''):
		self.name = name
		self.email = email

	def __repr__(self):
		return "<Person('%s')" % self.name
