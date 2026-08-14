from app import db
from app.models import Soldier


class SoldierImporter:

    @staticmethod
    def import_data(soldiers_data, course_id):
        soldiers = []

        national_codes = [
            str(soldier_data.get("national_code", "")).strip()
            for soldier_data in soldiers_data
            if soldier_data.get("national_code") is not None
        ]

        if national_codes:
            existing_codes = {
                code for (code,) in db.session.query(Soldier.national_code)
                .filter(Soldier.national_code.in_(national_codes))
                .distinct()
                .all()
            }
        else:
            existing_codes = set()

        if existing_codes:
            raise ValueError(
                f"کد ملی تکراری در پایگاه داده: {', '.join(sorted(existing_codes))}"
            )

        for soldier_data in soldiers_data:
            soldier = Soldier(course_id=course_id, **soldier_data)
            db.session.add(soldier)
            soldiers.append(soldier)

        db.session.commit()
        return soldiers
