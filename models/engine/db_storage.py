#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
import os
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class manages storage of hbnb models in mysql format"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new model"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, pwd, host, db), pool_pre_ping=True
            )
        if env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of objects from db"""
        __type_object = [User, State, City, Amenity, Place, Review]
        dict = {}
        if cls is None:
            for obj in __type_object:
                results = self.__session.query(obj).all()
                for result in results:
                    key = '{}.{}'.format(obj, result.id)
                    dict[key] = result
        elif cls in __type_object:
            results = self.__session.query(cls).all()
            for result in results:
                key = '{}.{}'.format(cls, result.id)
                dict[key] = result
        return dict

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """Method to delete an object from the current database"""
        self.__session.delete(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def reload(self):
        """Method to create the current database session"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Closes the session"""
        self.__session.close()
