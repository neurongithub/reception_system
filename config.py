# application main settings  file

import os
from pathlib import Path
from datetime import datetime , timedelta

# BASE_DIR = Path(__file__).resolve().parent
class Config :
        #=========== database configs  = ================
        #set database path to root directory 
        SQLALCHEMY_DATABASE_URI  ="sqlite:///database.db"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        #=========session configs ==========
        PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
        SESSION_COOKIE_NAME = "login_session"
        SESSION_COOKIE_SECURE = True
        #when using real domain
        # SESSION_COOKIE_DOMAIN = ".example.com"
        #=================================
        

    
    
    
        SECRET_KEY = 'this#testign_secret$key' 
        #run.py configs
        DEBUG = True 
        HOST = 'localhost'
