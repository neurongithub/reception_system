from flask import Flask , session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from config import Config

try:
    from flask_session import Session
except ImportError:
    Session = None


db = SQLAlchemy() 
migrate = Migrate() 


#[Application factory] function
def create_app () : 
    app = Flask(__name__)
    
    
    app.config.from_object ('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)

    if Session is not None:
        Session(app)

    from app.features.auth.routes import auth_bp
    from app.features.dashboard.routes import dashboard_bp
    from app.features.course.routes import course_bp
    from app.features.reception.routes import reception_bp
    from app.features.user_management.routes import user_manage_bp , setup_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(reception_bp)
    app.register_blueprint(user_manage_bp)
    app.register_blueprint(setup_bp)

    from app import models

    
    
    # create DATABASE TABLES if don't exsist 
    with app.app_context():
        db.create_all()
    
        

    
    return app  

    

