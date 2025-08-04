from flask import Flask, render_template, session, request, redirect, url_for, flash
from azure_auth import AzureADAuth
from config import Config
import os

app = Flask(__name__)

# Load configuration
try:
    Config.validate_config()
    app.config.from_object(Config)
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please copy .env.example to .env and fill in your Azure AD details")
    exit(1)

# Initialize Azure AD authentication
azure_auth = AzureADAuth()

@app.route('/')
def index():
    """Home page - shows login status"""
    user = session.get('user')
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    """Initiate Azure AD login process"""
    try:
        auth_url = azure_auth.get_authorization_request_url(session)
        return redirect(auth_url)
    except Exception as e:
        flash(f'Login error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/getAToken')
def get_token():
    """Handle the redirect from Azure AD after authentication"""
    try:
        # Get authorization code from query parameters
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code:
            error = request.args.get('error')
            error_description = request.args.get('error_description')
            flash(f'Authentication failed: {error} - {error_description}', 'error')
            return redirect(url_for('index'))
        
        # Exchange code for token
        result = azure_auth.acquire_token_by_authorization_code(code, state, session)
        
        if 'access_token' in result:
            # Get user information
            user_info = azure_auth.get_user_info(result['access_token'])
            
            # Store user info in session
            session['user'] = {
                'name': user_info.get('displayName', 'Unknown'),
                'email': user_info.get('mail', user_info.get('userPrincipalName', 'Unknown')),
                'id': user_info.get('id'),
                'access_token': result['access_token']
            }
            
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            error = result.get('error', 'Unknown error')
            error_description = result.get('error_description', 'No description')
            flash(f'Token acquisition failed: {error} - {error_description}', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Authentication error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    flash('Successfully logged out!', 'info')
    
    # Get the appropriate post-logout redirect URI
    if os.environ.get('WEBSITE_SITE_NAME'):  # Running on Azure
        post_logout_uri = f"https://{azure_auth.config.WEBSITE_HOSTNAME}"
    else:  # Running locally
        post_logout_uri = "http://localhost:5000"
    
    # Redirect to Azure AD logout URL for complete logout
    logout_url = f"{azure_auth.config.AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={post_logout_uri}"
    return redirect(logout_url)

@app.route('/profile')
def profile():
    """Display user profile information"""
    user = session.get('user')
    if not user:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='localhost', port=5000)
