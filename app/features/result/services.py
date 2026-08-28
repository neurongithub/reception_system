from app import db
from sqlalchemy import func
from app.models import Soldier


class Result:

    @classmethod
    def get_company_counts(cls):

        rows = (
            db.session.query(
                Soldier.battalion,
                Soldier.company,
                func.count(Soldier.id).label("count")
            )
            .filter(
                Soldier.status == "پذیرش-شده"
            )
            .group_by(
                Soldier.battalion,
                Soldier.company
            )
            .order_by(
                Soldier.battalion,
                Soldier.company
            )
            .all()
        )

        return rows

    @classmethod
    def build_result_structure(cls, rows):

        result = {}

        for battalion, company, count in rows:

            if battalion not in result:
                result[battalion] = {}

            result[battalion][company] = {
                "count": count
            }

        return result

    @classmethod
    def get_health_statistics(cls):

        rows = (
            db.session.query(
                Soldier.battalion,
                Soldier.company,
                Soldier.health_status,
                func.count(Soldier.id).label("count")
            )
            .filter(
                Soldier.status == "پذیرش-شده"
            )
            .group_by(
                Soldier.battalion,
                Soldier.company,
                Soldier.health_status
            )
            .order_by(
                Soldier.battalion,
                Soldier.company
            )
            .all()
        )

        return rows

    @classmethod
    def add_health_statistics(cls, result, rows):

        for battalion, company, health, count in rows:

            company_data = result[battalion][company]

            company_data.setdefault("health", {})

            company_data["health"][health] = count

        return result

    @classmethod
    def get_religion_statistics(cls):

        rows = (
            db.session.query(
                Soldier.battalion,
                Soldier.company,
                Soldier.religion,
                func.count(Soldier.id).label("count")
            )
            .filter(
                Soldier.status == "پذیرش-شده"
            )
            .group_by(
                Soldier.battalion,
                Soldier.company,
                Soldier.religion
            )
            .order_by(
                Soldier.battalion,
                Soldier.company
            )
            .all()
        )

        return rows

    @classmethod
    def add_religion_statistics(cls, result, rows):

        for battalion, company, religion, count in rows:

            company_data = result[battalion][company]

            company_data.setdefault("religion", {})

            company_data["religion"][religion] = count

        return result

    @classmethod
    def get_education_statistics(cls):

        rows = (
            db.session.query(
                Soldier.battalion,
                Soldier.company,
                Soldier.education,
                func.count(Soldier.id).label("count")
            )
            .filter(
                Soldier.status == "پذیرش-شده"
            )
            .group_by(
                Soldier.battalion,
                Soldier.company,
                Soldier.education
            )
            .order_by(
                Soldier.battalion,
                Soldier.company
            )
            .all()
        )

        return rows

    @classmethod
    def add_education_statistics(cls, result, rows):

        for battalion, company, education, count in rows:

            company_data = result[battalion][company]

            company_data.setdefault("education", {})

            company_data["education"][education] = count

        return result

    @classmethod
    def get_result_data(cls):

        # 1. تعداد افراد هر گروهان
        company_rows = cls.get_company_counts()

        # 2. ساخت ساختار اولیه
        result = cls.build_result_structure(company_rows)

        # 3. آمار وضعیت سلامت
        health_rows = cls.get_health_statistics()
        cls.add_health_statistics(result, health_rows)

        # 4. آمار مذهب
        religion_rows = cls.get_religion_statistics()
        cls.add_religion_statistics(result, religion_rows)

        # 5. آمار تحصیلات
        education_rows = cls.get_education_statistics()
        cls.add_education_statistics(result, education_rows)

        return result