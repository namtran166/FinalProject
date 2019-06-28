from flask import Blueprint, jsonify, request

from main.models.category import CategoryModel
from main.schemas.category import CategorySchema
from main.utils.exception import BadRequestError
from main.utils.validation import error_checking, validate_input

bp_category = Blueprint("category", __name__, url_prefix="/categories")


@bp_category.route("", methods=['GET'])
@error_checking
def get_categories():
    categories = CategoryModel.query.all()
    return jsonify(CategorySchema(many=True).dump(categories).data), 200


@bp_category.route("/<int:category_id>", methods=['GET'])
@error_checking
def get_category(category_id):
    category = validate_input(category_id=category_id)
    return jsonify(CategorySchema().dump(category).data), 200


@bp_category.route("", methods=['POST'])
@error_checking
def create_category():
    data = CategorySchema().load(request.get_json()).data

    if CategoryModel.find_by_name(data["name"]):
        raise BadRequestError("Category already exists.")

    category = CategoryModel(**data)
    category.save_to_db()
    return jsonify(CategorySchema().dump(category).data), 201
