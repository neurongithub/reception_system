#All routes & views & blueprints
from flask import Blueprint,render_template , request , redirect , url_for , session ,abort , flash , current_app
from app.models import User, Course , Soldier
from werkzeug.security import check_password_hash ,generate_password_hash
from werkzeug.utils import secure_filename
from pathlib import Path
from app.excel.parser import ExcelParser
from app.excel.validator import ExcelValidator
from app.excel.mapper import SoldierMapper
from app.excel.importer import SoldierImporter
from app.json_parse.json_parser import JsonParser
from app.json_parse.json_mapper import JsonMapper
from app.json_parse.responder import JsonResponser
from datetime import datetime
from app import db
from uuid import uuid4
import os
import json


#main Blueprint
main_bp = Blueprint('main', __name__)

#login route - http://host.com/login/
@main_bp.route('/login/' , methods = ["GET" ,"POST"])
def login_page () : 

    
    #get server time zone and date to show in UI
    current_time = datetime.now()
    formated_time =current_time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y/%m/%d")

    if request.method == "POST" : 
        
        # remember me check box (default==True)
        remember =bool(request.form.get("remember"))

        #saving value of username & password 
        username = request.form.get("username")
        password = request.form.get("password")

        #checing on username & password is require!!!
        if not username : 
            flash ("وارد کردن نام کاربری اجباری میباشد" ,'error')
            return redirect(url_for('main.login_page'))
        if not password :
            flash("وارد کردن پسورد اجباری میباشد" , 'error')
            return redirect(url_for('main.login_page'))

        #search query on username 
        user = User.query.filter_by(username=username).first()
        
        if not user : 
            flash("خطا:‌ نام کاربری یا رمزعبور اشتباه وارد شده است", "error")
            return redirect(url_for("main.login_page"))
            
       
        #cheeck on username & password 
        if user and check_password_hash(user.password_hashed , password): 
            if user.role =="admin" : 
                
                #Set session 
                session.permanent = remember # session expire time 
                session['user_id']  = user.id 
                session ['role'] = user.role
                
                
                #if is admin return darboard page
                return redirect(url_for('main.dashboard'))
           
                
            
            elif user.role=="viewer" : 

                session.permanent = remember
                session["user_id"] = user.id
                session["role"] = user.role

                # print("SESSION AFTER LOGIN:", dict(session))

                return redirect(url_for("main.view"))
               
               #if invalid user return Error  with alert box 
            else :
                return "<h1></h1>"
        else :
            flash("خطا: نام کاربری یا رمز عبور اشتباه وارد شده است", "error")
            return redirect(url_for("main.login_page"))
            
    
    
    return render_template('login.html', time=formated_time , date=current_date  )


#Change password functionality 
@main_bp.route("/dashboard/changepassword/", methods=["POST"])
def change_pass():

    # Get form inputs
    username = request.form.get("username", "").strip()
    old_pass = request.form.get("old-password", "").strip()
    new_pass = request.form.get("new-password", "").strip()
    again_new_pass = request.form.get("again-password", "").strip()

    # 1. Check empty inputs
    if not username or not old_pass or not new_pass or not again_new_pass:
        flash("برای تغییر رمز عبور همه مقادیر را وارد کنید", "error")
        return redirect(url_for("main.login_page"))

    # 2. Find user
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("نام کاربری یافت نشد", "error")
        return redirect(url_for("main.login_page"))

    # 3. Check current password
    if not check_password_hash(user.password_hashed, old_pass):
        flash("رمز عبور فعلی صحیح نمی باشد", "error")
        return redirect(url_for("main.login_page"))

    # 4. Check new password confirmation
    if new_pass != again_new_pass:
        flash("رمز جدید و تکرار آن یکسان نیست", "error")
        return redirect(url_for("main.login_page"))

    # 5. Check new password is different from old password
    if check_password_hash(user.password_hashed, new_pass):
        flash("رمز جدید نباید با رمز قبلی یکسان باشد", "error")
        return redirect(url_for("main.login_page"))

    # 6. Check password length
    if len(new_pass) < 4:
        flash("طول رمز جدید نباید از ۸ کاراکتر کمتر باشد", "error")
        return redirect(url_for("main.login_page"))

    # 7. Hash new password
    hashed_new_pass = generate_password_hash(new_pass)

    # 8. Save new password
    user.password_hashed = hashed_new_pass
    db.session.commit()

    flash("رمز عبور با موفقیت بروزرسانی شد", "success")

    return redirect(url_for("main.login_page"))



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


    current_time = datetime.now()
    formated_time =current_time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y/%m/%d")

    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    
    if session.get("role") != "admin":
        abort(403)
    
    return render_template("dashboard.html" ,time=formated_time ,date=current_date)


#create course rooute  ==> open create course page
@main_bp.route('/dashboard/create_course/')
def create_course ()  :

    #real time and date server     
    current_time = datetime.now()
    formated_time =current_time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y/%m/%d")

    #check user session 
    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    if session.get("role")!="admin" : 
        abort(403)
    
    return render_template('create_coures.html' , result=None ,time=formated_time, date=current_date)

#reception route ==> open reception page 
@main_bp.route('/dashboard/reception//')
def reception () : 

    #real time and date server     
    current_time = datetime.now()
    formated_time =current_time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y/%m/%d")

    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    if session.get("role")!="admin" : 
        abort(403)
    
    return render_template('reception.html' , time=formated_time,date=current_date)

#last courses ==> open last courses page [back log now]
@main_bp.route('/dashboard/last_courses/')
def last_courses () : 
    #real time and date server     
    current_time = datetime.now()
    formated_time =current_time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    if "user_id" not in session : 
        return redirect(url_for("main.login_page"))
    if session.get("role")!="admin" : 
        abort(403)
    
    return render_template('last_courses.html', time=formated_time , date=current_date)

#logout button endpoint 
@main_bp.route("/dashboard/logout/") 
def logout () :
    
    session.pop('user_id',None)
    session.clear()
    return redirect(url_for("main.login_page"))


@main_bp.route("/dashboard/help/")
def help() : 

    #real time and date server     
    current_time = datetime.now()
    formated_time =current_time.strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y/%m/%d")

    try:
        if "user_id" not in session:
            flash("برای دسترسی به راهنما اپلیکیشن ابتدا وارد شوید" , 'error')
            return redirect(url_for("main.login_page"))
            
    except Exception as e:
        return redirect(url_for("main.login_page"))
            
        
    
    
    return render_template("help.html" , time=formated_time,date=current_date)


@main_bp.route("/dashboard/upload/" ,methods=["GET","POST"])
# upload functionality 
def upload() : 
# 1.upolad function in upload route
    # 1.save the excel file 
     # file extension checking 
    ALLOWED_EXTENSIONS ={
        "xls", 
        "xlsx"
    }
    if request.method =='POST': 

        #==============================================================================
        #                           Handel course informations PART1 
        #==============================================================================
        #1.get input from html form for courses table
        course_name = request.form.get("course_name", "").strip()
        course_code = request.form.get("course_code", "").strip().upper()
        course_date = request.form.get("course_date" , "")
        
        #validate fileds not empty 
        if not course_name or not course_code or not course_date:
            flash("لطفا تمامی اطلاعات دوره را واردکنید!", "warning")
            return redirect(url_for("main.create_course"))

        #convert date string to python date object 
        try:
            course_date = datetime.strptime(course_date, "%Y-%m-%d").date()
        except ValueError:
            flash("فرمت تاریخ اشتباه است " , "error")
            return redirect(url_for("main.create_course"))
        
        #==============================================================================
        #                           Handel <<excel>> file PART1
        #==============================================================================
        
        def allowed_file (filename) : 
            return ("." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS)
        
        #basic validation
        if "excel_file" not in request.files:
            flash("خطا : فایل اکسل را انتخاب کنید" ,'error')
            return redirect(url_for("main.create_course"))

        file = request.files["excel_file"]

        if file.filename == "":
            flash("[Error]-فایل اکسل انتخاب نشده است ابتدا فایل اکسل را وارد کنید" , 'error')
            ##print("choose file please ") #just show me on server log in testsing 
            return redirect(url_for("main.create_course"))
        
        if not allowed_file(file.filename):
            print("invalid input type")
            flash("Invalid file type ",'error')
            return redirect(url_for("main.create_course"))
        
        
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        upload_folder.mkdir(parents=True, exist_ok=True)

        ###### prevent to over write new excel file 
        original_filename = secure_filename(file.filename)
        extension = Path(original_filename).suffix
        unique_filename = f"{uuid4()}{extension}"
        # file.save(upload_folder / file.filename)
        file_path = upload_folder / unique_filename
        file.save (file_path)
        filename = secure_filename(file.filename)
        print("File uploaded successfully")
        #========================================================================================
        #                          Handel course informations PART2
        #========================================================================================
        #Create course Object 
        new_course = Course(
            course_name=course_name, 
            course_code=course_code, 
            course_date=course_date, 
            excel_file=unique_filename
        )
        #save course object to data_base

        try:
            db.session.add(new_course)
            db.session.flush()

        except : 
            db.session.rollback()
            flash("این دروه قبلا ایجاد شده است" ,"error")
            return redirect(url_for("main.create_course"))
        
    # # 2. excel parsing 
        course_id = new_course.id
        try :
            df = ExcelParser.parse(file_path)
        except Exception as e : 
                flash(str(e),"error")
                return redirect(url_for("main.create_course"))

# # 3. validate parsed excel (validate data_fram)

        try:
            ExcelValidator.validate_columns(df)
            ExcelValidator.validate_required_values(df)
        except Exception as e : 
            flash(str(e), "error")
            return redirect(url_for("main.create_course"))

# # 4. Mapper 
        soldiers_data =  SoldierMapper.map_dataframe(df)
    
        # soldiers_data = SoldierMapper.map_dataframe(df)
        # print(soldiers_data[0])
# # 5.importer 
        try :
            SoldierImporter.import_data(soldiers_data, new_course.id)
        except Exception as e:
            db.session.rollback()
            flash(f"خطا درثبت سرباز ها " "error")
            return redirect(url_for("main.create_course"))
        #evey thing is ok showing this message 
        
        #==============================================================================
        #                           Handel battalion & company informations (json file) 
        #==============================================================================

        # 1.get battalion and company from html input
        config ={
            "course_id" : course_id,
            "course_code": course_code,
            "course_name": course_name,
            "battalions" : {} 
        }
        # print(request.form.to_dict())
        for battalion in range (1,4): 

            config["battalions"][str(battalion)] ={}

            for company in range (1,6):
                field = f"b{battalion}-c{company}"
                config["battalions"][str(battalion)][str(company)] = request.form.get(field)
        # print(config)


        # 2.save python_object to json file
        json_folder = Path("json_folder")
        json_folder.mkdir(exist_ok=True)
        json_file = json_folder / f"{course_code}.json"

        with open (json_file, "w",  encoding="utf-8")as f :
            json.dump(config , f , ensure_ascii=False, indent=4)

        #==============================================================================
        #                           show json parsing result 
        #==============================================================================
        #3.parsing json file 

        #json file location 
        json_folder = current_app.config['JSON_FOLDER']

        # json parser 
        original_json_file = json_folder / f"{course_code}.json"
        try :
            json_df = JsonParser.parse(original_json_file)
        except Exception as e : 
            flash (f"json parssing Incompelete!!{e}" , 'error')
        # print(json_df)

        #json mapper
        try:
            json_mapp = JsonMapper.mapper(json_df)
            
        except Exception as e : 
            flash (f"json mapping is Incompelete!!{e}" , 'error')


        #json responder
        try:
            json_final = JsonResponser.response(json_mapp)
            return json_final
        except Exception as e :
            flash(f"[-] json responser error" , 'error')

        #success message finaly
        flash("دوره با موفقیت ایجاد شد" , "success")
        return redirect(url_for("main.create_course"))


# # 5. save in data_base


        
    flash("آپلود فایل اکسل با موفقیت انجام شد!!!", "success")
        
    return redirect(url_for("main.create_course"))
    

