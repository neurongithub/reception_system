from flask import request
import json
from datetime import date
from flask import current_app
from app import db
from app.features.reception.finder import ReceptionFinder
from app.features.reception.formater import ReceptionFormatter
from app.features.reception.updater import ReceptionUpdater
from app.features.reception.validator import ReceptionValidator
from app.features.course.mappers import JsonMapper
from app.models import Soldier, Course
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

        return Result, enable_first_initial, national_code , action

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


    #================================================================
    # find & return battalion/company from json file 
    #================================================================

    @staticmethod
    def load_json (course_code): 

        json_folder = current_app.config["JSON_FOLDER"]
        json_file = json_folder / f"{course_code}.json"

        if not json_file.exists():
            raise FileNotFoundError(f"Configuration for course {course_code} not found.")

        with open(json_file, "r", encoding="utf-8") as json_file : 
            return json.load(json_file)
    
    @classmethod
    def get_company_allocation(cls , course_code,battalion,company): 
        config = cls.load_json(course_code)
        battalion_data = config["battalions"].get(str(battalion), {})
        value = battalion_data.get(str(company))

        if value is None:
            return None

        if isinstance(value, str):
            mapped_value = JsonMapper.OBJECT_MAP.get(value, value)
            return mapped_value or None

        return str(value)

    @classmethod
    def get_current_allocation_label(cls, course_code, battalion, company):
        value = cls.get_company_allocation(course_code, battalion, company)

        if value is None:
            return "تخصیصی ثبت نشده است"

        return value

    # ================================================================
    # service=> inputs from manual reception form
    # ================================================================
    @staticmethod
    def normalize_digits(value):
        if value is None:
            return None
        return str(value).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))

    @staticmethod
    def parse_birth_date(value):
        if value in (None, ''):
            return None

        cleaned = str(value).strip()
        if not cleaned:
            return None

        cleaned = ReceptionService.normalize_digits(cleaned)

        for candidate in (cleaned, cleaned.replace('/', '-')):
            try:
                return date.fromisoformat(candidate)
            except ValueError:
                pass

        try:
            return jdatetime.date.strptime(cleaned, '%Y/%m/%d').togregorian()
        except Exception:
            pass

        raise ValueError('تاریخ تولد معتبر نیست')

    @classmethod
    def get_inputs_manual_reception(cls, request):
        raw = request.form

        return {
            'national_code': (raw.get('national_code', '') or '').strip(),
            'first_name': (raw.get('first_name', '') or '').strip(),
            'last_name': (raw.get('last_name', '') or '').strip(),
            'father_name': (raw.get('father_name', '') or '').strip(),
            'birth_date': (raw.get('birth_date', '') or '').strip(),
            'education': (raw.get('education', '') or '').strip(),
            'field': (raw.get('field', '') or '').strip(),
            'health_status': (raw.get('health_status') or raw.get('health') or '').strip(),
            'religion': (raw.get('religion', '') or '').strip(),
            'is_marriage': (raw.get('is_marriage') or raw.get('marriage') or '').strip(),
            'province': (raw.get('province', '') or '').strip(),
            'city': (raw.get('city', '') or '').strip(),
            'phone': (raw.get('phone', '') or '').strip(),
            'address': (raw.get('address', '') or '').strip(),
            'course_code': (raw.get('course_code', '') or '').strip(),
        }

    # ================================================================
    # service=> validate inputs 
    # ================================================================

    @classmethod
    def validate_inputs_manual_reception(cls, inputs):
        cleaned = {}

        for field, value in inputs.items():
            if field in ['course_code']:
                cleaned[field] = (value or '').strip()
                continue

            if value is None:
                value = ''

            value = str(value).strip()
            if not value and field in ['national_code', 'first_name', 'last_name', 'father_name']:
                raise ValueError(f"مقدار {field} الزامی است")

            if field == 'national_code':
                value = cls.normalize_digits(value)
                if not value.isdigit() or len(value) != 10:
                    raise ValueError('کد ملی باید 10 رقم باشد')

            if field == 'birth_date':
                if value:
                    value = cls.parse_birth_date(value)
                else:
                    value = None

            if field in ['education', 'field', 'health_status', 'religion', 'is_marriage', 'province', 'city', 'phone', 'address'] and not value:
                value = None

            cleaned[field] = value

        national_code = cleaned.get('national_code')
        if national_code:
            existing_soldier = Soldier.query.filter_by(national_code=national_code).first()
            if existing_soldier is not None:
                raise ValueError('این کد ملی قبلا در دیتابیس ثبت شده است')

        course_code = cleaned.get('course_code')
        if not course_code:
            raise ValueError('دوره مورد نظر انتخاب نشده است')

        course = Course.query.filter_by(course_code=course_code).first()
        if course is None:
            raise ValueError('کد دوره معتبر نیست')

        cleaned['course_id'] = course.id
        cleaned.pop('course_code', None)

        return cleaned

    # ============================================
    # service => push data into database 
    # ===========================================
    @staticmethod
    def manual_reception_add_user(validated_inputs):
        payload = dict(validated_inputs)
        payload['status'] = payload.get('status', 'ثبت-اولیه')
        payload['is_green'] = payload.get('is_green', False)

        soldier = Soldier(**payload)
        db.session.add(soldier)
        db.session.commit()
        return soldier



            
            
            
