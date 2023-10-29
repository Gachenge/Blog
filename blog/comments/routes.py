from flask import Blueprint, jsonify, request
from blog.utils import login_is_required, get_user
from blog import db
from blog.models.posts import Posts
from blog.models.users import Users
from blog.models.comment import Comment

comment_bp = Blueprint('comments', __name__, url_prefix='/api/comments')


@comment_bp.route('/<string:comment_id>', methods=['GET', 'PATCH', 'DELETE'])
@login_is_required
def comment_by_id(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({"Error": "Comment not found"}), 404

    user = Users.query.get(comment.user_id)


    if request.method == 'GET':
        comment_info = {
            "Author": user.name,
            "user_image": user.avatar,
            "comment": comment.text
        }
        return jsonify({"Comment": comment_info})

    if request.method == 'PATCH':
        data = request.get_json()
        for key, val in data.items():
            if key == 'text' or key == 'image':
                setattr(comment, key, val)
            else:
                return jsonify({"Error": f"You are not allowed to change '{key}'"}), 400

        db.session.commit()
        return jsonify({"message": "Post updated successfully"}), 200

    if request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment deleted successfully"}), 200

    return jsonify({"Error": "Method not allowed"}), 405

