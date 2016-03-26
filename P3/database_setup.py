from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


# Class representing table usr
class User(Base):
    __tablename__='usr'
    id = Column(Integer, primary_key=True)
    access_token = Column(String, nullable=False)

    def __init__(self, access_token):
        self.access_token = access_token


# Class representing table category
class Category(Base):
    __tablename__='category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


    @property
    def serialize(self):
        """
        Returns: Serialized data for JSON method

        """
        return {
            'id': self.id,
            'name': self.name
        }


# Class representing table item
class Item(Base):
    __tablename__='item'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, backref="item")
    usr_id = Column(Integer, ForeignKey('usr.id'))
    usr = relationship(User, backref="item")

    @property
    def serialize(self):
        """
        Returns: Serialized data for JSON method

        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }
