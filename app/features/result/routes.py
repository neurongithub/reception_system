from flask import Blueprint, render_template
from app.features.result.services import Result

import pprint


result_page_bp = Blueprint(
    "result_page",
    __name__
)


@result_page_bp.route("/result/", methods=["GET"])
def result():

    result_data = Result.get_result_data()

    pprint.pprint(result_data)

    return render_template(
        "result.html",
        result=result_data
    )