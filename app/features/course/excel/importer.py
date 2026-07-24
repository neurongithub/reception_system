# this is file used for -> sending date to data_base
# create data_base data based on data_frame


from app import db 
from app.models import Soldier

class SoldierImporter: 

    @classmethod
    def import_data (cls, soldiers_data , course_id):

        soldiers = []

        for soldier_data in soldiers_data:

            soldier = Soldier(

                course_id=course_id,

                **soldier_data

            )

            db.session.add(soldier)

            soldiers.append(soldier)

        db.session.commit()

        return soldiers

