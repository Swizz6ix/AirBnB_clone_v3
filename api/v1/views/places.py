#!/usr/bin/python3
""" Flask route that returns json response """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from os import getenv


@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'], strict_slashes=False)
def palces_per_city(city_id):
    """ Places route that handles http request no id given """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        all_places = storage.all("Place")
        city_places = [obj.to_dict() for obj in all_places.values()
                        if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404, "Not found")
        if req_json.get("name") is None:
            abort(404, 'Missing name')
        req_json['city_id'] = city_id
        new_object = Place(**req_json)
        new_object.save()
        return (jsonify(new_object.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places_with_id(place_id=None):
    """ Users route to handle http methods for requested user by id """
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        place_obj.delete()
        del place_obj
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in req_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(place_obj, attr, val)
        place_obj.save()
        return (jsonify(place_obj.to_dict()), 200)


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """ Places route to handle http method for request to search places. """
    all_places = [place for place in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([city_id for city_id in cities
                        if storage.get('City', city_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [place for place in all_places
                        if place.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_dict() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([amenity_id for amenity_id in amenities
                            if storage.get('Amenity', amenity_id)])
        for place in all_places:
            place_amenities = None
            if getenv('HBNB_TYPE_STORAGE') == 'db' and place.amenities:
                place_amenities = [amenity.id for amenity in place.amenities]
            elif len(place.amenities) > 0:
                place_amenities = place.amenities
            if place_amenities and all([amenity in place_amenities for amenity in amenities]):
                places_amenities.append(place)
    else:
        places_amenities = all_places
    result = [place.to_dict() for place in places_amenities]
    return jsonify(result)