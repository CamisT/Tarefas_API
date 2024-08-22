from marshmallow import Schema, fields

class TarefaSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    descricao = fields.Str()
    concluida = fields.Bool()
    data_criacao = fields.DateTime(dump_only=True)
    data_inicio = fields.DateTime(required=True)  # Adicionados os campos de data e hora
    data_fim = fields.DateTime(required=True)
