from flask import Blueprint, flash, redirect, request, url_for

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
            Result, enable_first_initial, national_code = ReceptionService.process_reception_request(request)
            flash('عملیات پذیرش با موفقیت انجام شد', 'success')
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
