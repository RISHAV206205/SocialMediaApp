import sys
import os

# Add the parent directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# This is the WSGI application that Vercel will call
application = app

# For Vercel serverless functions
def handler(request, response):
    return app