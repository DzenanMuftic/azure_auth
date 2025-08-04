import os
from dotenv import load_dotenv

# Load environment variables only in development
if not os.environ.get('WEBSITE_SITE_NAME'):  # Not running on Azure
    load_dotenv()

class Config:
    # Azure AD Configuration
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
    REDIRECT_PATH = "/getAToken"
    ENDPOINT = "https://graph.microsoft.com/v1.0/me"
    SCOPE = ["User.ReadBasic.All"]
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SESSION_TYPE = 'filesystem'
    
    # Azure App Service specific settings
    WEBSITE_HOSTNAME = os.getenv('WEBSITE_HOSTNAME', 'localhost:5000')
    
    def get_redirect_uri(self):
        """Get the full redirect URI based on environment"""
        if os.environ.get('WEBSITE_SITE_NAME'):  # Running on Azure
            return f"https://{self.WEBSITE_HOSTNAME}{self.REDIRECT_PATH}"
        else:  # Running locally
            return f"http://localhost:5000{self.REDIRECT_PATH}"
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present"""
        required_vars = ['CLIENT_ID', 'CLIENT_SECRET', 'TENANT_ID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
