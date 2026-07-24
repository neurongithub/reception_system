from flask import Blueprint

from app.features.common.utils import render_with_time, require_admin, require_login

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard/')
def dashboard():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()
    return render_with_time('dashboard.html')


@dashboard_bp.route('/help/')
def help():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    return render_with_time('help.html')


@dashboard_bp.route('/last_courses/')
def last_courses():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()
    return render_with_time('last_courses.html')


@dashboard_bp.route('/view/')
def view():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    return render_with_time('view.html')
