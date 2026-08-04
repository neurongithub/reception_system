
from app import db
from app.models import User

class NewUserValidate: 

    @staticmethod
    def user_validate (username, full_name, password, confirm_password,role):

        if not username or not full_name or not password or not confirm_password:
            raise ValueError("همه مقادیر را وارد کنید.")
        
        #search query to check user is exsist or not 
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        if user : 
            raise ValueError("این نام کاربری قبلا استفاده شده است")

        if len(password) < 4 :
            raise ValueError("رمز عبور باید حداقل ۴ کاراکتر باشد")
        
        if password != confirm_password : 
            raise ValueError ("رمز عبور با تکرار آن یکسان نیست")

       

        
        
    