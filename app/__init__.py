from flask import Flask , session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


db = SQLAlchemy() 
migrate = Migrate() 


#Application factory (main function in project)
def create_app () : 
    app = Flask(__name__)
    

    app.config.from_object ('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db )

    
    from app.routes import main_bp
    app.register_blueprint(main_bp)   
    
    from app import models
    
    # create DATABASE TABLES if don't exsist 
    with app.app_context():
        db.create_all()
    
    
        
        
    
    
    return app 

    