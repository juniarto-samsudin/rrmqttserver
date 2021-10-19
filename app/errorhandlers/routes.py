from app.errorhandlers import blueprint 
from flask import Response
import json

@blueprint.app_errorhandler(400)
def handle_400(err):
    response_dict={"status":"Required JSON key not available"}
    return Response(json.dumps(response_dict), status=400, mimetype="application/json")

@blueprint.app_errorhandler(500)
def handle_500(err):
    return "five oh oh"

@blueprint.app_errorhandler(503)
def handle_503(err):
    return Response(status=503, mimetype="application/json")