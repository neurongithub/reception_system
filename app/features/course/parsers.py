import json
from pathlib import Path
import pandas as pd


class ExcelParser:

    ALLOWED_EXTENSIONS = [".xlsx", ".xls"]

    @staticmethod
    def parse(file_path):
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError("فایل اکسل پیدا نشد")

        if file_path.suffix not in ExcelParser.ALLOWED_EXTENSIONS:
            raise ValueError("فرمت فایل ورودی مجاز نمیباشد only [xls,xlsx]")

        df = pd.read_excel(file_path, dtype={"کد ملی": str})
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df = df.dropna(how="all")
        df.columns = df.columns.astype(str).str.strip()

        return df


class JsonParser:

    @staticmethod
    def parse(file_path):
        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
