
# from database import db
from app import db

class ReceptionUpdater:

    
    @staticmethod
    def assign_battalion_company_status(soldier,battalion_option,company_option,status="ثبت-اولیه"):

        soldier.battalion = battalion_option
        soldier.company = company_option 
        soldier.status = status

        db.session.commit()

        return soldier

    
