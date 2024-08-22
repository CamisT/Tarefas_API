from flask import Flask
from config import Config
from flasgger import Swagger 
from models import db
from logs import setup_logging
from auth import jwt, AuthResource
from resources import TarefaResource
from error_handlers import setup_error_handlers

class TaskManagerApp:
    def __init__(self, config_class=Config):
        self.app = Flask(__name__)
        self.app.config.from_object(config_class)
        self.init_extensions()
        self.register_blueprints()
        self.setup_logging()
        self.setup_error_handlers()
        self.create_db()

    def init_extensions(self):
        db.init_app(self.app)
        jwt.init_app(self.app)
        Swagger(self.app, template={
    "swagger": "2.0",
    "info": {
        "title": "API de Gerenciamento de Tarefas",
        "description": "Documentação da API para Gerenciamento de Tarefas",
        "version": "1.0.0"
    },
    "basePath": "/api/v1"
})

    def register_blueprints(self):
        # Instanciar as classes AuthResource e TarefaResource
        auth_resource = AuthResource()
        tarefa_resource = TarefaResource()
        
        # Registrar os blueprints
        self.app.register_blueprint(auth_resource.api)
        self.app.register_blueprint(tarefa_resource.api)

    def setup_logging(self):
        setup_logging(self.app)

    def setup_error_handlers(self):
        setup_error_handlers(self.app)

    def create_db(self):
        with self.app.app_context():
            db.create_all()

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == '__main__':
    app = TaskManagerApp()
    app.run()
