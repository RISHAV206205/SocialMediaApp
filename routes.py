from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Post, Comment
from data_store import save_post, get_all_posts, get_post_by_id, save_comment
from news_service import get_news_by_category
import uuid
from datetime import datetime

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/")
def index():
    """Main social media feed"""
    posts = get_all_posts()
    # Sort posts by timestamp (newest first)
    posts.sort(key=lambda x: x.timestamp, reverse=True)
    return render_template("index.html", posts=posts)

@main_routes.route("/news")
def news():
    """News aggregation page"""
    category = request.args.get('category', 'general')
    news_data = get_news_by_category(category)
    return render_template("news.html", news_data=news_data, category=category)

@main_routes.route("/profile")
@login_required
def profile():
    """User profile page"""
    user_posts = [post for post in get_all_posts() if post.user_id == current_user.id]
    user_posts.sort(key=lambda x: x.timestamp, reverse=True)
    return render_template("profile.html", posts=user_posts)

@main_routes.route("/api/posts", methods=["POST"])
@login_required
def create_post():
    """API endpoint to create a new post"""
    try:
        content = request.json.get("content", "").strip()
        if not content:
            return jsonify({"error": "Post content cannot be empty"}), 400
        
        post_id = str(uuid.uuid4())
        post = Post(
            id=post_id,
            user_id=current_user.id,
            username=current_user.username,
            content=content
        )
        
        save_post(post)
        return jsonify({
            "success": True,
            "post": post.to_dict()
        })
    
    except Exception as e:
        return jsonify({"error": "Failed to create post"}), 500

@main_routes.route("/api/posts/<post_id>/like", methods=["POST"])
@login_required
def toggle_like(post_id):
    """API endpoint to like/unlike a post"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        if current_user.id in post.likes:
            post.likes.remove(current_user.id)
            liked = False
        else:
            post.likes.append(current_user.id)
            liked = True
        
        save_post(post)
        return jsonify({
            "success": True,
            "liked": liked,
            "like_count": len(post.likes)
        })
    
    except Exception as e:
        return jsonify({"error": "Failed to toggle like"}), 500

@main_routes.route("/api/posts/<post_id>/react", methods=["POST"])
@login_required
def add_reaction(post_id):
    """API endpoint to add reaction to a post"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        reaction_type = request.json.get("reaction")
        if reaction_type not in post.reactions:
            return jsonify({"error": "Invalid reaction type"}), 400
        
        # Remove user from all reaction types first
        for reaction_list in post.reactions.values():
            if current_user.id in reaction_list:
                reaction_list.remove(current_user.id)
        
        # Add user to the selected reaction
        post.reactions[reaction_type].append(current_user.id)
        
        save_post(post)
        return jsonify({
            "success": True,
            "reactions": {k: len(v) for k, v in post.reactions.items()}
        })
    
    except Exception as e:
        return jsonify({"error": "Failed to add reaction"}), 500

@main_routes.route("/api/posts/<post_id>/comments", methods=["POST"])
@login_required
def add_comment(post_id):
    """API endpoint to add a comment to a post"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        content = request.json.get("content", "").strip()
        if not content:
            return jsonify({"error": "Comment content cannot be empty"}), 400
        
        comment_id = str(uuid.uuid4())
        comment = Comment(
            id=comment_id,
            post_id=post_id,
            user_id=current_user.id,
            username=current_user.username,
            content=content
        )
        
        post.comments.append(comment.to_dict())
        save_post(post)
        
        return jsonify({
            "success": True,
            "comment": comment.to_dict()
        })
    
    except Exception as e:
        return jsonify({"error": "Failed to add comment"}), 500

@main_routes.route("/api/news/<category>")
def get_news_api(category):
    """API endpoint to get news by category"""
    try:
        news_data = get_news_by_category(category)
        return jsonify(news_data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch news"}), 500
