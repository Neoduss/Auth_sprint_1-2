import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api

from src.app.oauth.oauth import init_oauth
from src.app.api.v1.routes.routes import initialize_routes
from src.app.api.v1.service.auth_service.auth_api import auth, auth_namespace
from src.app.api.v1.service.role_service.cli_commands import adm_cmd
from src.app.api.v1.service.role_service.roles_api import roles, role_namespace
from src.app.db.db import init_db
from src.app.db.db_models import db

load_dotenv(f'{os.getcwd()}/.env')

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app, version='1.0', title='Auth API',
          description='Сервис авторизации', doc='/doc/')
app.config.from_object('config')
migrate = Migrate(app, db)


app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

init_db(app)
init_oauth(app)
initialize_routes(api)
app.register_blueprint(auth)
app.register_blueprint(roles)
app.register_blueprint(adm_cmd)
api.add_namespace(role_namespace)
api.add_namespace(auth_namespace)

if __name__ == '__main__':
    app.run()
