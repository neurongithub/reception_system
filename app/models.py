from app import db 
from datetime import datetime

#database modles (every modle is a class)


#model: users table 
class User(db.Model) :  
    __tablename__ = 'users'
    
    id = db.Column(db.Integer , primary_key=True ,  unique =True , nullable=False , autoincrement=True )
    username= db.Column(db.String(50) , unique=True , nullable=False, )
    password_hashed = db.Column(db.String(255) , nullable=False)
    role = db.Column(db.String(20), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    