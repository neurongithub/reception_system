# return final resutl(parsed‌ &‌ mapped ) to html format to showing in web page 
from flask import render_template, redirect , url_for, request

class JsonResponser : 


    @staticmethod
    def response(mapped_df):
        
        return render_template("create_coures.html", result=mapped_df) 