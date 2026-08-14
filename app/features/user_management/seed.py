# seed.py -> is a service to  Initial Setup Wizard page , seed initial Administrator 

from app import db
from flask import redirect , url_for ,flash
from werkzeug.security import generate_password_hash
from app.models import User

class SeedService :


    @staticmethod
    def admin_exists() -> bool:

        admin = User.query.filter_by(role="admin").first()
        return admin is not None



    @staticmethod
    def create_admin (username: str,full_name:str,password: str, confirm_password:str) -> None: 

        #validation inputs 
        if not username or not full_name or not password or not confirm_password: 
            raise ValueError ("همه مقادیر را وارد کنید. ")
            
        if len(username) < 4 or len(username) > 30 : 
            raise ValueError("طول نام کاربری مجاز نمیباشد (حداقل ۴ و حداکثر ۳۰ )کاراکتر مجاز است")
            
        if len(password) < 4 : 
            raise ValueError ("طول رمز عبور نباید از ۴ کاراکتر کمتر باشد")
            
        if password != confirm_password : 
            raise ValueError("رمز عبور با تکرار آن مطابق نیست")
            
        # Prevent creating a second administrator
        if SeedService.admin_exists():
            raise ValueError("Administrator already exists.")
        
        if User.query.filter_by(username=username).first(): 
            raise ValueError (" نام کاربری قبلا انتخاب شده است - یک نام کاربری دیگر انتخاب کنید")

       
        
        admin = User(username=username,password_hashed=generate_password_hash(password),role="admin",full_name=full_name,created_by=None)
        db.session.add(admin)
        db.session.commit()
        flash ("کاربر ادمین ایجاد شد - لاگین کنید.")
        


         