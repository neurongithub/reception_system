from werkzeug.security import generate_password_hash 
from flask import session ,flash ,redirect,url_for
from app import db
from app.models import User

class UserManageService : 

    #service 1 - show all users in database 
    @staticmethod
    def show_all_users (sort="desc",role='all', search_username=""): 
        

        query = db.select(User)

        if search_username : 
            query = query.filter(User.username.contains(search_username))
        # Role Filter
        if role != "all":
            query = query.where(User.role == role)

        # Sort
        if sort == "asc":
            query = query.order_by(User.create_at.asc())
        else:
            query = query.order_by(User.create_at.desc())



        all_users = db.session.execute(query).scalars().all()

        return all_users

    
    @staticmethod
    def search_one_username (search_username): 
        searched_user = User.query.filter_by(username=search_username).first()

        

        return searched_user





    #service 2 - create new user 
    @staticmethod
    def create_new_user (password , username , full_name, role): 

        #hasing password & create new user
        hashed_password = generate_password_hash(password) 
        
        user = User (username=username,
                    full_name=full_name,
                    password_hashed=hashed_password,
                    role=role)

        db.session.add(user)
        db.session.commit()


    #service 3 -delete users base on autorization 
    @staticmethod 
    def delete_user(user_id):

        #find user in table 
        user = User.query.get_or_404(user_id)

        current_role = session["role"]

        if current_role == "admin":
            pass

        if current_role == "operator":

            if user.role != "viewer":
                abort(403)

        if user.id == session["user_id"]:
            flash("نمی‌توانید حساب کاربری خودتان را حذف کنید.", "error")
            return redirect(url_for("user_management.user_manage"))

        db.session.delete(user)
        db.session.commit()
        flash(f"کاربر {user.username} با موفیت حذف گردید!",'warning')

    #service 4 - get logged user information from db and return to user_management web page 
    @staticmethod
    def get_current_user ():

        user_id = session.get("user_id")

        if not user_id: 
            return None 

        return User.query.get(user_id)

        
