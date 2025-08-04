# Azure AD Authentication Flask Application

A simple Python Flask web application that demonstrates Azure Active Directory authentication using MSAL (Microsoft Authentication Library).

## Features

- 🔐 Azure Active Directory OAuth2 authentication
- 👤 User profile information from Microsoft Graph API
- 🔄 Secure session management
- 🚪 Proper logout functionality
- 📱 Responsive Bootstrap UI

## Prerequisites

- Python 3.12 or higher
- Azure AD tenant with app registration
- Azure AD application configured with redirect URI

## Azure AD Setup

1. **Register an Application in Azure AD:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to Azure Active Directory > App registrations
   - Click "New registration"
   - Enter application name (e.g., "Flask Azure AD App")
   - Set redirect URI to `http://localhost:5000/getAToken`
   - Note down the Application (client) ID and Directory (tenant) ID

2. **Create Client Secret:**
   - In your app registration, go to "Certificates & secrets"
   - Click "New client secret"
   - Note down the secret value

3. **Configure API Permissions:**
   - Go to "API permissions"
   - Add Microsoft Graph > Delegated permissions > User.Read

## Installation

1. **Clone and setup the project:**
   ```bash
   cd c:\kodiranje\azure_login
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` file with your Azure AD details:
   ```
   CLIENT_ID=your-azure-ad-client-id
   CLIENT_SECRET=your-azure-ad-client-secret
   TENANT_ID=your-azure-ad-tenant-id
   SECRET_KEY=your-secret-key-here
   ```

## Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Click "Sign in with Microsoft" to test the authentication flow**

## Project Structure

```
azure_login/
├── app.py                 # Main Flask application
├── azure_auth.py          # Azure AD authentication logic
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── base.html         # Base template with Bootstrap
│   ├── index.html        # Home page
│   ├── dashboard.html    # User dashboard
│   └── profile.html      # User profile page
└── .github/
    └── copilot-instructions.md  # Copilot instructions

```

## Key Components

### Azure Authentication (`azure_auth.py`)
- Handles OAuth2 authorization flow
- Token acquisition and validation
- Microsoft Graph API integration

### Flask Routes (`app.py`)
- `/` - Home page with login status
- `/login` - Initiate Azure AD authentication
- `/getAToken` - Handle OAuth callback
- `/logout` - Clear session and logout
- `/profile` - Display user profile

### Configuration (`config.py`)
- Environment variable management
- Azure AD settings
- Flask configuration

## Deployment to Azure App Services

1. **Create Azure App Service:**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myapp --runtime "PYTHON|3.12"
   ```

2. **Configure environment variables in Azure:**
   - Set all variables from `.env` file in App Service Configuration

3. **Deploy the application:**
   ```bash
   az webapp deployment source config-zip --resource-group myResourceGroup --name myapp --src app.zip
   ```

## Security Notes

- Always use HTTPS in production
- Store secrets in Azure Key Vault for production
- Implement proper error handling
- Validate all OAuth state parameters
- Use secure session configuration

## Troubleshooting

**Common Issues:**
1. **Invalid redirect URI** - Ensure the redirect URI in Azure AD matches exactly
2. **Missing permissions** - Check API permissions in Azure AD
3. **Token acquisition fails** - Verify client secret and tenant ID

## Next Steps

- Add role-based access control
- Implement reservation management features
- Add database integration
- Set up continuous deployment
- Add logging and monitoring
