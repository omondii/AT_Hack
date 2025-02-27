#!/usr/bin/env python3
"""
Application configuration class
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    AT_API = os.getenv('ATAPI_KEY')

    