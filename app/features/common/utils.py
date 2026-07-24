from datetime import datetime
import jdatetime
from flask import abort, redirect, render_template, session, url_for


#curren time & date of server 
def get_current_time_data():
    now = datetime.now()
    return now.strftime('%H:%M:%S'), jdatetime.date.fromgregorian(date=now.date()).strftime('%Y/%m/%d') #convert date to hegri calendaer


def render_with_time(template_name, **context):
    time, date = get_current_time_data()
    return render_template(template_name, time=time, date=date, **context)


def require_login():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    return None


def require_admin():
    if session.get('role') != 'admin':
        abort(403)
