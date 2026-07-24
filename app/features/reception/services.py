from flask import request

from app import db
from app.features.reception.finder import ReceptionFinder
from app.features.reception.formater import ReceptionFormatter
from app.features.reception.updater import ReceptionUpdater
from app.features.reception.validator import ReceptionValidator
import jdatetime


class ReceptionService:
    jdatetime = jdatetime

    @classmethod
    def process_reception_request(cls, request):
        national_code = request.form.get('national_code', '').strip()
        battalion_option = request.form.get('battalion_option')
        company_option = request.form.get('company_option')
        action = request.form.get('action')

        valid, national_code, message = ReceptionValidator.request_validator(
            national_code, battalion_option, company_option
        )
        if not valid:
            raise ValueError(message)

        valid, national_code, message = ReceptionValidator.national_code_validator(national_code)
        if not valid:
            raise ValueError(message)

        soldier = ReceptionFinder.find_soldier(national_code)
        if soldier is None:
            raise ValueError('فرد یافت نشد')

        Result = ReceptionFormatter.prepare(soldier)
        enable_first_initial = (
            soldier is not None
            and battalion_option
            and company_option
            and soldier.status == 'پذیرش-نشده'
        )

        if action == 'first_initial':
            ReceptionUpdater.assign_battalion_company_status(
                soldier=soldier,
                battalion_option=battalion_option,
                company_option=company_option,
                status='ثبت-اولیه',
            )
            enable_first_initial = False

        return Result, enable_first_initial, national_code

    @classmethod
    def get_first_initial_soldiers(cls):
        return ReceptionFinder.find_first_initial()

    @classmethod
    def update_status(cls, request):
        data = request.get_json() or {}
        ids = data.get('ids', [])
        status = data.get('status')

        if not ids or not status:
            raise ValueError('اطلاعات نامعتبر است')

        from app.models import Soldier

        Soldier.query.filter(Soldier.id.in_(ids)).update({Soldier.status: status}, synchronize_session=False)
        db.session.commit()
