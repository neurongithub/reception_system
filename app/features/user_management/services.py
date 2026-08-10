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

        # sort users count by role (Segmenting users by role)
        admin_count = sum(1 for user in all_users if user.role == "admin")
        operator_count = sum (1 for user in all_users if user.role =="operator")
        viewer_count = sum(1 for user in all_users if user.role == "viewer")

        users_count = {"admin":admin_count, "operator":operator_count,"viewer":viewer_count, "total":len(all_users)}


        return all_users , users_count

    
    @staticmethod
    def search_one_username (search_username): 
        searched_user = User.query.filter_by(username=search_username).first()

        

        return searched_user





    #service 2 - create new user 
    @staticmethod
    def create_new_user (password , username , full_name, role, created_by): 

        #hasing password & create new user
        hashed_password = generate_password_hash(password) 
        
        user = User (username=username,
                    full_name=full_name,
                    password_hashed=hashed_password,
                    role=role,
                    created_by=created_by)

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



    @staticmethod
    def edit_user (validated_data):

        user = User.query.get(validated_data["user_id"])

        if not user : 
            raise ValueError("User Not found")

        existing_user = User.query.filter(User.username == validated_data["username"],User.id != user.id).first()
        if existing_user : 
            raise ValueError("این نام کاربری قبلا استفاده شده است")
        
        
        current_role = user.role
        new_role = validated_data["role"]

        if current_role == "admin" and new_role != "admin":
            raise ValueError("امکان تغییر سطح دسترسی مدیر سامانه وجود ندارد.")

        if current_role != "admin" and new_role == "admin":
            raise ValueError("امکان انتخاب نقش مدیر سامانه وجود ندارد.")

        #update basic informatinos 
        user.username = validated_data["username"]
        user.full_name = validated_data["full_name"]
        user.role = validated_data["role"]

        # update password if user want to change it 

        if validated_data["password"]: 
            user.password_hashed = generate_password_hash(validated_data["password"])

        db.session.commit()
        

        
