# this is temprary file to create users in application untile I create user-managment feature 

from werkzeug.security import generate_password_hash

from app import create_app ,db
from app.models import User 


app = create_app()

with app.app_context():

    if User.query.filter_by(username="admin").first():
        print("Admin already is exsist in database")
        exit()


    admin = User(
        username = "admin", 
        password_hashed = generate_password_hash(password="admin"), 
        role = "admin", 
        full_name = "Administrator"


    ) 

    db.session.add(admin)
    db.session.commit()

    print("user create succsessfully!!")
