from flask import Blueprint, jsonify, request
from blog.utils import login_is_required, get_user
from blog import db
from blog.models.posts import Posts
from blog.models.users import Users

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route("/all")
@login_is_required
def all_posts():
    """Returns all posts with user information"""
    posts = Posts.query.all()
    post_data = []

    for post in posts:
        user = Users.query.get(post.user_id)
        post_info = {
            "Author": user.name,
            "Body": post.body,
            "Image": post.image_url
        }
        post_data.append(post_info)

    return jsonify({"Posts": post_data})


@posts_bp.route("/user/<string:user_id>")
@login_is_required
def user_posts(user_id):
    """Returns all posts by a particular user"""
    user = Users.query.get(user_id)  # Retrieve the user by user_id
    if user is None:
        return jsonify({"error": "User not found"}), 404

    posts = Posts.query.filter_by(user_id=user_id).all()  # Filter posts by user_id

    post_data = []

    for post in posts:
        post_info = {
            "Author": user.name,
            "Body": post.body,
            "Image": post.image_url
        }
        post_data.append(post_info)

    return jsonify({"Posts": post_data})


@posts_bp.route("/<string:post_id>", methods=['GET', 'PATCH', 'DELETE'])
@login_is_required
def post_by_id(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({"message": "Post not found"}), 404

    user = Users.query.get(post.user_id)

    if request.method == 'GET':
        post_info = {
            "Author": user.name,
            "Post": post.body,
            "Image": post.image_url
        }
        return jsonify({"Post": post_info})

    if request.method == 'PATCH':
        data = request.get_json()
        allowed_attributes = ['body', 'image_url']  # List of allowed attributes to update

        for key, value in data.items():
            if key in allowed_attributes:
                setattr(post, key, value)
            else:
                return jsonify({"Error": f"You are not allowed to change '{key}'"}), 400

        db.session.commit()
        return jsonify({"message": "Post updated successfully"}), 200

    if request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted successfully"}), 200

    return jsonify({"message": "Method not allowed"}), 405


@posts_bp.route("/create", methods=['POST'])
@login_is_required
def create_post():
    data = request.get_json()

    # Check if the 'body' field is provided and not empty
    if 'body' not in data or data['body'] is None or data['body'] == "":
        return jsonify({"Error": "A post must have a body"}), 400
    
    user = get_user()

    # Create a new post
    post = Posts(user_id=user.id, body=data.get('body'), image_url=data.get('image'))
    db.session.add(post)
    db.session.commit()

    return jsonify({"Message": "Post created successfully"}), 200

