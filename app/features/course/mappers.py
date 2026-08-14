import jdatetime
import pandas as pd


class SoldierMapper:

    @staticmethod
    def clean_value(value):
        if pd.isna(value):
            return None

        return value

    @staticmethod
    def convert_birth_date(value):
        if value is None or pd.isna(value):
            return None

        if isinstance(value, str):
            try:
                year, month, day = value.split("/")
                jalali = jdatetime.date(int(year), int(month), int(day))
                return jalali.togregorian()
            except Exception:
                return None

        return value

    @staticmethod
    def convert_marriage(value):
        if value is None or pd.isna(value):
            return None

        if value in ["متأهل","متاهل", "بله", True]: # store 1 in database table
            return True

        if value in ["مجرد", "خیر", False]: # sotre 0 in database table 
            return False

        return None

    COLUMN_MAP = {
        "نام": "first_name",
        "نام خانوادگی": "last_name",
        "نام پدر": "father_name",
        "کد ملی": "national_code",
        "تاریخ تولد": "birth_date",
        "تحصیلات": "education",
        "رشته تحصیلی": "field",
        "وضعیت سلامت": "health_status",
        "مذهب": "religion",
        "تلفن": "phone",
        "استان": "province",
        "شهر": "city",
        "آدرس": "address",
        "وضعیت تاهل": "is_marriage",
    }

    @classmethod
    def map_row(cls, row):
        soldier = {}

        for excel_column, model_field in cls.COLUMN_MAP.items():
            value = row[excel_column]

            if model_field == "birth_date":
                value = cls.convert_birth_date(value)
            elif model_field == "is_marriage":
                value = cls.convert_marriage(value)
            else:
                value = cls.clean_value(value)

            soldier[model_field] = value

        return soldier

    @classmethod
    def map_dataframe(cls, df):
        soldiers = []

        for _, row in df.iterrows():
            soldiers.append(cls.map_row(row))

        return soldiers


class JsonMapper:

    OBJECT_MAP = {
        "option0": "",
        "option1": "تحصیلاتی-شیعه-سالم",
        "option2": "دیپلم-شیعه-سالم",
        "option3": "تحصیلاتی-سنی-سالم",
        "option4": "دیپلم-سنی-سالم",
        "option5": "تحصیلاتی-شیعه-معاف",
        "option6": "دیپلم-شیعه-معاف",
        "option7": "تحصیلاتی-سنی-معاف",
        "option8": "دیپلم-سنی-معاف",
        "option9": "کفایتی",
    }

    @staticmethod
    def map_companies(battalion):
        companies = []

        for company_id, company_data in battalion.items():
            mapped_value = JsonMapper.OBJECT_MAP.get(company_data, company_data)
            companies.append({"company_id": company_id, "value": mapped_value})

        return companies

    @staticmethod
    def mapper(json_df):
        course_id = json_df["course_id"]
        course_code = json_df["course_code"]
        course_name = json_df["course_name"]

        battalion_1 = json_df["battalions"]["1"]
        battalion_2 = json_df["battalions"]["2"]
        battalion_3 = json_df["battalions"]["3"]

        battalion_1_companies = JsonMapper.map_companies(battalion_1)
        battalion_2_companies = JsonMapper.map_companies(battalion_2)
        battalion_3_companies = JsonMapper.map_companies(battalion_3)

        return {
            "course_id": course_id,
            "course_code": course_code,
            "course_name": course_name,
            "battalions": {
                "1": battalion_1_companies,
                "2": battalion_2_companies,
                "3": battalion_3_companies,
            },
        }
