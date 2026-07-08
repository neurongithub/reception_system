# this file used for -> parse the excel file 
# work_flow : read excel file and create data frame 

import pandas as pd 

from pathlib import Path

class ExcelParser:

    ALLOWED_EXTENSIONS = [
        ".xlsx",
        ".xls"
    ]

    @staticmethod
    def parse (file_path): 

        file_path = Path(file_path)
        
        #check excel file exsist 
        if not file_path.exists ():
            raise FileNotFoundError('فایل اکسل پیدا نشد')
        
        #check excel file extension
        if file_path.suffix not in ExcelParser.ALLOWED_EXTENSIONS:
            raise ValueError('فرمت فایل ورودی مجاز نمیباشده only [xls,xlsx]')

        #data frame 
        df = pd.read_excel(file_path)

        #delete empty columns and rows 
        df.dropna (how='all', inplace = True )
        df.columns = (df.columns.astype(str).str.strip())

        
        return df
