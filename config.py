# main configuration application file 

import os
from pathlib import Path
from datetime import datetime , timedelta


class Config :

        # root [directory] application 
        BASE_DIR =Path(__file__).resolve().parent
        
        #=========== database configs  = ================
        #set database path to root directory 
        SQLALCHEMY_DATABASE_URI  ="sqlite:///database.db"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        #=========session configs ==========
        PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
        SESSION_COOKIE_NAME = "login_session"
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        SESSION_TYPE = "filesystem"
        SESSION_FILE_DIR = BASE_DIR / "flask_session"
        SESSION_USE_SIGNER = True
        SESSION_PERMANENT = True
        SESSION_REFRESH_EACH_REQUEST = True
        #when using real domain
        # SESSION_COOKIE_DOMAIN = ".example.com"
        #====================================
        
        # ================ excel file upload configs==================
        UPLOAD_FOLDER= BASE_DIR / "app/uploads"
        #================= json folder path config ==================
        JSON_FOLDER = BASE_DIR / "json_folder"
       
        #secret key configuration
        SECRET_KEY = 'this#testign_secret$key' 
        #run.py configs
        DEBUG = True 
        HOST = 'localhost'
        