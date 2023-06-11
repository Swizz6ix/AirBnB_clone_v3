#!/usr/bin/python3
""" Flask route that returns json response """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route("/user", methods=['GET', 'POST'], strict_slashes=False)
def users_no_id():
    """ users route that handles http request no id given """
    if request.method == 'GET':
        all_users = storage.all("User")
        all_users = [obj.to_dict() for obj in all_users.values()]
        return jsonify(all_users)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        new_object = User(**req_json)
        new_object.save()
        return (jsonify(new_object.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users_with_id(user_id=None):
    """ Users route to handle http methods for requested user by id """
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 400)

    if request.method == 'GET':
        return jsonify(user_id.to_dict())

    if request.method == 'DELETE':
        user_obj.delete()
        del user_obj
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in req_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(user_obj, attr, val)
        user_obj.save()
        return (jsonify(user_obj.to_dict()), 200)