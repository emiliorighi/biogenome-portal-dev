import services.search_service as service
import services.organisms_service as organism_service
from flask import Response, request
from db.models import Organism
from flask_restful import Resource
from errors import NotFound, SchemaValidationError
import json
from flask_jwt_extended import jwt_required
from utils.constants import OrganismPipeline
from utils.utils import sort_lineage
from flask import current_app as app
import base64


class OrganismsApi(Resource):
	def get(self):
		return Response(service.default_query_params(request.args,Organism),mimetype="application/json", status=200)
	
	@jwt_required()
	def delete(self):
		if 'tax_ids' in request.args.keys() and len(request.args['tax_ids'].split(',')) > 0:
			taxids = request.args['tax_ids'].split(',')
			deleted_taxons = organism_service.delete_organisms(taxids)
			return Response(json.dumps(deleted_taxons),mimetype="application/json", status=200)
		else:
			raise SchemaValidationError

class OrganismsSearchApi(Resource):
	def get(self):
		return Response(service.full_text_search(request.args,Organism),mimetype="application/json", status=200)

class OrganismApi(Resource):
	def get(self,name):
		organism_obj = Organism.objects(organism=name)
		if organism_obj.count() == 0:
			raise NotFound
		organism_response = organism_obj.aggregate(*OrganismPipeline).next()
		if 'image' in organism_response.keys():
			encoded_image = base64.b64encode(organism_obj.first().image.read())
			organism_response['image'] = encoded_image.decode('utf-8')
		sort_lineage(organism_response['taxon_lineage']) #sort lineage (aggregation pipeline returns unordered list)
		return Response(json.dumps(organism_response),mimetype="application/json", status=200)

	@jwt_required()
	def post(self,name):
		organism = Organism.objects(organism=name).first()
		if not organism:
			raise NotFound
		if request.form:
			if 'delete_image' in request.form.keys():
				organism.image.delete()
			if 'image' in request.files.keys():
				if organism.image:
					organism.image.replace(request.files['image'], content_type = 'image/jpeg')
				else:
					organism.image.put(request.files['image'], content_type = 'image/jpeg')
			if 'image_url' in request.form.keys():
				organism.image_url = request.form['image_url']
			if 'common_name' in request.form.keys():
				common_names = request.form['common_name'].split(',')
				organism.common_name = (common_names)
			organism.save()
		else:
			raise SchemaValidationError	# organism.common_name.extend


