from app.api import bp
from app.models import User, Post
from app import db
from flask import jsonify, request, url_for, g

from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/users/<int:id>/posts', methods=["GET"])
@token_auth.login_required
def get_posts(id):
    user = User.query.get_or_404(id)
    posts = Post.to_collection(user.posts)
    return jsonify({'posts':posts})

@bp.route("/users/post", methods=["POST"])
@token_auth.login_required
def create_post():
    data = request.get_json() or {}
    if 'body' not in data:
        return bad_request("must include body")
    post = Post(body=data['body'], author=g.current_user)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict())

@bp.route('/users/<int:id>', methods=["GET"])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=["GET"])
@token_auth.login_required
def get_users():
    return jsonify(User.to_collection(User.query))

@bp.route('/users', methods=["POST"])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>/followers', methods=["GET"])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    return jsonify(User.to_collection(user.followers))

@bp.route('/users/<int:id>/followed', methods=["GET"])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    return jsonify(User.to_collection(user.followed))

@bp.route('/users/<int:id>', methods=["PUT"])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())