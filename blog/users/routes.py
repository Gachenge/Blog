from flask import Blueprint, jsonify, request
from blog.utils import login_is_required
from blog.models.users import Users
from blog import db

user_bp = Blueprint('users', __name__, url_prefix='/api/user')


@user_bp.route("/all")
@login_is_required
def all_users():
    """Returns all users registered."""
    users = Users.query.all()
    user_data = []
    for user in users:
        user_info = {
            'avatar': user.avatar,
            'name': user.name,
            'email': user.email
        }
        user_data.append(user_info)
    return jsonify({"Users": user_data}), 200


@user_bp.route("/<string:user_id>", methods=['GET', 'PATCH', 'DELETE'])
@login_is_required
def user_by_id(user_id):
    """Allows operations on one user by their id."""
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if request.method == 'GET':
        user_info = {
            'avatar': user.avatar,
            'name': user.name,
            'email': user.email
        }
        return jsonify({"User": user_info}), 200

    if request.method == 'PATCH':
        data = request.get_json()
        allowed_attributes = ['name', 'email', 'avatar']  # List of allowed attributes to update

        for key, value in data.items():
            if key in allowed_attributes:
                setattr(post, key, value)
            else:
                return jsonify({"Error": f"You are not allowed to change '{key}'"}), 400

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

    return jsonify({"message": "Method not allowed"}), 405
