from flask import Blueprint, flash, redirect, request, url_for, jsonify

from app.features.common.utils import render_with_time, require_admin, require_login
from app.features.reception.services import ReceptionService

reception_bp = Blueprint('reception', __name__, url_prefix='/dashboard')


@reception_bp.route('/reception/', methods=['GET', 'POST'])
def reception():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    open_modal = False
    soldiers = []
    enable_first_initial = False
    national_code = ''
    Result = None

    if request.method == 'POST':
        try:
            Result, enable_first_initial, national_code, action = ReceptionService.process_reception_request(request)
            flash('فرد مورد نظر یافت شد', 'success')
            if action == 'first_initial':
                Result = None
                enable_first_initial = False
                national_code = ''
                flash('عملیات پذیرش با موفقیت انجام شد🆗', 'success')
        except ValueError as exc:
            flash(str(exc), 'error')

    

    return render_with_time(
        'reception.html',
        jdatetime=ReceptionService.jdatetime,
        open_modal=open_modal,
        soldiers=soldiers,
        enable_first_initial=enable_first_initial,
        national_code=national_code,
        Result=Result,
        battalion_option=request.form.get('battalion_option', ''),
        company_option=request.form.get('company_option', ''),
    )


@reception_bp.route('/final_reception/', methods=['GET'])
def final_reception():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    soldier = ReceptionService.get_first_initial_soldiers()
    return render_with_time('final_reception.html', soldier=soldier)


@reception_bp.route('/update_status/', methods=['POST'])
def update_status():
    try:
        ReceptionService.update_status(request)
        flash('ثبت نهایی سربازان با موفقیت انجام شد.', 'success')
        return {'success': True}
    except ValueError as exc:
        return {'success': False, 'message': str(exc)}


@reception_bp.route('/reception/allocation/', methods=['GET'])
def get_allocation_value():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect
    require_admin()

    course_code = request.args.get('course_code', '').strip()
    battalion = request.args.get('battalion', '').strip()
    company = request.args.get('company', '').strip()

    if not course_code or not battalion or not company:
        return jsonify({'allocation': 'تخصیصی ثبت نشده است'})

    try:
        allocation = ReceptionService.get_current_allocation_label(course_code, battalion, company)
        return jsonify({'allocation': allocation})
    except FileNotFoundError:
        return jsonify({'allocation': 'تخصیصی ثبت نشده است'})
    except ValueError:
        return jsonify({'allocation': 'تخصیصی ثبت نشده است'})

# ==========================================
# manual reception route 
# ==========================================

@reception_bp.route('/manual_reception/', methods=['GET','POST'])
def manual_reception (): 

    #1.get input data from form
    inputs = ReceptionService.get_inputs_manual_reception(request)
    
    for input_item in inputs : 
        print(type(input_item))
    #2.validate input data
    try:
        validated_inputs = ReceptionService.validate_inputs_manual_reception(inputs)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('reception.reception'))
    

    #3.save data to database 
    try:
        ReceptionService.manual_reception_add_user(validated_inputs)
    except ValueError as exc : 
        flash(str(exc),'error')
        return redirect(url_for('reception.reception'))
        
    flash("پذیرش فراگیر با موفیت انجام شد" , 'success')


    return redirect(url_for('reception.reception'))
