import re


class CourseInfoValidation:

    @staticmethod
    def course_info_validate(course_name, course_code, course_date):
        if not course_name or not course_code or not course_date:
            raise ValueError("مقادیر ستاره دار * اجباری است")

        pattern = r"^[A-Z0-9_-]+$"
        if not re.fullmatch(pattern, course_code):
            raise ValueError("کد دوره فقط می‌تواند شامل حروف بزرگ انگلیسی، عدد، خط تیره و آندرلاین باشد")

        if len(course_name) > 100:
            raise ValueError("نام دوره بیش از حد طولانی است")

        if len(course_code) > 20:
            raise ValueError("کد دوره بیش از حد طولانی است")

    



class ExcelValidation:

    # ستون های اجباری فایل اکسل ورودی 
    REQUIRED_COLUMNS = {
        "نام",
        "نام خانوادگی",
        "نام پدر",
        "کد ملی",
        "تاریخ تولد",
        "تحصیلات",
        "وضعیت سلامت",
    }
    # هر ردیف در فایل اکسل باید حتما این سه  ستون را داشته باشد و حتما هم مقدار داشته باشند
    REQUIRED_VALUES = [
        "نام",
        "نام خانوادگی",
        "کد ملی",
    ]

    @classmethod
    def validate_columns(cls, df):
        missing_columns = cls.REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            raise ValueError(f"ستون‌های زیر پیدا نشدند: {missing_columns}")
        return True

    @classmethod
    def validate_required_values(cls, df):
        for column in cls.REQUIRED_VALUES:
            if df[column].isnull().any():
                raise ValueError(f"ستون {column} نمی‌تواند مقدار خالی داشته باشد")
        return True

    @classmethod
    def validate_national_codes(cls, df):
        national_codes = df["کد ملی"].astype(str).str.strip()

        if national_codes.isnull().any() or (national_codes == "").any():
            raise ValueError("یک یا چند کد ملی خالی یا نامعتبر در فایل اکسل وجود دارد")

        invalid_codes = national_codes[~national_codes.str.fullmatch(r"\d{10}")]
        if not invalid_codes.empty:
            raise ValueError("یک یا چند کد ملی نامعتبر در فایل اکسل وجود دارد")

        duplicated_codes = national_codes[national_codes.duplicated(keep=False)]
        if not duplicated_codes.empty:
            duplicates = sorted(set(duplicated_codes.tolist()))
            raise ValueError(f"کد ملی تکراری در فایل اکسل: {', '.join(duplicates)}")

        return True

    @staticmethod
    def validate_national_code(value):
        value = str(value).strip()
        if len(value) != 10:
            return False
        if not value.isdigit():
            return False
        return True
