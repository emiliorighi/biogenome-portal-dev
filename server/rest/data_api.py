from flask_restful import Resource
from flask import Response, request
from services.data_service import get_data
from errors import SchemaValidationError
from flask import current_app as app


class OrganismData(Resource):
    def post(self, model):
        if request.is_json and 'ids' in request.json.keys(): 
            ids = request.json['ids']
        elif request.form and 'ids' in request.form.keys():
            ids = request.form
        else:
            raise SchemaValidationError
        return Response(get_data(model,ids), mimetype="application/json", status=201)
