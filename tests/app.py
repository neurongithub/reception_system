from flask import Flask
from markupsafe import escape

application = Flask("--__name__")

@application.route('/users/<username>')

def user_account (username) :

    return f"username is : {escape(username)}"

@application.route('/ids/<float:u_id>/')

def user_id (u_id):

    return f"id is :{escape(u_id)}"




