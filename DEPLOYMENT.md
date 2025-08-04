# Azure Deployment Guide

## Prerequisites
1. Azure CLI installed: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
2. Azure subscription and account

## Deployment Steps

### 1. Login to Azure
```bash
az login
```

### 2. Create Resource Group
```bash
az group create --name myResourceGroup --location "West Europe"
```

### 3. Create App Service Plan
```bash
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku FREE --is-linux
```

### 4. Create Web App
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name your-app-name --runtime "PYTHON|3.12" --deployment-local-git
```

### 5. Configure Application Settings (Environment Variables)
```bash
az webapp config appsettings set --resource-group myResourceGroup --name your-app-name --settings \
  CLIENT_ID="your-azure-ad-client-id" \
  CLIENT_SECRET="your-azure-ad-client-secret" \
  TENANT_ID="cd2a81e-51be-4a91-82df-ac10bee3e90b" \
  SECRET_KEY="your-production-secret-key"
```

### 6. Deploy Code
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# Add Azure remote
git remote add azure https://your-app-name.scm.azurewebsites.net:443/your-app-name.git

# Deploy
git push azure main
```

### 7. Update Azure AD App Registration
- Go to Azure Portal → Azure AD → App registrations → Your app
- In Authentication settings, add new Redirect URI:
  `https://your-app-name.azurewebsites.net/getAToken`

## Environment Variables Required in Azure:
- CLIENT_ID: Your Azure AD Application ID
- CLIENT_SECRET: Your Azure AD Client Secret  
- TENANT_ID: Your Azure AD Tenant ID
- SECRET_KEY: A secure random string for Flask sessions

## Troubleshooting:
- Check application logs: `az webapp log tail --resource-group myResourceGroup --name your-app-name`
- View deployment logs in Azure Portal under Deployment Center
