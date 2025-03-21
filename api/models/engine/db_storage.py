#!/usr/bin/env python3
"""
DB storage handles the creation of the application db,
a connection to execute defined methods on db data
"""
from models.tables import Rider, Contact, Base
from sqlalchemy import create_engine
import os
from pathlib import Path
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
print(os.getenv('DATABASE_URL'))

# if No DB URL is provided, the system defaults to an sqllite DB
if not DATABASE_URL:
    db_path = Path('app.db').absolute()
    DATABASE_URL = f"sqlite:///{db_path}"

classes = {
    "Rider": Rider,
    "Contact": Contact
}

class DBStorage:
    """
    Creates a connection to me a postgres db
    class methods: all, reload, new, delete, get, cloes
    """
    __session = None
    __engine = None

    def __init__(self, db_engine=None):
        """
        Class initiator. Create a connection to the db for every instance
        """
        if db_engine:
            self.__engine = db_engine
            self.__session = scoped_session(sessionmaker(bind=self.__engine))
        else:
            self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def new(self, obj):
        """
        Add a new object to the db session
        :return:
        """
        self.__session.add(obj)

    def save(self):
        """
        Save current session changes to db
        :return:
        """
        self.__session.commit()

    def reload(self):
        """
        Create and manage db sessions
        :return: a session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session

    def all(self, cls=None):
        """
        Class method to retrieve all items in the db based on class name
        :param cls: classname == A db table
        :return: dict of all class items in db
        """
        new_dict = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = self.__session.query(Rider).all() + self.__session.query(Contact).all()

        for obj in objects:
            if isinstance(obj, Rider):
                key = f"User.{obj.riderId}"
            elif isinstance(obj, Contact):
                key = f"Contact.{obj.orgId}"
            else:
                continue  # Skip if it's neither rider nor Contact
            new_dict[key] = obj

        return new_dict

    def delete(self, obj=None):
        """
        Delete an obj instance from db
        :param obj: object to delete
        :return:
        """
        if obj is not None:
            self.__session.delete(obj)

    def rollback(self):
        """
        Reverts changes made i the current session to the last commited state
        :return:
        """
        self.__session.rollback()

    def close(self):
        """
        Close the current session by removing the private attribute __session
        :return:
        """
        self.__session.remove()

    def get(self, cls, id):
        """ Returns the object based on the class name and its ID """
        try:
            if isinstance(cls, str):
                cls_name = cls
            else:
                cls_name = cls.__name__

            if cls_name == 'Rider':
                return self.__session.query(Rider).filter(Rider.riderId == id).one()
            elif cls_name == 'Contact':
                return self.__session.query(Contact).filter(Contact.orgId == id).one()
            else:
                return None
        except NoResultFound:
            return None

    def get_by_email(self, cls, email):
        """Returns the object based on the class and email"""
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.email == email:
                return value
        return None

    def get_by_orgname(self, cls, org_name):
        """ Returns the object based on the organisation name """
        if cls not in classes.values():
            return None

        all_objs = self.all(cls).values()
        for obj in all_objs:
            if getattr(obj, 'name', None) == org_name:
                return obj
        return None

    def to_dict(self, save_fs=None):
        """ Return a dict of the current class instance
        """
        new_dict = self.__dict__.copy()
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict