import json
import os
from models import User, Post, Comment
from datetime import datetime

# Data file paths
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
POSTS_FILE = os.path.join(DATA_DIR, "posts.json")

def ensure_data_directory():
    """Ensure data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_users():
    """Load users from JSON file"""
    ensure_data_directory()
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users_data = json.load(f)
                return [User.from_dict(user) for user in users_data]
        return []
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

def save_users(users):
    """Save users to JSON file"""
    ensure_data_directory()
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump([user.to_dict() for user in users], f, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")

def save_user(user):
    """Save a single user"""
    users = load_users()
    
    if user is None:
        return users
    
    # Check if user already exists
    existing_user_index = None
    for i, existing_user in enumerate(users):
        if existing_user.id == user.id:
            existing_user_index = i
            break
    
    if existing_user_index is not None:
        users[existing_user_index] = user
    else:
        users.append(user)
    
    save_users(users)
    return users

def get_user_by_id(user_id):
    """Get user by ID"""
    users = load_users()
    for user in users:
        if str(user.id) == str(user_id):
            return user
    return None

def get_user_by_username(username):
    """Get user by username"""
    users = load_users()
    for user in users:
        if user.username == username:
            return user
    return None

def load_posts():
    """Load posts from JSON file"""
    ensure_data_directory()
    try:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as f:
                posts_data = json.load(f)
                return [Post.from_dict(post) for post in posts_data]
        return []
    except Exception as e:
        print(f"Error loading posts: {e}")
        return []

def save_posts(posts):
    """Save posts to JSON file"""
    ensure_data_directory()
    try:
        with open(POSTS_FILE, 'w') as f:
            json.dump([post.to_dict() for post in posts], f, indent=2)
    except Exception as e:
        print(f"Error saving posts: {e}")

def save_post(post):
    """Save a single post"""
    posts = load_posts()
    
    # Check if post already exists
    existing_post_index = None
    for i, existing_post in enumerate(posts):
        if existing_post.id == post.id:
            existing_post_index = i
            break
    
    if existing_post_index is not None:
        posts[existing_post_index] = post
    else:
        posts.append(post)
    
    save_posts(posts)

def get_all_posts():
    """Get all posts"""
    return load_posts()

def get_post_by_id(post_id):
    """Get post by ID"""
    posts = load_posts()
    for post in posts:
        if post.id == post_id:
            return post
    return None

def save_comment(comment):
    """Save a comment (this is handled within posts)"""
    # Comments are saved as part of posts
    pass
