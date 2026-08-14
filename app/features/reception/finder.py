# this file use to find different stuff in database

from app.models import Soldier

class ReceptionFinder :

    #find_soldier_by_national_code
    @staticmethod
    def find_soldier(national_code):

        soldier  = Soldier.query.filter_by(national_code=national_code).first()

        return soldier

    #find all data base rows where status="ثبت-اولیه"
    @staticmethod
    def find_first_initial ():
        
        soldier = Soldier.query.filter_by(status="ثبت-اولیه").all()
        return soldier
    
    


   

        

