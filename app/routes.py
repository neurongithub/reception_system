#All routes & views &blue prints
from flask import Blueprint,render_template , request , redirect , url_for , session ,abort , flash
from app.models import User
from werkzeug.security import check_password_hash

#main Blueprint
main_bp = Blueprint('main', __name__)

#login route - http://host.com/login/
@main_bp.route('/login/' , methods = ["GET" ,"POST"])
def login_page () : 
    
    if request.method == "POST" : 
        
        #saving value of username & password 
        username = request.form.get("username")
        password = request.form.get("password")
        
        #search query on username 
        user = User.query.filter_by(username=username).first()
        
        if not user : 
            flash("خطا:‌ نام کاربری یا رمزعبور اشتباه وارد شده است", "error")
            return redirect(url_for("main.login_page"))
            
       
        #cheeck on username & password 
        if user and check_password_hash(user.password_hashed , password): 
            if user.role =="admin" : 
                
                #Set session 
                session.permanent = True # session expire time 
                session['user_id']  = user.id 
                session ['role'] = user.role
                
                
                #if is admin return darboard page
                return redirect(url_for('main.dashboard'))
                
            
            elif user.role=="viewer" : 
                session["user_id"] = user.id
                session["role"] = user.role

                print("SESSION AFTER LOGIN:", dict(session))

                return redirect(url_for("main.view"))
               
               #if invalid user return Error  with alert box 
            else :
                return "<h1></h1>"
        
            
    
    
    return render_template('login.html')


# view route (commen users see this )
@main_bp.route("/view/")
def view():

    print("SESSION IN VIEW:", dict(session))

    if "user_id" not in session:
        return redirect(url_for("main.login_page"))

    return render_template("view.html")
    

#Dashboard route (retun to admin only )
@main_bp.route("/dashboard/")
def dashboard () : 
    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    
    if session.get("role") != "admin":
        abort(403)
    
    return render_template("dashboard.html")


#create course rooute  ==> open create course page
@main_bp.route('/dashboard/create_course/')
def create_course ()  :
    
    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    if session.get("role")!="admin" : 
        abort(403)
    
    return render_template('create_coures.html')

#reception route ==> open reception page 
@main_bp.route('/dashboard/reception//')
def reception () : 
    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    if session.get("role")!="admin" : 
        abort(403)
    
    return render_template('reception.html')

#last courses ==> open last courses page [back log now]
@main_bp.route('/dashboard/last_courses/')
def last_courses () : 
    
    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    if session.get("role")!="admin" : 
        abort(403)
    
    return render_template('last_courses.html')

#logout button endpoint 
@main_bp.route("/dashboard/logout/") 
def logout () :
    
    session.pop('user_id',None)
    session.clear()
    return redirect(url_for("main.login_page"))


