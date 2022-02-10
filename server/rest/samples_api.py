from flask import Response, request
from db.models import  SecondaryOrganism
from flask_restful import Resource
from errors import NotFound,SchemaValidationError,RecordAlreadyExistError
from services import sample_service
import services.submission_service as service
from flask_jwt_extended import jwt_required
from mongoengine.queryset.visitor import Q
from flask import current_app as app
from utils.constants import SamplePipeline
import json

#CRUD operations on sample
class SamplesApi(Resource):

    def get(self,accession=None):
        sample = SecondaryOrganism.objects((Q(accession=accession) | Q(sample_unique_name=accession)))
        if len(sample) > 0:
            result = sample.aggregate(*SamplePipeline).next()
            return Response(json.dumps(result),mimetype="application/json", status=200)
        else:
            raise NotFound

    @jwt_required()
    def delete(self):
        data = request.json if request.is_json else request.form
        if not data:
            raise SchemaValidationError
        else:
            sample_service.delete_samples(data)

    @jwt_required()
    def put(self,accession):
        data = request.json if request.is_json else request.form
        app.logger.info('HELLOOOO')
        sample = SecondaryOrganism.objects((Q(accession=accession) | Q(sample_unique_name=accession))).first()
        if not sample:
            raise NotFound
        else:
            sample.update(**data)
        if sample.accession:
            id = sample.accession
        else:
            id = sample.sample_unique_name
        return Response(json.dumps(f'sample with id {id} has been saved'),mimetype="application/json", status=200)
		#update sample


    @jwt_required()
    def post(self):
        ## TODO add metadata validation for different clients
        # SecondaryOrganism._get_collection().drop_index('accession_1')
        data = request.json if request.is_json else request.form
        if all (k in data.keys() for k in ("taxid","metadata")) and 'sample_unique_name' in data['metadata'].keys():
            specimen_id= data['metadata']['sample_unique_name']
            if SecondaryOrganism.objects(specimen_id=specimen_id).first():
                raise RecordAlreadyExistError
            else:
                sample = service.create_sample(data)
                return Response(json.dumps(f'sample with id {sample.sample_unique_name} has been saved'),mimetype="application/json", status=200)
        else:
            raise SchemaValidationError
   

		#update sample

	
		# if not sample:
		# 	raise NotFound
##endpoint to retrieve checklist fields