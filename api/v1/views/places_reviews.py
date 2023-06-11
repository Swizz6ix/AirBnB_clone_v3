#!/usr/bin/python3
""" Flask route that returns json response """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'], strict_slashes=False)
def reviews_per_place(place_id):
    """ Reviews route that handles http requested per place """
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        all_reviews = storage.all("Review")
        place_reviews = [obj.to_dict() for obj in all_places.values()
                        if obj.place_id == place_id]
        return jsonify(place_reviews)

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
        if req_json.get("text") is None:
            abort(404, 'Missing text')
        req_json['place_id'] = place_id
        new_object = Review(**req_json)
        new_object.save()
        return (jsonify(new_object.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews_with_id(review_id=None):
    """ Reviews route to handle http methods for requested review by id """
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj.delete()
        del review_obj
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in req_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(review_obj, attr, val)
        review_obj.save()
        return (jsonify(review_obj.to_dict()), 200)