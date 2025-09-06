from flask_login import UserMixin
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(UserMixin):
    def __init__(self, id, username, password_hash=None, profile_picture=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.profile_picture = profile_picture
        self.created_at = datetime.now().isoformat()
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def validate_username(username):
        """Validate username: 6+ characters, 1 number, 1 exclamation mark"""
        if len(username) < 6:
            return False, "Username must be at least 6 characters long"
        
        if not re.search(r'\d', username):
            return False, "Username must contain at least one number"
        
        if '!' not in username:
            return False, "Username must contain at least one exclamation mark (!)"
        
        return True, "Valid username"

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['id'], data['username'], data.get('password_hash'), data.get('profile_picture'))
        user.created_at = data.get('created_at', datetime.now().isoformat())
        return user

class Post:
    def __init__(self, id, user_id, username, content, timestamp=None, likes=None, comments=None, reactions=None):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()
        self.likes = likes or []
        self.comments = comments or []
        self.reactions = reactions or {
            'like': [],
            'love': [],
            'laugh': [],
            'wow': [],
            'angry': [],
            'sad': []
        }

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp,
            'likes': self.likes,
            'comments': self.comments,
            'reactions': self.reactions
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['user_id'],
            data['username'],
            data['content'],
            data.get('timestamp'),
            data.get('likes', []),
            data.get('comments', []),
            data.get('reactions', {
                'like': [], 'love': [], 'laugh': [], 
                'wow': [], 'angry': [], 'sad': []
            })
        )

class Comment:
    def __init__(self, id, post_id, user_id, username, content, timestamp=None):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.username = username
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['post_id'],
            data['user_id'],
            data['username'],
            data['content'],
            data.get('timestamp')
        )
