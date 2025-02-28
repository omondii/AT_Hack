#!/usr/bin/env python3
"""
Application configuration class
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    api_key = os.getenv('ATAPI_KEY')
    username = os.getenv("AT_USERNAME")
    AT_SENDER_ID = os.getenv("AT_SENDER_ID")

    