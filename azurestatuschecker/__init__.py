import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here-da-boo-dee-da-bo-daa'

    if 'DATABASE_URL' in os.environ:
        postgresql_url = os.environ['DATABASE_URL']
    else:
        postgresql_url = "postgresql://{}:{}@localhost:5432/{}".format(os.environ['POSTGRES_USERNAME'], os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_DATABASE'])

    app.config['SQLALCHEMY_DATABASE_URI'] = postgresql_url

    # The webhook URL requests an Azure runbook to run
    # See: https://docs.microsoft.com/en-us/azure/automation/automation-webhooks#create-a-webhook
    if 'AZURE_MC_START_WEBHOOK_URL' not in os.environ:
        raise Exception("No webhook URL is set. Please set the 'AZURE_MC_START_WEBHOOK_URL' environment variable to the Azure webhook URL.")

    if 'SERVER_IP_ADDRESS' not in os.environ:
        raise Exception("No server IP address is set. Please set the 'SERVER_IP_ADDRESS' environment variable.")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Create tables that do not exist after importing the models
    from .models import Admin
    db.create_all(app=app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Admin.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app