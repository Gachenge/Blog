from flask import Blueprint, jsonify, request
from oauth.utils import login_is_required
from oauth.models.users import Users

users = Blueprint('users', __name__, url_prefix='/api/user')

@login_is_required
@users.route("/all")
def all_user():
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

@login_is_required
@users.route("/<string:user_id>", methods=['GET', 'PATCH', 'DELETE'])
def user_by_id(user_id):
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
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                return jsonify({"message": f"Attribute '{key}' is not valid"}), 400

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

    return jsonify({"message": "Method not allowed"}), 405
