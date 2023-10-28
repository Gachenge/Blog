from flask import Blueprint, jsonify, request
from blog.utils import login_is_required, get_user
from blog import db
from blog.models.posts import Posts
from blog.models.users import Users
from blog.models.comment import Comment

comment_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comment_bp.route('/posts/<string:post_id>/comments')
@login_is_required
def post_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_data = []
    for comment in comments:
        user = Users.query.get(comment.user_id)
        comment_info = {
            "user_image": user.avatar,
            "comment": comment.text,
        }
        comment_data.append(comment_info)
    return jsonify({"Comments": comment_data})


@comment_bp.route('/<string:comment_id>', methods=['GET', 'PATCH', 'DELETE'])
@login_is_required
def comment_by_id(comment_id):
    comment = Comment.query.filter_by(comment_id).first()
    if comment is None:
        return jsonify({"Error": "Comment not found"}), 404

    user = Users.query.get(comment.user_id)


    if request.method == 'GET':
        comment_info = {
            "user_image": user.avatar,
            "comment": comment.text
        }
        return jsonify({"Comment": comment_info})

    if request.method == 'PATCH':
        data = request.get_json()
        for key, val in data.items():
            if key == 'text':
                comment.text = val
            else:
                return jsonify({"Error": f"You are not allowed to change '{key}'"}), 400

        db.session.commit()
        return jsonify({"message": "Post updated successfully"}), 200

    if request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment deleted successfully"}), 200

    return jsonify({"Error": "Method not allowed"}), 405


@comment_bp.route('/post/<string:post_id>/comment', methods=['POST'])
@login_is_required
def create_comment(post_id):
    data = request.get_json()
    if 'text' not in data or data['text'] is None or data['text'] == "":
        return jsonify({"Error": "A post must have a text"}), 400

    user = get_user()
    
    comment = Comment(user_id=user.id, post_id=post_id, image_url=data.get('image'), text=data['text'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment made successfully"}), 200
