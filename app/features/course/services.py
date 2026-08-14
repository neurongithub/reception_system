import json
from pathlib import Path
from uuid import uuid4

import jdatetime
from flask import current_app, render_template
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Course
from app.features.common.utils import normalize_digits
from app.features.course.importers import SoldierImporter
from app.features.course.mappers import SoldierMapper, JsonMapper
from app.features.course.parsers import ExcelParser, JsonParser
from app.features.course.validator import CourseInfoValidation, ExcelValidation


class CourseService:

    ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

    #=========================================================================
    # 1.service - porcess course upload => handel course information & excel 
    #=========================================================================
    @classmethod
    def process_course_upload(cls, request):
        course_name = request.form.get('course_name', '').strip()
        course_code = request.form.get('course_code', '').strip()
        course_code = normalize_digits(course_code).upper() #convert farsi or arabic numbers to english numbers (۱۲۳ -> 123)
        course_date = request.form.get('course_date', '').strip()
        
        CourseInfoValidation.course_info_validate(course_name, course_code, course_date)

        try:
            jalali_date = jdatetime.datetime.strptime(course_date, '%Y/%m/%d')
            g_date = jalali_date.togregorian().date()
        except Exception:
            raise ValueError('فرمت تاریخ نامعتبر است. از فرمت YYYY/MM/DD استفاده کنید.')

        file = request.files.get('excel_file')
        if not file or not file.filename:
            raise ValueError('فایل اکسل انتخاب نشده است')

        if not cls.is_allowed_file(file.filename):
            raise ValueError('فرمت فایل اکسل معتبر نیست')

        

        upload_folder = current_app.config['UPLOAD_FOLDER']
        upload_folder.mkdir(parents=True, exist_ok=True)

        original_filename = Path(file.filename).name
        unique_filename = f'{uuid4()}{Path(original_filename).suffix}'
        file_path = upload_folder / unique_filename
        file.save(file_path)

        new_course = cls.create_course_record(course_name, course_code, g_date, unique_filename)
        try:
            df = ExcelParser.parse(file_path)
            ExcelValidation.validate_columns(df)
            ExcelValidation.validate_required_values(df)
            ExcelValidation.validate_national_codes(df)
            soldiers_data = SoldierMapper.map_dataframe(df)
            SoldierImporter.import_data(soldiers_data, new_course.id)
        except IntegrityError as exc:
            db.session.rollback()
            raise ValueError("خطا در وارد کردن اطلاعات سربازان: کد ملی تکراری یا داده نامعتبر") from exc
        except Exception:
            db.session.rollback()
            raise

        config = cls.build_course_config(request.form, new_course.id, course_name, course_code)
        cls.save_json_config(course_code, config)
        return cls.render_json_response(course_code)


    #=========================================================================
    # 2.service 
    #=========================================================================
    @classmethod
    def is_allowed_file(cls, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS
    #=========================================================================
    # 3.service 
    #=========================================================================
    @classmethod
    def create_course_record(cls, course_name, course_code, course_date, excel_filename):
        course = Course(
            course_name=course_name,
            course_code=course_code,
            course_date=course_date,
            excel_file=excel_filename,
        )

        db.session.add(course)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            raise ValueError('این دوره قبلا ایجاد شده است')

        return course
    #=========================================================================
    # 4.service 
    #=========================================================================
    @classmethod
    def build_course_config(cls, form, course_id, course_name, course_code):
        config = {
            'course_id': course_id,
            'course_code': course_code,
            'course_name': course_name,
            'battalions': {},
        }

        for battalion in range(1, 4):
            config['battalions'][str(battalion)] = {}
            for company in range(1, 6):
                field = f'b{battalion}-c{company}'
                config['battalions'][str(battalion)][str(company)] = form.get(field)

        return config
    #=========================================================================
    # 5.service 
    #=========================================================================
    @classmethod
    def save_json_config(cls, course_code, config):
        json_folder = current_app.config['JSON_FOLDER']
        json_folder.mkdir(parents=True, exist_ok=True)
        json_file = json_folder / f'{course_code}.json'

        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

        return json_file
    #=========================================================================
    # 6.service 
    #=========================================================================
    @classmethod
    def render_json_response(cls, course_code):
        json_folder = current_app.config['JSON_FOLDER']
        json_file = json_folder / f'{course_code}.json'
        json_df = JsonParser.parse(json_file)
        json_mapp = JsonMapper.mapper(json_df)
        return render_template('create_coures.html', result=json_mapp)