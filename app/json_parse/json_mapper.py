# mapping parsed data final format
# mapping : option1 -> 'تحصیلاتی-سالم-شیعه'


class JsonMapper:

    OBJECT_MAP = {
        "option0": "",
        "option1": "تحصیلاتی-سالم-شیعه",
        "option2": "دیپلم-شیعه-سالم",
        "option3": "تحصیلاتی-سنی-سالم",
        "option4": "دیپلم-سنی-سالم",
        "option5": "تحصیلاتی-شیعه-معاف",
        "option6": "دیپلم-شیعه-معاف",
        "option7": "تحصیلاتی-سنی-معاف",
        "option8": "دیپلم-سنی-معاف",
        "option9": "کفایتی"
    }


    @staticmethod
    def map_companies(battalion):

        companies = []

        for company_id, company_data in battalion.items():

            mapped_value = JsonMapper.OBJECT_MAP.get(
                company_data,
                company_data
            )

            companies.append(
                {
                    "company_id": company_id,
                    "value": mapped_value
                }
            )

        return companies


    @staticmethod
    def mapper(json_df):

        # extract course information
        course_id = json_df['course_id']
        course_code = json_df['course_code']
        course_name = json_df['course_name']


        # extract battalion information
        battalion_1 = json_df["battalions"]["1"]
        battalion_2 = json_df["battalions"]["2"]
        battalion_3 = json_df["battalions"]["3"]


        # mapping companies
        battalion_1_companies = JsonMapper.map_companies(battalion_1)
        battalion_2_companies = JsonMapper.map_companies(battalion_2)
        battalion_3_companies = JsonMapper.map_companies(battalion_3)


        # final data for template
        mapped_result = {

            "course_id": course_id,

            "course_code": course_code,

            "course_name": course_name,


            "battalions": {

                "1": battalion_1_companies,

                "2": battalion_2_companies,

                "3": battalion_3_companies

            }

        }


        return mapped_result