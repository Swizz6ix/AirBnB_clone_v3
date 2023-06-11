#!/usr/bin/python3
""" Flask route that returns json response """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
# from flasgger import Swagger, swag_from
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
# @swag_from('swagger_yaml/states_no_id.yml', methods=['GET', 'POST'])
def states_no_id():
    """ State route to handle http method for requested states no id provided. """
    if request.method == 'GET':
        all_states = storage.all('State')
        all_states = list(obj.to_dict() for obj in all_states.values())
        return jsonify(all_states)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if req_json.get("name") is None:
            abort(400, "Missing name")
        # state = storage("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
# @swag_from('swagger_yaml/states_id.yaml', methods=['PUT', 'GET', 'DELETE'])
def states_with_id(state_id=None):
    """ States route to handle http method for requested state by id """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        del state_obj
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in req_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state_obj, attr, val)
        state_obj.save()
        return jsonify(state_obj.to_dict()), 200