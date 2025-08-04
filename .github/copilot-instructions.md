<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Azure AD Authentication Flask Application

This is a Python Flask application that implements Azure Active Directory authentication using MSAL (Microsoft Authentication Library).

## Project Structure
- `app.py` - Main Flask application with routes
- `azure_auth.py` - Azure AD authentication logic
- `config.py` - Configuration management
- `templates/` - HTML templates using Bootstrap
- `requirements.txt` - Python dependencies

## Key Features
- Azure AD OAuth2 authentication flow
- Secure session management
- User profile information from Microsoft Graph API
- Bootstrap-based responsive UI
- Proper logout with Azure AD sign-out

## Development Guidelines
- Follow Flask best practices for route handling
- Use MSAL library for all Azure AD interactions
- Implement proper error handling for authentication flows
- Store sensitive configuration in environment variables
- Use Bootstrap components for consistent UI styling

## Security Considerations
- Always validate state parameters in OAuth flows
- Store access tokens securely in sessions
- Implement proper CSRF protection
- Use HTTPS in production environments
