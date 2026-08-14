from flask import Blueprint , flash ,redirect , url_for , request , render_template , abort ,session
from app.features.common.utils import render_with_time , require_admin , require_login
from app.features.user_management.services import UserManageService
from app.features.user_management.validator import NewUserValidate ,EditUserValidate
from app.features.user_management.seed import SeedService

#==============================================================
# Blueprints
#==============================================================
user_manage_bp = Blueprint("user_management" ,__name__,url_prefix="/dashboard")
setup_bp = Blueprint('setup', __name__)
#===============================================================
#create user authorization check (frontend side)
ALLOWED_ROLE_CREATION ={"admin":["operator" , "viewer"],"operator" : ["viewer"]}

#==============================================================
# route => user management main route 
#==============================================================
@user_manage_bp.route('/user_management/' , methods=['GET'])
def user_manage():
    
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    sort = request.args.get("sort", "desc")
    role = request.args.get("role", "all")
    search_username = request.args.get("search-username", "").strip()

    

    # query to get all users in database  
    all_users, users_count = UserManageService.show_all_users(sort, role,search_username)

    current_user = UserManageService.get_current_user()

    current_role = session.get("role")
     #curren user's role from session
    allowed_roles = ALLOWED_ROLE_CREATION[current_role]
    

    return render_with_time('user_management.html',all_users=all_users,allowed_roles=allowed_roles,current_user=current_user ,users_count=users_count)




#==============================================================
# route => Create new user  
#==============================================================
@user_manage_bp.route('/create_user/' , methods=["POST"])
def create_new_user ():

    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin() 

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
        return redirect(url_for('user_management.user_manage'))

    #create user authorization check (backend side)
    current_role = session.get("role")

    allowed_roles = ALLOWED_ROLE_CREATION[current_role]

    if role not in allowed_roles:
        flash("شما دسترسی لازم برای این عملیات را ندارید.")
        abort(403)
    current_user_id = session['user_id']
    #runnig create new user servic  e 
    UserManageService.create_new_user(password ,username,full_name,role,current_user_id)
    flash("کاربر جدید با موفقیت ایجاد شد" , "success")

    return redirect(url_for('user_management.user_manage'))


#==============================================================
# route =>  Edit users  
#==============================================================
@user_manage_bp.route('/edit_user/' , methods=['POST'])
def edit_user():
    
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin() 

    user_id = request.form.get("user_id","").strip()
    username = request.form.get("username","").strip()
    full_name = request.form.get("full_name","").strip()
    password = request.form.get("password","").strip()
    confirm_password = request.form.get("confirm_password","").strip()
    role = request.form.get("role","").strip()
    
    try : 
    # runnig validation service on inputs 
       validated_data =  EditUserValidate.edit_user_validate (user_id,username,full_name,password,confirm_password,role) 
       # edit user service running 
       UserManageService.edit_user(validated_data)
    except ValueError as ex : 
        flash (str(ex) ,"error")
        return redirect(url_for('user_management.user_manage'))

    
    flash("تغییرات با موفقیت اعمال شد!" , "success")
    return redirect(url_for('user_management.user_manage'))



#==============================================================
# route =>  remove users  
#==============================================================
@user_manage_bp.route("/delete_user/<int:user_id>/" , methods=['POST'])
def delete_user (user_id):

    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    UserManageService.delete_user(user_id)

    return redirect(url_for('user_management.user_manage'))

#==============================================================
# route => first initial Wizard(setup route)
#==============================================================
@setup_bp.route('/setup/' , methods=['GET', 'POST'])
def setup() :

    # if admin is exsist => redirect to login page 
    admin_exists = SeedService.admin_exists()
    if admin_exists : 
        return redirect(url_for("auth.login_page"))

    if request.method =='POST': 

        username = request.form.get('username').strip()
        full_name = request.form.get('full-name').strip()
        password = request.form.get('password').strip()
        confirm_password = request.form.get('confirm-password').strip()
        try:
            SeedService.create_admin(username,full_name,password, confirm_password)
            return redirect(url_for("auth.login_page"))
        except ValueError as ex : 
            flash(str(ex), "error")
            return redirect(url_for("setup.setup"))

    return render_template('seed.html')



    



