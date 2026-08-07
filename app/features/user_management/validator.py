import re
from app import db
from app.models import User

class NewUserValidate: 

    @staticmethod
    def user_validate (username, full_name, password, confirm_password,role):

        if not username or not full_name or not password or not confirm_password:
            raise ValueError("همه مقادیر را وارد کنید.")

        #user name English and numbers only regex 
        pattern = r"^[a-zA-Z0-9_]+$"
        if not re.fullmatch(pattern,username): 
            raise ValueError("نام کاربری فقط شامل حروف انگلیسی و عدد باشد - بدون فاصله")

        if len(username) > 30 : 
            raise ValueError("نام کاربری بیش از حد طولانی است")
        if len(username) < 4 : 
            raise ValueError("نام کاربری نباید از 4 کاراکتر کمتر باشد.")
        
        #search query to check user is exsist or not 
        current_user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        if current_user : 
            raise ValueError("این نام کاربری قبلا استفاده شده است")

        if len(password) < 4 :
            raise ValueError("رمز عبور باید حداقل ۴ کاراکتر باشد")
        if " " in password :
            raise ValueError("رمز عبور نمی تواند شامل فاصله باشد")
        
        if password != confirm_password : 
            raise ValueError ("رمز عبور با تکرار آن یکسان نیست")

    
    







        
        
    