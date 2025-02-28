#!/usr/bin/env python3 
from .engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()