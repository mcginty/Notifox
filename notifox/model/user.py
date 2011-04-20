from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import relation, backref

from notifox.model.meta import Base

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	password = Column(String(100))
	email = Column(String(100))
	pages = relation("Page", backref="user")

	def __init__(self, name, password, email):
		self.name = name
		self.password = password
		self.email = email

	def __repr__(self):
		return "<Person('%s')" % self.name
