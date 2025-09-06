from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User
from data_store import save_user, get_user_by_username, load_users
import uuid

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Please enter both username and password", "error")
            return render_template("login.html")
        
        user = get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("main_routes.index"))
        else:
            flash("Invalid username or password", "error")
    
    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        
        # Validate inputs
        if not username or not password or not confirm_password:
            flash("All fields are required", "error")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("register.html")
        
        # Validate username format
        is_valid, message = User.validate_username(username)
        if not is_valid:
            flash(message, "error")
            return render_template("register.html")
        
        # Check if username already exists
        if get_user_by_username(username):
            flash("Username already exists", "error")
            return render_template("register.html")
        
        # Create new user
        users = load_users()
        user_id = len(users) + 1
        user = User(user_id, username)
        user.set_password(password)
        
        save_user(user)
        login_user(user)
        
        flash(f"Account created successfully! Welcome, {username}!", "success")
        return redirect(url_for("main_routes.index"))
    
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("main_routes.index"))