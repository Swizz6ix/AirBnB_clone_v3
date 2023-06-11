#!/usr/bin/python3
""" Flask route that returns json response """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
def amenities_no_id():
    """ amenties route that handles http request no ID given """
    if request.method == 'GET':
        all_amenities = storage.all('Amenity')
        all_amenities = [obj.to_dict() for obj in all_amenities.values()]
        return jsonify(all_amenities)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        new_object = Amenity(**req_json)
        new_object.save()
        return (jsonify(new_object.to_dict()), 201)

    
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities_with_id(amenity_id=None):
    """ Amenities route to handle http methods for requested amenity by id"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        amenity_obj.delete()
        del amenity_obj
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in req_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenity_obj, attr, val)
        amenity_obj.save()
        return (jsonify(amenity_obj.to_dict()), 200)