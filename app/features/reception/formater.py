

class ReceptionFormatter:

    @staticmethod
    def normalize_marriage(value):
        if value is None:
            return "نامشخص"

        if isinstance(value, str):
            normalized = value.strip()
            if normalized in {"0", "False", "false", "مجرد"}:
                return "مجرد"
            if normalized in {"1", "True", "true", "متاهل"}:
                return "متاهل"
            return normalized

        if value is False or value == 0:
            return "مجرد"

        if value is True or value == 1:
            return "متاهل"

        return str(value)

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

            "marriage": ReceptionFormatter.normalize_marriage(soldier.is_marriage),

            "address": soldier.address, 

            "birth_date": soldier.birth_date,

            "field": soldier.field,

            "religion":soldier.religion, 

            "status" : soldier.status,

            "course_name": soldier.Course.course_name,
            
            "course_code": soldier.Course.course_code,

            "course_date": soldier.Course.course_date,

        }
   

