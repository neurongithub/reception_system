class ExcelValidator:

    REQUIRED_COLUMNS = {
        "نام",
        "نام خانوادگی",
        "نام پدر",
        "کد ملی",
        "تاریخ تولد",
        "تحصیلات",
        "وضعیت سلامت",
    }


    @classmethod
    def validate_columns(cls, df):

        missing_columns = (
            cls.REQUIRED_COLUMNS
            -
            set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                f"Missing columns: {missing_columns}"
            )

        return True


    @classmethod
    def validate_required_values(cls, df):

        required = [
            "نام",
            "نام خانوادگی",
            "کد ملی"
        ]

        for column in required:

            if df[column].isnull().any():

                raise ValueError(
                    f"Empty values found in {column}"
                )

        return True


    @staticmethod
    def validate_national_code(value):

        value = str(value).strip()

        if len(value) != 10:
            return False

        if not value.isdigit():
            return False

        return True