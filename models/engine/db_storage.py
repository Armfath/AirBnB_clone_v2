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


class DBStorage:
    """This class manages storage of hbnb models in mysql format"""

    __engine = None
    __session = None

    def __init__(self):
        """Instatntiates a new model"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{pwd}@{host}/{name}", pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(bind=self.__engine)
        

    def all(self, cls=None):
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()


    def close(self):
        """close the session
        """
        self.__session.close()
