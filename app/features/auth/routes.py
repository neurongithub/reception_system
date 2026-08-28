from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.features.auth.services import AuthService
from app.features.common.utils import render_with_time

#auth blueprint 
auth_bp = Blueprint('auth', __name__)

#===============================================================
# 1. route => root (redirect user to login)
#===============================================================
@auth_bp.route('/')
def root():
    return redirect(url_for('setup.setup'))

#===============================================================
# 2. route => login (return login page & login buissness logic)
#===============================================================

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login_page():

    if request.method == 'POST':
        remember = bool(request.form.get('remember'))
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        try:
            user = AuthService.authenticate(username, password)
        except ValueError as exc:
            flash(str(exc), 'error')
            return redirect(url_for('auth.login_page'))

        session.permanent = remember
        session['user_id'] = user.id
        session['role'] = user.role

        return redirect(url_for('dashboard.dashboard') if user.role == 'admin' or user.role=='operator' else url_for('result_page.result'))

    return render_with_time('login.html')

#===============================================================
# 3. route => change password (open modal & chage password)
#===============================================================

@auth_bp.route('/changepassword/', methods=['POST'])
def change_pass():
    username = request.form.get('username', '').strip()
    old_pass = request.form.get('old-password', '').strip()
    new_pass = request.form.get('new-password', '').strip()
    confirm_pass = request.form.get('again-password', '').strip()

    try:
        AuthService.change_password(username, old_pass, new_pass, confirm_pass)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('auth.login_page'))

    flash('رمز عبور با موفقیت بروزرسانی شد', 'success')
    return redirect(url_for('auth.login_page'))

#===============================================================
# 4. route => logout from account (clear user session)
#===============================================================

@auth_bp.route('/dashboard/logout/')
def logout():
    session.clear()# remove session 
    return redirect(url_for('auth.login_page'))
