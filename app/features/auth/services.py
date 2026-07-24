from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User


class AuthService:

    @staticmethod
    def authenticate(username, password):
        if not username:
            raise ValueError('نام کاربری وارد نشده است.')

        if not password:
            raise ValueError('رمز عبور وارد نشده است.')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hashed, password):
            raise ValueError('نام کاربری یا رمز عبور اشتباه است.')

        return user

    @staticmethod
    def change_password(username, old_password, new_password, confirm_password):
        if not username or not old_password or not new_password or not confirm_password:
            raise ValueError('برای تغییر رمز عبور همه مقادیر را وارد کنید.')

        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError('نام کاربری یافت نشد.')

        if not check_password_hash(user.password_hashed, old_password):
            raise ValueError('رمز عبور فعلی صحیح نمی باشد.')

        if new_password != confirm_password:
            raise ValueError('رمز جدید و تکرار آن یکسان نیست.')

        if check_password_hash(user.password_hashed, new_password):
            raise ValueError('رمز جدید نباید با رمز قبلی یکسان باشد.')

        if len(new_password) < 4:
            raise ValueError('طول رمز جدید نباید از 4 کاراکتر کمتر باشد.')

        user.password_hashed = generate_password_hash(new_password)
        db.session.commit()
