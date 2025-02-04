#!/usr/bin/python3
"""The following script handles all default RestFul API
actions for Place - Amenity"""

from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import abort, jsonify, make_response, request


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_by_place(place_id):
    """
    This method retrieves the list of all Amenity objects of a Place
    Args:
        place_id (str): The ID of the Place.
    Returns:
        JSON: List of dictionaries representing Amenity objects.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleting_place_amenity(place_id, amenity_id):
    """
    This method deletes a Amenity object of a Place
    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity.
    Returns:
        JSON: Empty dictionary with 200 status code.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """
    This method links a Amenity object to a place

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity.

    Returns:
        JSON: Dictionary representing the linked Amenity object.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
