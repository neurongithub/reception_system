from flask import Blueprint , flash ,redirect , url_for , request , render_template , abort ,session

from app.features.common.utils import render_with_time , require_admin , require_login
# import user management service 
from app.features.user_management.services import UserManageService
#import validator modul
from app.features.user_management.validator import NewUserValidate

#user management blueprint
user_manage_bp = Blueprint("user_management" ,__name__,url_prefix="/dashboard")

#==============================================================
#user management main route 
#==============================================================
@user_manage_bp.route('/user_management/' , methods=['GET'])
def user_manage():
    
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin() 

   

    # query to get all users in database  
    all_users =  UserManageService.show_all_users()

    current_user = UserManageService.get_current_user()

    #create user authorization check (frontend side)
    ALLOWED_ROLE_CREATION ={
        "admin":["operator" , "viewer"],
        "operator" : ["viewer"]}

    current_role = session["role"] #curren user's role from session
    allowed_roles = ALLOWED_ROLE_CREATION[current_role]
    


    return render_with_time('user_management.html',all_users=all_users,allowed_roles=allowed_roles,current_user=current_user) 
#==============================================================
#Create new user route 
#==============================================================
@user_manage_bp.route('/create_user/' , methods=["POST"])
def create_new_user ():

    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin() 

    ALLOWED_ROLE_CREATION ={
        "admin":["operator" , "viewer"],
        "operator" : ["viewer"]}
    
    
    #get inputs from modal form 
    username = request.form.get('username' ,'').strip()
    full_name = request.form.get('full_name','').strip()
    password = request.form.get('password','').strip()
    confirm_password = request.form.get('confirm_password','').strip()
    role = request.form.get('role')

     
    #runnig validate inputs 
    try:
        NewUserValidate.user_validate(username, full_name, password, confirm_password,role)
    except ValueError as ex : 
        flash (str(ex) ,"error")
        return render_with_time("user_management.html")

    #create user authorization check (backend side)
    current_role = session["role"]

    allowed_roles = ALLOWED_ROLE_CREATION[current_role]

    if role not in allowed_roles:
        flash("شما دسترسی لازم برای این عملیات را ندارید.")
        abort(403)
    
    #runnig create new user servic  e 
    user = UserManageService.create_new_user(password ,username,full_name,role)
    flash("کاربر جدید با موفقیت ایجاد شد" , "success")

    return redirect(url_for('user_management.user_manage'))


#==============================================================
# remove users route 
#==============================================================
@user_manage_bp.route("/delete_user/<int:user_id>/" , methods=['GET','POST'])
def delete_user (user_id):

    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    UserManageService.delete_user(user_id)

    

    return redirect(url_for('user_management.user_manage'))





    



