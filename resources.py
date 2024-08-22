from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from models import db, Tarefa
from schemas import TarefaSchema
from google_calendar import get_calendar_service

class TarefaResource:
    api = Blueprint('tarefas_api', __name__)
    tarefa_schema = TarefaSchema()
    tarefas_schema = TarefaSchema(many=True)

    @staticmethod
    @api.route('/tarefas/', methods=['POST'])
    @jwt_required()
    @swag_from({
        'tags': ['Tarefas'],
        'summary': 'Cria uma nova tarefa',
        'description': 'Endpoint para criar uma nova tarefa.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'titulo': {'type': 'string'},
                        'descricao': {'type': 'string'},
                        'data_inicio': {'type': 'string', 'format': 'date-time'},
                        'data_fim': {'type': 'string', 'format': 'date-time'}
                    },
                    'example': {
                        'titulo': 'Minha nova tarefa',
                        'descricao': 'Descrição da tarefa',
                        'data_inicio': '2024-08-21T09:00:00-03:00',
                        'data_fim': '2024-08-21T17:00:00-03:00'
                    }
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Tarefa criada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'titulo': {'type': 'string'},
                        'descricao': {'type': 'string'}
                    }
                }
            }
        }
    })
    def criar_tarefa():
        data = request.json
        tarefa_data = TarefaResource.tarefa_schema.load(data)
        nova_tarefa = Tarefa(
            titulo=tarefa_data['titulo'],
            descricao=tarefa_data.get('descricao')
        )
        db.session.add(nova_tarefa)
        db.session.commit()

        # Criar um evento no Google Calendar
        service = get_calendar_service()

        event = {
            'summary': nova_tarefa.titulo,
            'description': nova_tarefa.descricao,
            'start': {
                'dateTime': data.get('data_inicio'),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': data.get('data_fim'),
                'timeZone': 'America/Sao_Paulo',
            },
        }
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        current_app.logger.info(f"Evento criado: {event_result.get('htmlLink')}")

        current_app.logger.info(f"Tarefa criada com ID: {nova_tarefa.id} e evento no Google Calendar criado com ID: {event_result['id']}")
        return jsonify(TarefaResource.tarefa_schema.dump(nova_tarefa)), 201

    @staticmethod
    @api.route('/tarefas/', methods=['GET'])
    @jwt_required()
    @swag_from({
        'tags': ['Tarefas'],
        'summary': 'Lista todas as tarefas',
        'description': 'Endpoint para listar todas as tarefas.',
        'responses': {
            200: {
                'description': 'Lista de tarefas',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'titulo': {'type': 'string'},
                            'descricao': {'type': 'string'}
                        }
                    }
                }
            }
        }
    })
    def listar_tarefas():
        tarefas = Tarefa.query.all()
        current_app.logger.info(f"{len(tarefas)} tarefas listadas")
        return jsonify(TarefaResource.tarefas_schema.dump(tarefas))

    @staticmethod
    @api.route('/tarefas/<int:tarefa_id>/', methods=['GET'])
    @jwt_required()
    @swag_from({
        'tags': ['Tarefas'],
        'summary': 'Obtém uma tarefa específica',
        'description': 'Endpoint para obter uma tarefa pelo ID.',
        'parameters': [
            {
                'name': 'tarefa_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID da tarefa'
            }
        ],
        'responses': {
            200: {
                'description': 'Tarefa encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'titulo': {'type': 'string'},
                        'descricao': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Tarefa não encontrada'
            }
        }
    })
    def obter_tarefa(tarefa_id):
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        current_app.logger.info(f"Tarefa obtida com ID: {tarefa.id}")
        return jsonify(TarefaResource.tarefa_schema.dump(tarefa))

    @staticmethod
    @api.route('/tarefas/<int:tarefa_id>/', methods=['PUT'])
    @jwt_required()
    @swag_from({
        'tags': ['Tarefas'],
        'summary': 'Atualiza uma tarefa',
        'description': 'Endpoint para atualizar uma tarefa existente pelo ID.',
        'parameters': [
            {
                'name': 'tarefa_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID da tarefa'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'titulo': {'type': 'string'},
                        'descricao': {'type': 'string'},
                        'concluida': {'type': 'boolean'}
                    },
                    'example': {
                        'titulo': 'Título atualizado',
                        'descricao': 'Descrição atualizada',
                        'concluida': True
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Tarefa atualizada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'titulo': {'type': 'string'},
                        'descricao': {'type': 'string'},
                        'concluida': {'type': 'boolean'}
                    }
                }
            },
            404: {
                'description': 'Tarefa não encontrada'
            }
        }
    })
    def atualizar_tarefa(tarefa_id):
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        data = request.json
        tarefa_data = TarefaResource.tarefa_schema.load(data, partial=True)
        tarefa.titulo = tarefa_data.get('titulo', tarefa.titulo)
        tarefa.descricao = tarefa_data.get('descricao', tarefa.descricao)
        tarefa.concluida = tarefa_data.get('concluida', tarefa.concluida)
        db.session.commit()

        current_app.logger.info(f"Tarefa atualizada com ID: {tarefa.id}")
        return jsonify(TarefaResource.tarefa_schema.dump(tarefa))

    @staticmethod
    @api.route('/tarefas/<int:tarefa_id>/', methods=['DELETE'])
    @jwt_required()
    @swag_from({
        'tags': ['Tarefas'],
        'summary': 'Deleta uma tarefa',
        'description': 'Endpoint para deletar uma tarefa existente pelo ID.',
        'parameters': [
            {
                'name': 'tarefa_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID da tarefa'
            }
        ],
        'responses': {
            204: {
                'description': 'Tarefa deletada com sucesso'
            },
            404: {
                'description': 'Tarefa não encontrada'
            }
        }
    })
    def deletar_tarefa(tarefa_id):
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        db.session.delete(tarefa)
        db.session.commit()

        current_app.logger.info(f"Tarefa deletada com ID: {tarefa.id}")
        return jsonify({"message": "Tarefa deletada com sucesso"}), 204
