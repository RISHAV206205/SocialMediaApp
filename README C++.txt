SocialFeed - Social Media Web Application
=========================================

STUDENT INFORMATION:
Name: [Your Full Name Here]
Email: [Your Vanderbilt Email Here]

PROJECT OVERVIEW:
This is a social media web application built for the Change++ coding challenge. 
The app allows users to login with Google, create posts, like/comment on posts, 
react with emojis, and browse news from multiple categories including general news, 
technology, sports, finance, and entertainment.

FEATURES:
- Google OAuth authentication
- Create, view, like, and comment on posts
- Emoji reactions (like, love, laugh, wow, sad, angry)
- Real-time news aggregation from multiple sources
- Responsive design that works on mobile and desktop
- News categories: General, Technology, Sports, Finance, Entertainment
- Market data integration for financial news
- User profiles with post history
- Clean, modern dark theme interface

TECHNOLOGY STACK:
Backend:
- Flask (Python web framework)
- Flask-Login (user session management)
- OAuthlib (Google authentication)
- Requests (API calls)
- JSON file storage for data persistence

Frontend:
- HTML5 with Jinja2 templating
- Bootstrap 5 with Replit dark theme
- Font Awesome icons
- Vanilla JavaScript
- Responsive design

APIs Used:
- Google OAuth API (authentication)
- NewsAPI (general, tech, sports, entertainment news)
- Alpha Vantage API (financial data)

SETUP INSTRUCTIONS:
1. Environment Variables Required:
   - GOOGLE_OAUTH_CLIENT_ID: Your Google OAuth client ID
   - GOOGLE_OAUTH_CLIENT_SECRET: Your Google OAuth client secret
   - NEWS_API_KEY: Your NewsAPI key (get from newsapi.org)
   - ALPHA_VANTAGE_API_KEY: Your Alpha Vantage key (get from alphavantage.co)
   - SESSION_SECRET: A random secret key for sessions

2. Google OAuth Setup:
   - Go to https://console.cloud.google.com/apis/credentials
   - Create a new OAuth 2.0 Client ID
   - Add your domain/callback URL to Authorized redirect URIs
   - Format: https://YOUR-DOMAIN/google_login/callback

3. Running the Application:
   - Run: python main.py
   - The app will start on http://0.0.0.0:5000
   - Access it through your web browser

4. Data Storage:
   - User data is stored in data/users.json
   - Posts and comments are stored in data/posts.json
   - Data files are created automatically when first needed

USAGE:
1. Visit the application URL
2. Click "Login with Google" to authenticate
3. Browse news feeds or create posts
4. Like, comment, and react to posts
5. Visit your profile to see your post history

REFLECTION:
This project was an excellent opportunity to learn full-stack web development 
with Flask and modern web technologies. I learned how to integrate OAuth 
authentication, work with external APIs, and create a responsive user interface. 
The most challenging part was integrating multiple news APIs and handling error 
cases gracefully. I reinforced my understanding of RESTful API design and 
gained experience with JSON data storage. The project helped me understand 
how social media applications work under the hood and the importance of 
user experience design.

FEEDBACK:
The coding challenge was well-structured and provided clear requirements. 
The scoring rubric helped prioritize features effectively. It would be helpful 
to have more guidance on API rate limits and error handling best practices. 
The workshops and office hours were valuable for getting started with the project.

BONUS FEATURES IMPLEMENTED:
- Emoji reaction system beyond basic likes
- News aggregation from multiple sources with real-time updates
- Market data integration for financial news
- Responsive design that works well on mobile devices
- User profile pages with post history
- Toast notifications for user feedback
- Keyboard shortcuts for better UX
- Auto-resizing textareas
- Share news articles as posts feature

DEPLOYMENT:
The application is designed to run on Replit or any Flask-compatible hosting 
platform. All dependencies are included and the app binds to 0.0.0.0:5000 
as required for external access.

SECURITY CONSIDERATIONS:
- Google OAuth provides secure authentication
- Session management with secure secret keys
- Input validation on all user inputs
- Error handling to prevent information disclosure
- No SQL injection risks (using JSON file storage)
- XSS prevention through Jinja2 template escaping

This application demonstrates a complete social media platform with modern 
features while maintaining simplicity and ease of use.
