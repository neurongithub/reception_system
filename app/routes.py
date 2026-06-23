#All routes & views &blue prints
from flask import Blueprint,render_template

#main Blueprint
main_bp = Blueprint('main', __name__)

#login route - http://host.com/login/
@main_bp.route('/login/')

def login_page () : 
    
    return render_template('login.html')


#@main_bp.route("view")
#other routes b