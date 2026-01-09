# Azure Best Practices

This document outlines essential best practices for Azure integration across all applications and infrastructure in this repository.

## 🔐 Authentication & Security

### Core Principle: Zero Trust Authentication

**NEVER use API keys or connection strings for Azure service authentication.**

All authentication MUST use Microsoft Entra ID (Azure Active Directory) with the following hierarchy:

1. **Azure Developer CLI** for local development
2. **Managed Identity** for production deployments

### Authentication Implementation

#### For Applications (Python, Node.js, .NET)

**✅ CORRECT - ChainedTokenCredential Pattern:**

```python
# Python (FastAPI, Gradio, Streamlit)
from azure.identity import AzureDeveloperCliCredential, ManagedIdentityCredential, ChainedTokenCredential

def get_azure_credential() -> ChainedTokenCredential:
    """Get Azure credential using best practice chain."""
    return ChainedTokenCredential(
        AzureDeveloperCliCredential(),  # Local development with azd
        ManagedIdentityCredential()     # Production with managed identity
    )
```

```typescript
// Node.js/TypeScript
import { ChainedTokenCredential, AzureDeveloperCliCredential, ManagedIdentityCredential } from '@azure/identity';

export function getAzureCredential(): ChainedTokenCredential {
    return new ChainedTokenCredential(
        new AzureDeveloperCliCredential(), // Local development with azd
        new ManagedIdentityCredential()    // Production with managed identity
    );
}
```

```csharp
// .NET (ASP.NET Core)
using Azure.Identity;

public static class AzureCredentialHelper
{
    public static ChainedTokenCredential GetAzureCredential()
    {
        return new ChainedTokenCredential(
            new AzureDeveloperCliCredential(), // Local development with azd
            new ManagedIdentityCredential()    // Production with managed identity
        );
    }
}
```

**❌ INCORRECT - Never Use These:**

```python
# NEVER do this - API keys are forbidden
client = OpenAIClient(
    endpoint="https://your-endpoint.openai.azure.com/",
    api_key="your-api-key"  # ❌ FORBIDDEN
)

# NEVER do this - connection strings with keys
blob_client = BlobServiceClient(
    account_url="https://account.blob.core.windows.net",
    credential="DefaultEndpointsProtocol=https;AccountName=..."  # ❌ FORBIDDEN
)
```

### Environment Variables

#### Required for Container Apps

Always set `AZURE_CLIENT_ID` environment variable in Azure Container Apps to specify which managed identity to use:

```bicep
environmentVariables: [
  {
    name: 'AZURE_CLIENT_ID'
    value: userAssignedIdentity.outputs.clientId  // ✅ REQUIRED
  }
  // Other environment variables...
]
```

#### Forbidden Environment Variables

**Never use these environment variables:**

- `AZURE_OPENAI_API_KEY` ❌
- `AZURE_AI_SEARCH_KEY` ❌  
- `AZURE_STORAGE_ACCOUNT_KEY` ❌
- `AZURE_COSMOS_DB_KEY` ❌
- Any `*_KEY` or `*_SECRET` variables for Azure services ❌

## 🏗️ Infrastructure as Code

### Managed Identity Requirements

**ALL infrastructure MUST use User Assigned Managed Identity:**

```bicep
// ✅ CORRECT - Always create User Assigned Managed Identity
module userAssignedIdentity 'core/security/user-assigned-identity.bicep' = {
  name: 'user-assigned-identity'
  params: {
    name: '${abbrs.managedIdentityUserAssignedIdentities}${environmentName}'
    location: location
    tags: tags
  }
}

// ✅ CORRECT - Assign to Container Apps
module containerApp 'core/host/container-app.bicep' = {
  name: 'container-app'
  params: {
    userAssignedIdentityId: userAssignedIdentity.outputs.id
    managedIdentityPrincipalId: userAssignedIdentity.outputs.principalId
    // ...
  }
}
```

### RBAC Role Assignments

**Use least privilege principle with specific roles:**

```bicep
// ✅ CORRECT - Specific roles for specific resources
resource keyVaultSecretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, principalId, keyVaultSecretsUserRole)
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6') // Key Vault Secrets User
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageDataContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, principalId, storageBlobDataContributorRole)
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}

resource cognitiveServicesUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openAi.id, principalId, cognitiveServicesUserRole)
  scope: openAi
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908') // Cognitive Services User
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

**❌ NEVER use these overprivileged roles:**

- `Contributor` (too broad)
- `Owner` (excessive permissions)
- `Key Vault Administrator` (when Secrets User suffices)

### Forbidden Infrastructure Patterns

**❌ NEVER create or use access keys in Bicep:**

```bicep
// ❌ FORBIDDEN - Don't create access keys
var storageAccountKey = storageAccount.listKeys().keys[0].value

// ❌ FORBIDDEN - Don't output sensitive values
output storageKey string = storageAccount.listKeys().keys[0].value

// ❌ FORBIDDEN - Don't use accessKey parameter
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  properties: {
    authenticationMethod: 'accessKey'  // ❌ Use 'managedIdentity' instead
  }
}
```

## 🚀 Application Configuration

### Service Client Configuration

**✅ CORRECT patterns for different Azure services:**

```python
# Azure OpenAI
from azure.ai.openai import AzureOpenAI

credential = get_azure_credential()
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
)

# Azure AI Search
from azure.search.documents import SearchClient

client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=credential
)

# Azure Storage
from azure.storage.blob import BlobServiceClient

client = BlobServiceClient(
    account_url=account_url,
    credential=credential
)

# Azure Cosmos DB
from azure.cosmos import CosmosClient

client = CosmosClient(
    url=endpoint,
    credential=credential
)
```

### Configuration Management

**Use environment-based configuration without secrets:**

```python
# ✅ CORRECT - No keys in configuration
class AzureSettings(BaseSettings):
    # Endpoints only - no keys
    openai_endpoint: str
    search_endpoint: str
    storage_account_url: str
    cosmos_endpoint: str
    keyvault_endpoint: str
    
    # Client ID for managed identity
    client_id: str | None = None
    
    class Config:
        env_prefix = "AZURE_"
```

## 📋 Deployment Configuration

### Azure Developer CLI (azd)

**Environment variables in azure.yaml:**

```yaml
services:
  api:
    project: "./src/api"
    language: python
    host: containerapp
    docker:
      remoteBuild: true
    env:
      # ✅ CORRECT - Endpoints and connection strings only
      - AZURE_OPENAI_ENDPOINT
      - AZURE_SEARCH_ENDPOINT
      - AZURE_STORAGE_ACCOUNT_URL
      - AZURE_COSMOS_ENDPOINT
      - AZURE_KEYVAULT_ENDPOINT
      - APPLICATION_INSIGHTS_CONNECTION_STRING
      - AZURE_CLIENT_ID  # ✅ REQUIRED for managed identity
      
      # ❌ FORBIDDEN - No keys in environment
      # - AZURE_OPENAI_API_KEY
      # - AZURE_SEARCH_KEY
      # - AZURE_STORAGE_ACCOUNT_KEY
```

### Container Apps Environment Variables

**Set in Bicep templates:**

```bicep
environmentVariables: [
  {
    name: 'AZURE_CLIENT_ID'
    value: userAssignedIdentity.outputs.clientId
  }
  {
    name: 'AZURE_OPENAI_ENDPOINT'
    value: openAi.outputs.endpoint
  }
  {
    name: 'AZURE_SEARCH_ENDPOINT'
    value: searchService.outputs.endpoint
  }
  {
    name: 'APPLICATION_INSIGHTS_CONNECTION_STRING'
    value: monitoring.outputs.applicationInsightsConnectionString
  }
  // ✅ Connection strings are acceptable (contain no keys)
]
```

## 🔍 Security Validation

### Pre-deployment Checklist

Before deploying any code or infrastructure:

- [ ] No API keys in code, configuration, or environment variables
- [ ] All Azure service clients use `ChainedTokenCredential`
- [ ] `AZURE_CLIENT_ID` environment variable is set for Container Apps
- [ ] Managed Identity is assigned appropriate RBAC roles
- [ ] No `Contributor` or `Owner` role assignments
- [ ] All sensitive values are retrieved from Key Vault (if needed)
- [ ] Infrastructure uses User Assigned Managed Identity
- [ ] No `listKeys()` functions in Bicep templates

### Code Review Requirements

All code must pass these security checks:

1. **No hardcoded credentials**: Search for patterns like `api_key=`, `secret=`, `password=`
2. **No key-based authentication**: Verify all Azure clients use managed identity
3. **No dangerous environment variables**: Check for `*_KEY`, `*_SECRET` variables
4. **Proper credential chain**: Ensure `AzureDeveloperCliCredential` → `ManagedIdentityCredential`

## 📚 Additional Resources

### Microsoft Documentation

- [Azure Identity client library best practices](https://docs.microsoft.com/azure/developer/intro/azure-developer-cli)
- [Managed identities for Azure resources](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/)
- [Azure RBAC built-in roles](https://docs.microsoft.com/azure/role-based-access-control/built-in-roles)

### Repository Integration

This document is referenced in:

- [GitHub Copilot Instructions](./copilot-instructions.md#azure-integration)
- [AI Agents Configuration](../AGENTS.md#development-standards)
- All application prompt files (`.github/prompts/*.prompt.md`)

---

## 🚨 Remember

**Security is not optional. Every line of code that connects to Azure MUST follow these practices.**

When in doubt, always choose managed identity over access keys. When managed identity isn't available, use Azure Key Vault with managed identity to retrieve secrets.

**Zero exceptions. Zero API keys. Zero compromise.**