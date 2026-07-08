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
    

#model:a model for courses table 
class Course (db.Model):
    __tablename__ = 'courses'

    id= db.Column(db.Integer,primary_key=True , unique=True, nullable=False , autoincrement=True)
    course_name = db.Column(db.String(100),nullable=False)
    course_code = db.Column(db.String(30), unique=True , nullable=False) 
    course_date = db.Column(db.Date,nullable=False)
    create_at = db.Column(db.DATETIME, erver_default=db.func.now())
    soldiers = db.relationship("Soldier" , backref="Course" , lazy=True ,  cascade="all, delete-orphan")
    



#model:model for soldier informations
# discreption:‌this tabel fill with data_frame (parsing result)
class Soldier(db.Model):
    __tablename__='soldiers'

    id = db.Column(db.Integer ,primary_key=True , unique=True , nullable=False , autoincrement=True )
    course_id = db.Column(db.Integer,db.ForeignKey('courses.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50))
    national_code = db.Column(db.String(10) , unique=True , nullable=False)
    birth_date = db.Column(db.Date)
    education = db.Column(db.String(50))
    health_status = db.Column(db.String(50))
    phone = db.Column(db.String(20))



