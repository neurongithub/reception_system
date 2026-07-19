

class ReceptionFormatter:

    @staticmethod 
    def prepare (soldier):
        return {
            "national_code":soldier.national_code,

            "first_name": soldier.first_name,

            "last_name": soldier.last_name,

            "father_name": soldier.father_name,

            "education": soldier.education,

            "province": soldier.province,

            "city": soldier.city,

            "phone": soldier.phone,

            "health": soldier.health_status,

            "marriage": soldier.is_marriage,

            "address": soldier.address, 

            "birth_date": soldier.birth_date,

            "field": soldier.field,

            "religion":soldier.religion, 

            "status" : soldier.status,

            "course_name": soldier.Course.course_name,
            
            "course_code": soldier.Course.course_code,

            "course_date": soldier.Course.course_date,

        }
   

