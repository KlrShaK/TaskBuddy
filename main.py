import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_login import LoginManager
from flask import render_template, flash, redirect

def create_app(app=None, api=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")

    if os.getenv('ENV', "development") == "production":
        raise Exception("No production config setup")
    else:
        print("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)

    api = Api(app)
    app.app_context().push()
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app, api
app, api = create_app()

#importing all controlers
from application.routes import *

if __name__=="__main__":
    # db.create_all() #todo Run only once overwrites everything
    app.run(host='0.0.0.0',port=8080)