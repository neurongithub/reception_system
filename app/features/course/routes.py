from flask import Blueprint, flash, redirect, request, url_for

from app.features.common.utils import render_with_time, require_admin, require_login
from app.features.course.services import CourseService

# create blueprint for course routes 
course_bp = Blueprint('course', __name__, url_prefix='/dashboard') 

#==========================================================
# 1. route => create course (return create_course web page)
#==========================================================
@course_bp.route('/create_course/')
def create_course():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()
    return render_with_time('create_coures.html', result=None)

#==========================================================
# route => upload (holde excel and json services )
#==========================================================
@course_bp.route('/upload/', methods=['POST'])
def upload():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    try:
        json_final = CourseService.process_course_upload(request)
        flash('دوره با موفقیت ایجاد شد', 'success')
        return json_final
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('course.create_course'))
    