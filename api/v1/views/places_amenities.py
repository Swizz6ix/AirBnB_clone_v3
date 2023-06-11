#!/usr/bin/python3
""" Flask route that returns json status response. """
from os import getenv
from api.v1.views import app_views
from flask import abort, make_response, request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=['GET'], strict_slashes=False)
def amenities_per_place(place_id):
    """ Amenities route that handles http requested per place """
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenity_objects = place_obj.amenities
        else:
            amenity_objects = place_obj.amenity_ids
        place_amenities = [obj.to_dict() for obj in amenity_objects.values()]
        return jsonify(place_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['DELETE', 'POST'])
def amenities_to_place(place_id=None, amenities_id=None):
    """ Ammenities route that handles http requested per place and per amenity. """
    place_obj = storage.get('Place', place_id)
    amenity_id = storage.get('Amenity', amenity_id)
    if place_obj is None or amenity_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)
    
    if request.method == 'DELETE':
        if (amenity_obj not in place_obj.amenities and amenity_obj.id not in place_obj.amenities):
            abort(404, 'Not found')
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = place_obj.amenities
        else:
            place_amenities = place_obj.amenity_ids
        place_amenities.remove(amenity_obj)
        place_obj.save()
        return (jsonify({}), 200)

    if request.method == 'POST':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = place_obj.amenties
        else:
            place_amenities = place_obj.amenity_ids
        if amenity_obj in place_amenities:
            return jsonify(amenity_obj.to_dict())
        place_amenities.append(amenity_obj)
        place.save()
        return make_response(jsonify(amenity_obj.to_dict()), 201)