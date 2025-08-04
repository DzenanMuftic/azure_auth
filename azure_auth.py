import msal
from config import Config

class AzureADAuth:
    def __init__(self):
        self.config = Config()
        self.app = msal.ConfidentialClientApplication(
            self.config.CLIENT_ID,
            authority=self.config.AUTHORITY,
            client_credential=self.config.CLIENT_SECRET
        )
    
    def get_authorization_request_url(self, session):
        """Generate the authorization URL for Azure AD login"""
        auth_url = self.app.get_authorization_request_url(
            self.config.SCOPE,
            redirect_uri=self._build_redirect_uri(),
            state=self._generate_state()
        )
        
        # Store state in session for validation
        session['state'] = self._generate_state()
        return auth_url
    
    def acquire_token_by_authorization_code(self, code, state, session):
        """Exchange authorization code for access token"""
        # Validate state parameter
        if state != session.get('state'):
            raise ValueError("Invalid state parameter")
        
        result = self.app.acquire_token_by_authorization_code(
            code,
            scopes=self.config.SCOPE,
            redirect_uri=self._build_redirect_uri()
        )
        
        return result
    
    def get_user_info(self, access_token):
        """Get user information from Microsoft Graph API"""
        import requests
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.config.ENDPOINT, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.status_code}")
    
    def _build_redirect_uri(self):
        """Build the redirect URI"""
        return self.config.get_redirect_uri()
    
    def _generate_state(self):
        """Generate a random state parameter for CSRF protection"""
        import secrets
        return secrets.token_urlsafe(32)
