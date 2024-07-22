from marshmallow import Schema, fields, validate

class CalculateDistancesSerializer(Schema):
    file = fields.Raw(required=True)

class GetResultSerializer(Schema):
    task_id = fields.UUID(required=True)

class TaskResultSchema(Schema):
    task_id = fields.UUID(required=True)
    status = fields.Str(required=True)
    data = fields.Dict(required=True)
