#mapping data_frame data to table columns in data_base 
import pandas as pd
from datetime import date
import jdatetime
class SoldierMapper :   

    @staticmethod
    def clean_value(value):

        if pd.isna(value):
            return None

        return value

    @staticmethod
    def convert_birth_date(value):

        if value is None:
            return None

        if pd.isna(value):
            return None

        if isinstance(value, str):

            try:
                year, month, day = value.split("/")

                jalali = jdatetime.date(
                    int(year),
                    int(month),
                    int(day)
                )

                return jalali.togregorian()

            except Exception:
                return None

        return value

    @staticmethod
    def convert_marriage(value):

        if value is None:
            return None


        if value in ["متاهل", "بله", True]:
            return True


        if value in ["مجرد", "خیر", False]:
            return False


        return None
        if model_field == "is_marriage":

            value = cls.convert_marriage(value)


    COLUMN_MAP = {
            "نام":"first_name",
            "نام خانوادگی":"last_name",
            "نام پدر":"father_name",
            "کد ملی":"national_code",
            "تاریخ تولد":"birth_date",
            "تحصیلات":"education",
            "رشته تحصیلی":"field",
            "وضعیت سلامت":"health_status",
            "مذهب":"religion",
            "تلفن":"phone",
            "استان":"province",
            "شهر":"city",
            "آدرس":"address",
            "وضعیت تاهل":"is_marriage",
    }

    @classmethod
    def map_row(cls, row):

        soldier = {}

        for excel_column, model_field in cls.COLUMN_MAP.items():

            value = row[excel_column]


            if model_field == "birth_date":
                value = cls.convert_birth_date(value)


            else:
                value = cls.clean_value(value)


            soldier[model_field] = value


        return soldier


    @classmethod
    def map_dataframe(cls, df):

        soldiers = []

        for _, row in df.iterrows():
            soldiers.append(
                cls.map_row(row)
            )

        return soldiers


    