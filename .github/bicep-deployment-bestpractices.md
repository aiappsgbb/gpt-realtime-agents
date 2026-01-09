# Bicep Deployment Best Practices with Azure Developer CLI

This document outlines essential best practices for Bicep infrastructure templates that work seamlessly with Azure Developer CLI (azd) and ensure consistent, secure deployments.

## 🏗️ Core Principles

### 1. Template Reusability
- **Always use modules from `infra/core/`** - Never inline resource definitions in main.bicep
- **Leverage Azure Verified Modules (AVM)** when available for standard resources
- **Create custom modules** for organization-specific patterns under `infra/core/`
- **Parameterize everything** - No hardcoded values in templates

### 2. Security First
- **Managed Identity Only** - Never use access keys or connection strings for authentication
- **User Assigned Managed Identity** - Required for all Azure Container Apps
- **RBAC Configuration** - Implement least privilege access with specific roles
- **Secret Management** - Use Azure Key Vault for sensitive values

### 3. Azure Developer CLI Integration
- **Parameter Validation** - Strict input validation with proper decorators
- **Output Consistency** - Standardized outputs for azd hook scripts
- **Environment Variable Alignment** - Match Container Apps env vars with application configuration

## 📁 Template Structure

### main.bicep Organization

```bicep
targetScope = 'resourceGroup'

// 1. METADATA
metadata description = 'Main infrastructure template for [Project Name]'
metadata author = 'Your Team'
metadata version = '1.0.0'

// 2. PARAMETERS - Input Validation
@description('Environment name (dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environmentName string

@description('Location for all resources')
param location string = resourceGroup().location

@description('Principal ID for RBAC assignments')
param principalId string = ''

@description('Enable GitHub Actions integration')
param githubActions bool = false

// Container Image Parameters (updated by azd deploy)
@description('Container image for API service')
param apiAppImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

// 3. VARIABLES - Computed Values
var abbrs = loadJsonContent('./abbreviations.json')
var tags = {
  'azd-env-name': environmentName
  'azd-provision-param-hash': take(uniqueString(deployment().name), 8)
}

// 4. SHARED INFRASTRUCTURE
module userAssignedIdentity 'core/security/user-assigned-identity.bicep' = {
  name: 'user-assigned-identity'
  params: {
    name: '${abbrs.managedIdentityUserAssignedIdentities}${environmentName}'
    location: location
    tags: tags
  }
}

module keyVault 'core/security/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    name: '${abbrs.keyVaultVaults}${environmentName}'
    location: location
    tags: tags
    principalId: principalId
    managedIdentityPrincipalId: userAssignedIdentity.outputs.principalId
  }
}

// 5. HOSTING INFRASTRUCTURE
module containerAppsEnvironment 'core/host/container-apps-environment.bicep' = {
  name: 'container-apps-environment'
  params: {
    name: '${abbrs.appManagedEnvironments}${environmentName}'
    location: location
    tags: tags
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
}

// 6. APPLICATION MODULES
module apiApp 'core/host/container-app.bicep' = {
  name: 'api-app'
  params: {
    name: '${abbrs.appContainerApps}api-${environmentName}'
    location: location
    tags: tags
    containerAppsEnvironmentId: containerAppsEnvironment.outputs.id
    containerRegistryName: containerRegistry.outputs.name
    userAssignedIdentityId: userAssignedIdentity.outputs.id
    managedIdentityPrincipalId: userAssignedIdentity.outputs.principalId
    githubActions: githubActions
    containerImage: apiAppImage
    containerPort: 80
    environmentVariables: [
      // CRITICAL: Always include AZURE_CLIENT_ID
      {
        name: 'AZURE_CLIENT_ID'
        value: userAssignedIdentity.outputs.clientId
      }
      // Application-specific variables
      {
        name: 'APPLICATION_INSIGHTS_CONNECTION_STRING'
        value: monitoring.outputs.applicationInsightsConnectionString
      }
      {
        name: 'AZURE_KEY_VAULT_ENDPOINT'
        value: keyVault.outputs.endpoint
      }
      // Add other required environment variables
    ]
    resources: {
      cpu: 1
      memory: '2Gi'
    }
  }
}

// 7. OUTPUTS - For azd integration and hook scripts
output AZURE_LOCATION string = location
output AZURE_RESOURCE_GROUP string = resourceGroup().name

// Identity Outputs
output AZURE_CLIENT_ID string = userAssignedIdentity.outputs.clientId
output AZURE_PRINCIPAL_ID string = userAssignedIdentity.outputs.principalId

// Service Endpoints
output API_ENDPOINT string = apiApp.outputs.fqdn
output API_NAME string = apiApp.outputs.name

// Infrastructure Outputs
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.endpoint
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.loginServer
```

## 🔧 Parameter Management

### main.parameters.json Structure

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "value": "${AZURE_ENV_NAME}"
    },
    "location": {
      "value": "${AZURE_LOCATION}"
    },
    "principalId": {
      "value": "${AZURE_PRINCIPAL_ID}"
    },
    "githubActions": {
      "value": false
    }
  }
}
```

### Parameter Validation Best Practices

```bicep
// String Length Validation
@description('Environment name')
@minLength(1)
@maxLength(10)
param environmentName string

// Allowed Values
@description('Environment type')
@allowed(['dev', 'staging', 'prod'])
param environmentType string

// Conditional Parameters
@description('Container image (updated by azd deploy)')
@minLength(5)
param containerImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

// Resource Name Validation
@description('Resource group name')
@maxLength(90)
param resourceGroupName string = ''

// Boolean with Clear Description
@description('Enable diagnostic settings and monitoring')
param enableMonitoring bool = true
```

## 🔐 Security & Authentication

### Managed Identity Pattern

**✅ ALWAYS Use This Pattern:**

```bicep
// 1. Create User Assigned Managed Identity
module userAssignedIdentity 'core/security/user-assigned-identity.bicep' = {
  name: 'user-assigned-identity'
  params: {
    name: '${abbrs.managedIdentityUserAssignedIdentities}${environmentName}'
    location: location
    tags: tags
  }
}

// 2. Assign to Container Apps
module containerApp 'core/host/container-app.bicep' = {
  name: 'container-app'
  params: {
    userAssignedIdentityId: userAssignedIdentity.outputs.id
    managedIdentityPrincipalId: userAssignedIdentity.outputs.principalId
    environmentVariables: [
      {
        name: 'AZURE_CLIENT_ID'
        value: userAssignedIdentity.outputs.clientId  // ✅ REQUIRED
      }
    ]
  }
}

// 3. Configure RBAC for Azure Services
resource keyVaultSecretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, userAssignedIdentity.outputs.principalId, 'Key Vault Secrets User')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: userAssignedIdentity.outputs.principalId
    principalType: 'ServicePrincipal'
  }
}
```

### RBAC Role Assignments

**Use specific, least-privilege roles:**

```bicep
// Azure OpenAI - Cognitive Services User
var cognitiveServicesUserRole = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'

// Azure AI Search - Search Service Contributor  
var searchServiceContributorRole = '7ca78c08-252a-4471-8644-bb5ff32d4ba0'

// Azure Storage - Storage Blob Data Contributor
var storageBlobDataContributorRole = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'

// Azure Key Vault - Key Vault Secrets User
var keyVaultSecretsUserRole = '4633458b-17de-408a-b874-0445c86b69e6'

// Example RBAC Assignment
resource openAiRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAi.id, principalId, cognitiveServicesUserRole)
  scope: openAi
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesUserRole)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

## 🚀 Azure Container Apps Best Practices

### Environment Variable Alignment

**Critical**: Container Apps environment variables MUST match application configuration.

#### 1. Check Application Settings Class

```python
# utils/config.py
class AppSettings(BaseSettings):
    # Azure Services
    azure_openai_endpoint: str
    azure_search_endpoint: str
    azure_storage_account_url: str
    azure_cosmos_endpoint: str
    azure_key_vault_endpoint: str
    
    # Azure Identity
    azure_client_id: str | None = None  # REQUIRED for Container Apps
    
    # Application Settings
    log_level: str = "INFO"
    debug: bool = False
    
    class Config:
        env_prefix = "AZURE_"
```

#### 2. Match in Bicep Template

```bicep
environmentVariables: [
  // Identity - ALWAYS REQUIRED
  {
    name: 'AZURE_CLIENT_ID'
    value: userAssignedIdentity.outputs.clientId
  }
  // Service Endpoints - Match settings class exactly
  {
    name: 'AZURE_OPENAI_ENDPOINT'
    value: openAi.outputs.endpoint
  }
  {
    name: 'AZURE_SEARCH_ENDPOINT'  
    value: searchService.outputs.endpoint
  }
  {
    name: 'AZURE_STORAGE_ACCOUNT_URL'
    value: storageAccount.outputs.primaryEndpoints.blob
  }
  {
    name: 'AZURE_COSMOS_ENDPOINT'
    value: cosmosDb.outputs.endpoint
  }
  {
    name: 'AZURE_KEY_VAULT_ENDPOINT'
    value: keyVault.outputs.endpoint
  }
  // Application Settings
  {
    name: 'LOG_LEVEL'
    value: 'INFO'
  }
  {
    name: 'DEBUG'
    value: 'false'
  }
]
```

#### 3. Validate with .env File

```bash
# .env file (for local development)
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net/
AZURE_STORAGE_ACCOUNT_URL=https://yourstorage.blob.core.windows.net/
AZURE_COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/
AZURE_KEY_VAULT_ENDPOINT=https://your-keyvault.vault.azure.net/
AZURE_CLIENT_ID=your-managed-identity-client-id
LOG_LEVEL=INFO
DEBUG=false
```

**Environment Variable Naming Rules:**
- Use SCREAMING_SNAKE_CASE for environment variables
- Match exactly between Bicep, application settings, and .env files
- Always include `AZURE_CLIENT_ID` for Container Apps
- Use descriptive, consistent naming conventions

### Container App Module Standards

```bicep
// Standard Container App configuration
module containerApp 'core/host/container-app.bicep' = {
  name: 'container-app-name'
  params: {
    // Required Parameters
    name: '${abbrs.appContainerApps}service-${environmentName}'
    location: location
    tags: tags
    
    // Container Configuration
    containerImage: serviceImage
    containerPort: 80  // Standard for web applications
    
    // Identity & Security
    userAssignedIdentityId: userAssignedIdentity.outputs.id
    managedIdentityPrincipalId: userAssignedIdentity.outputs.principalId
    
    // Infrastructure References
    containerAppsEnvironmentId: containerAppsEnvironment.outputs.id
    containerRegistryName: containerRegistry.outputs.name
    
    // Resource Allocation
    resources: {
      cpu: 1        // Adjust based on application needs
      memory: '2Gi' // Adjust based on application needs
    }
    
    // Scaling Configuration
    scale: {
      minReplicas: 1
      maxReplicas: 10
      rules: [
        {
          name: 'http-scaling'
          http: {
            metadata: {
              concurrentRequests: '10'
            }
          }
        }
      ]
    }
    
    // Environment Variables - CRITICAL ALIGNMENT
    environmentVariables: [
      // ... as shown above
    ]
    
    // Deployment Configuration
    githubActions: githubActions
  }
}
```

## 📤 Output Management

### Standard Output Pattern

```bicep
// Environment Information
output AZURE_LOCATION string = location
output AZURE_RESOURCE_GROUP string = resourceGroup().name
output AZURE_ENV_NAME string = environmentName

// Identity Outputs - For authentication
output AZURE_CLIENT_ID string = userAssignedIdentity.outputs.clientId
output AZURE_PRINCIPAL_ID string = userAssignedIdentity.outputs.principalId

// Service Endpoints - For application configuration
output AZURE_OPENAI_ENDPOINT string = openAi.outputs.endpoint
output AZURE_SEARCH_ENDPOINT string = searchService.outputs.endpoint
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.endpoint

// Application Endpoints - For testing and integration
output API_ENDPOINT string = apiApp.outputs.fqdn
output WEB_ENDPOINT string = webApp.outputs.fqdn

// Resource Names - For azd hook scripts
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.name
output AZURE_KEY_VAULT_NAME string = keyVault.outputs.name

// Container App Details - For deployment automation
output API_CONTAINER_APP_NAME string = apiApp.outputs.name
output API_CONTAINER_APP_ID string = apiApp.outputs.id
```

### Output Naming Conventions

- **Environment Variables**: Use for service endpoints that applications consume
- **Resource Names**: Use for azd hook scripts that need to reference resources
- **Service Endpoints**: Use for external integrations and testing
- **Container App Details**: Use for deployment automation and monitoring

## 🔍 Validation Checklist

### Pre-Deployment Validation

- [ ] All modules use `infra/core/` templates
- [ ] User Assigned Managed Identity is created and assigned
- [ ] RBAC roles are specific and least-privilege
- [ ] No API keys or connection strings in templates
- [ ] Container Apps include `AZURE_CLIENT_ID` environment variable
- [ ] Environment variables match application settings classes
- [ ] Parameter validation decorators are applied
- [ ] Outputs follow naming conventions
- [ ] Resource naming uses abbreviations.json
- [ ] Tags include azd-specific metadata

### Post-Deployment Validation

- [ ] Container Apps start successfully (check logs for env var errors)
- [ ] Managed Identity authentication works
- [ ] RBAC assignments allow required access
- [ ] Service endpoints are accessible
- [ ] Environment variables are correctly set
- [ ] Application configuration loads without errors

## 🚨 Common Pitfalls

### ❌ Avoid These Patterns

```bicep
// DON'T: Inline resource definitions
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  // Use module instead: 'core/storage/storage-account.bicep'
}

// DON'T: Hardcoded values
param location string = 'East US'  // Use resourceGroup().location

// DON'T: Missing validation
param environmentName string  // Add @allowed decorator

// DON'T: Generic outputs
output storageKey string = storage.listKeys().keys[0].value  // Use endpoint instead

// DON'T: Missing AZURE_CLIENT_ID
environmentVariables: [
  {
    name: 'SOME_OTHER_VAR'
    value: 'value'
  }
  // Missing AZURE_CLIENT_ID will cause authentication failures
]
```

### ✅ Use These Patterns Instead

```bicep
// DO: Use modules
module storageAccount 'core/storage/storage-account.bicep' = { ... }

// DO: Parameterize with defaults
param location string = resourceGroup().location

// DO: Validate inputs
@allowed(['dev', 'staging', 'prod'])
param environmentName string

// DO: Provide service endpoints
output AZURE_STORAGE_ENDPOINT string = storageAccount.outputs.primaryEndpoints.blob

// DO: Always include managed identity
environmentVariables: [
  {
    name: 'AZURE_CLIENT_ID'
    value: userAssignedIdentity.outputs.clientId
  }
  // ... other variables
]
```

## 🔗 Integration with Azure Developer CLI

### azd Environment Variables

These outputs automatically become azd environment variables:

```bicep
// These outputs are available in azd hooks as ${AZURE_OPENAI_ENDPOINT}
output AZURE_OPENAI_ENDPOINT string = openAi.outputs.endpoint
output AZURE_SEARCH_ENDPOINT string = searchService.outputs.endpoint
output API_ENDPOINT string = apiApp.outputs.fqdn
```

### Hook Script Integration

```python
# infra/scripts/postprovision.py
import os
from utils import get_azd_env

def main():
    env_vars = get_azd_env()
    
    # These come from main.bicep outputs
    openai_endpoint = env_vars['AZURE_OPENAI_ENDPOINT']
    api_endpoint = env_vars['API_ENDPOINT']
    keyvault_name = env_vars['AZURE_KEY_VAULT_NAME']
    
    # Configure resources using these values
    configure_ai_services(openai_endpoint)
    setup_application_secrets(keyvault_name)
```

## 📚 Module Standards

### Custom Module Template

```bicep
// infra/core/[category]/[service].bicep
targetScope = 'resourceGroup'

@description('Resource name')
@minLength(1)
@maxLength(50)
param name string

@description('Location for resources')
param location string = resourceGroup().location

@description('Resource tags')
param tags object = {}

@description('Managed Identity Principal ID for RBAC')
param managedIdentityPrincipalId string = ''

// Resource definition
resource service 'Microsoft.SomeService/someResource@2023-01-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    // Service-specific configuration
  }
}

// RBAC assignments (if needed)
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(managedIdentityPrincipalId)) {
  name: guid(service.id, managedIdentityPrincipalId, 'ServiceRole')
  scope: service
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'role-id')
    principalId: managedIdentityPrincipalId
    principalType: 'ServicePrincipal'
  }
}

// Standard outputs
output id string = service.id
output name string = service.name
output endpoint string = service.properties.endpoint  // If applicable
```

---

## 🎯 Summary

Following these best practices ensures:

1. **Consistent Infrastructure** - Reusable modules and standardized patterns
2. **Secure Authentication** - Managed Identity with proper RBAC
3. **azd Integration** - Proper parameters, outputs, and environment alignment
4. **Application Compatibility** - Environment variables match application configuration
5. **Maintainable Code** - Clear structure and validation rules

**Remember**: The goal is to create infrastructure templates that work reliably with Azure Developer CLI while maintaining security best practices and ensuring applications start successfully with proper authentication.