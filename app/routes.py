from . import bp as blog
from app.blueprints.auth.http_auth import token_auth
from flask import jsonify, request
from .models import Post


# Create a blog post
@blog.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Please send a body'}), 400
    data = request.json
    # Validate the data
    for field in ['title', 'content']:
        if field not in data:
            return jsonify({'error': f"You are missing the {field} field"}), 400
    current_user = token_auth.current_user()
    data['user_id'] = current_user.id
    new_post = Post(**data)
    return jsonify(new_post.to_dict()), 201


# Get all posts
@blog.route('/posts')
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


# Get a single post with id
@blog.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


# Update a single post with id
@blog.route('/posts/<int:post_id>', methods=['PUT'])
@token_auth.login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = token_auth.current_user()
    if user.id != post.user_id:
        return jsonify({'error': 'You are not allowed to edit this post'}), 403
    data = request.json
    post.update(data)
    return jsonify(post.to_dict())


# Delete a single post with id
@blog.route('/posts/<int:post_id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = token_auth.current_user()
    if user.id != post.user_id:
        return jsonify({'error': 'You are not allowed to edit this post'}), 403
    post.delete()
    return jsonify({'success': f'{post.title} has been deleted'})
    