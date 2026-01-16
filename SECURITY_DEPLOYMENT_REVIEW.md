# Security & Network Hardening Review: Identity, Private Networking, and Required SKUs

**Review Date:** 2026-01-16  
**Repository:** aiappsgbb/gpt-realtime-agents  
**Reviewer:** GitHub Copilot Agent  

---

## Executive Summary

This document provides a comprehensive security and deployment hardening review of the GPT Realtime Agents accelerator. The review focuses on three key areas:

1. **Identity & Secrets Usage** - Evaluation of authentication mechanisms and credential management
2. **Network Isolation Capabilities** - Assessment of private networking and locked-down deployment feasibility
3. **Required Azure SKUs** - Identification of minimum SKU requirements for enterprise-grade security

**Key Findings:**
- ✅ The application **partially supports** Managed Identity authentication
- ⚠️ The application **requires API keys** for several Azure services due to service limitations
- ⚠️ **Fully private deployment is NOT currently achievable** due to external service dependencies
- ⚠️ Several services require **specific SKUs** to support private endpoints and advanced security features

---

## 1. Identity & Secrets Usage Analysis

### 1.1 Components Using Managed Identity

#### ✅ Azure OpenAI Realtime API (Browser Sessions)

**Location:** `audio_backend/backend.py`

**Implementation:**
```python
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider

credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
```

**IaC Configuration:** `infra/app/audio-backend.bicep`
```bicep
resource apiIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

module app '../shared/host/container-app-upsert.bicep' = {
  params: {
    identityType: 'UserAssigned'
    identityName: apiIdentity.name
    env: union(env, [
      {
        name: 'AZURE_CLIENT_ID'
        value: apiIdentity.properties.clientId
      }
    ])
  }
}
```

**Status:** ✅ **FULLY COMPLIANT**
- Uses **User-Assigned Managed Identity** for Azure OpenAI authentication
- No API keys required when Managed Identity is properly configured
- DefaultAzureCredential chain supports local development (AzureDeveloperCliCredential) and production (ManagedIdentityCredential)

---

#### ✅ Azure Container Registry

**Location:** `infra/shared/host/container-app.bicep`

**Implementation:**
```bicep
module containerRegistryAccess '../security/registry-access.bicep' = if (usePrivateRegistry) {
  name: '${deployment().name}-registry-access'
  params: {
    containerRegistryName: containerRegistryName
    principalId: usePrivateRegistry ? userIdentity.properties.principalId : ''
  }
}

configuration: {
  registries: usePrivateRegistry ? [
    {
      server: '${containerRegistryName}.${containerRegistryHostSuffix}'
      identity: userIdentity.id
    }
  ] : []
}
```

**Status:** ✅ **FULLY COMPLIANT**
- Uses **User-Assigned Managed Identity** for ACR authentication
- No admin credentials required
- ACR pull role automatically assigned via `registry-access.bicep`

---

#### ✅ Application Insights

**Location:** `infra/app/audio-backend.bicep`

**Implementation:**
```bicep
env: union(env, [
  {
    name: 'AZURE_CLIENT_ID'
    value: apiIdentity.properties.clientId
  }
  {
    name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
    value: applicationInsights.properties.ConnectionString
  }
])
```

**Status:** ✅ **FULLY COMPLIANT**
- Uses **connection string** (not instrumentation key)
- Connection string supports both key-based and Entra ID authentication
- Can be enhanced to use Managed Identity exclusively via Azure Monitor OpenTelemetry

---

### 1.2 Components NOT Using Managed Identity

#### ⚠️ Azure OpenAI Realtime API (Initial Session Creation)

**Location:** `infra/main.bicep` (lines 119-120, 127-128)

**Current Implementation:**
```bicep
{
  name: 'AZURE_GPT_REALTIME_KEY'
  value: gptRealtimeKey
}
{
  name: 'AZURE_OPENAI_API_KEY'
  value: azureOpenAiApiKey
}
```

**Code Reference:** `audio_backend/common/config.py` (lines 86-91)
```python
return BrowserRealtimeConfig(
    realtime_session_url=_clean_env("AZURE_GPT_REALTIME_URL"),
    webrtc_url=_clean_env("WEBRTC_URL"),
    default_deployment=default_deployment,
    default_voice=_clean_env("AZURE_GPT_REALTIME_VOICE", default="verse"),
    azure_api_key=_optional_env("AZURE_GPT_REALTIME_KEY"),
)
```

**Why API Key is Used:**
1. **Fallback Authentication** - The code supports both Managed Identity and API key authentication
2. **Development Convenience** - API keys simplify local development setup
3. **Optional** - The `azure_api_key` is marked as `Optional[str]`, indicating it can be None

**Managed Identity Alternative:**
✅ **ALREADY IMPLEMENTED** - The application uses `DefaultAzureCredential` and `get_bearer_token_provider` in `backend.py`

**Migration Path:**
```python
# In browser_session_service.py, headers are generated with token provider
async def create_browser_session(...):
    if connection_mode == "webrtc":
        return await _create_gpt_realtime_session(
            deployment=deployment,
            voice=voice,
            headers=_ensure_headers(realtime_headers),  # Uses token from DefaultAzureCredential
        )
```

**Recommendation:** ⚠️ **CONDITIONALLY COMPLIANT**
- API keys are **optional** and used as fallback
- Managed Identity is the **primary authentication method**
- For fully locked-down deployment: **Remove API key parameters** from `infra/main.bicep` and ensure proper RBAC roles

**Required RBAC Role:**
- `Cognitive Services OpenAI User` (role ID: `5e0bd9bd-7b93-4f28-af87-19fc36ad61bd`)

---

#### ⚠️ Azure Voice Live API

**Location:** `infra/main.bicep` (lines 154-155)

**Current Implementation:**
```bicep
{
  name: 'AZURE_VOICELIVE_API_KEY'
  value: azureVoiceLiveApiKey
}
```

**Code Reference:** `audio_backend/common/config.py` (lines 96-97)
```python
def get_voice_live_config() -> VoiceLiveConfig:
    endpoint = _clean_env("AZURE_VOICELIVE_ENDPOINT")
    api_key = _clean_env("AZURE_VOICELIVE_API_KEY")
```

**Why API Key is Required:**
1. **Service Limitation** - Azure Voice Live (Speech Service) currently requires API key for WebSocket connections
2. **No Managed Identity Support** - The Voice Live realtime API endpoint does not support Entra ID authentication tokens for WebSocket connections

**Managed Identity Alternative:**
❌ **NOT CURRENTLY SUPPORTED** by Azure Voice Live WebSocket API

**Workarounds:**
1. **Azure Key Vault Integration** (Recommended)
   - Store API key in Azure Key Vault
   - Use Managed Identity to retrieve secret from Key Vault
   - Rotate keys regularly
   
2. **Service Endpoint Protection**
   - Use Virtual Network Service Endpoints
   - Restrict Speech Service to private network
   - Use IP allowlisting

**Recommendation:** ⚠️ **JUSTIFIED EXCEPTION**
- API key is **required** due to service limitations
- **Mitigation:** Store in Azure Key Vault and retrieve via Managed Identity
- **Future:** Monitor Azure Voice Live service updates for Managed Identity support

**Implementation Example:**
```bicep
// Store Voice Live API key in Key Vault
module voiceLiveSecret '../shared/security/keyvault-secret.bicep' = {
  name: 'voice-live-api-key-secret'
  params: {
    name: 'voice-live-api-key'
    keyVaultName: keyVault.outputs.name
    secretValue: azureVoiceLiveApiKey
  }
}

// Grant Managed Identity access to Key Vault
module keyVaultAccess '../shared/security/keyvault-access.bicep' = {
  name: 'audio-backend-keyvault-access'
  params: {
    keyVaultName: keyVault.outputs.name
    principalId: apiIdentity.properties.principalId
  }
}

// Reference secret in Container App
env: [
  {
    name: 'AZURE_VOICELIVE_API_KEY'
    secretRef: 'voice-live-api-key'
  }
]
secrets: {
  'voice-live-api-key': {
    keyVaultUrl: '${keyVault.outputs.endpoint}secrets/voice-live-api-key'
    identity: apiIdentity.id
  }
}
```

---

#### ⚠️ Azure Communication Services (ACS)

**Location:** `infra/main.bicep` (lines 133-136)

**Current Implementation:**
```bicep
{
  name: 'AZURE_ACS_CONN_KEY'
  value: azureAcsConnKey
}
```

**Code Reference:** `audio_backend/common/config.py` (lines 124-125), `audio_backend/acs/acs.py` (lines 26-27, 41-42, 52-53)
```python
# Configuration
def get_acs_config() -> AcsConfig:
    return AcsConfig(
        source_number=_optional_env("ACS_PHONE_NUMBER"),
        connection_string=_optional_env("AZURE_ACS_CONN_KEY"),
        # ...
    )

# Usage in AcsCaller
def __init__(self, source_number:str, acs_connection_string: str, ...):
    self.acs_connection_string = acs_connection_string
    # ...

async def initiate_call(self, target_number: str):
    self.call_automation_client = CallAutomationClient.from_connection_string(self.acs_connection_string)
    # ...

async def answer_inbound_call(self, incoming_call_context: str):
    self.call_automation_client = CallAutomationClient.from_connection_string(self.acs_connection_string)
    # ...
```

**Why Connection String is Used:**
1. **SDK Limitation** - The `CallAutomationClient.from_connection_string()` method is used
2. **Historical Pattern** - Connection strings were the original authentication method for ACS

**Managed Identity Alternative:**
✅ **SUPPORTED** - ACS Call Automation supports Managed Identity via `CallAutomationClient(endpoint, credential)`

**Migration Path:**
```python
# Current implementation
self.call_automation_client = CallAutomationClient.from_connection_string(self.acs_connection_string)

# Managed Identity implementation
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
acs_endpoint = "https://<resource-name>.communication.azure.com"
self.call_automation_client = CallAutomationClient(acs_endpoint, credential)
```

**Required Changes:**
1. **Update `audio_backend/acs/acs.py`:**
   - Replace `from_connection_string()` with credential-based initialization
   - Pass ACS endpoint instead of connection string
   
2. **Update `infra/main.bicep`:**
   - Remove `azureAcsConnKey` parameter
   - Add `azureAcsEndpoint` parameter
   - Grant Managed Identity the following RBAC role:

**Required RBAC Role:**
- `Azure Communication Services User` (for call operations)
- `Contributor` or custom role with `Microsoft.Communication/CommunicationServices/Write` permission

**Recommendation:** ⚠️ **CAN BE MIGRATED TO MANAGED IDENTITY**
- Connection string is **NOT required**
- Managed Identity authentication is **fully supported**
- **Action Required:** Refactor code to use credential-based authentication

---

### 1.3 Summary: Identity & Secrets Inventory

| Component | Identity Mechanism | Status | Migration Effort |
|-----------|-------------------|--------|------------------|
| **Azure OpenAI Realtime** (WebRTC) | User-Assigned Managed Identity | ✅ Compliant | N/A - Already using MI |
| **Azure Container Registry** | User-Assigned Managed Identity | ✅ Compliant | N/A - Already using MI |
| **Application Insights** | Connection String (supports MI) | ✅ Compliant | Low - Can enhance with MI |
| **Azure OpenAI API Keys** | API Key (fallback) | ⚠️ Optional | None - Already supports MI |
| **Azure Voice Live** | API Key (required) | ⚠️ Exception | Medium - Store in Key Vault |
| **Azure Communication Services** | Connection String | ⚠️ Needs Migration | Medium - Refactor to use MI |

**Overall Assessment:**
- **3 of 6** components fully use Managed Identity (50%)
- **1 component** has justified exception (Azure Voice Live - service limitation)
- **2 components** can be migrated to Managed Identity with medium effort

---

## 2. Locked-Down Network Deployment Analysis

### 2.1 Current Network Architecture

**Default Configuration:**
- All services deployed with **public endpoints enabled**
- No VNet integration configured
- No Private Endpoints defined
- Container Apps Environment uses **default networking**

### 2.2 Service-by-Service Network Isolation Assessment

#### 2.2.1 Azure Container Apps

**Current Configuration:** `infra/shared/host/container-apps-environment.bicep`
```bicep
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}
```

**Private Networking Support:**
✅ **SUPPORTED** - Azure Container Apps supports VNet integration

**Required Configuration:**
```bicep
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  properties: {
    vnetConfiguration: {
      infrastructureSubnetId: infrastructureSubnet.id
      internal: true  // Internal environment (no public ingress)
    }
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}
```

**Required Subnet:**
- **Minimum CIDR:** `/23` (512 IPs) for infrastructure subnet
- **Recommended CIDR:** `/21` (2048 IPs) for production workloads

**Networking Model:**
- ✅ **VNet Integration:** Supported
- ✅ **Internal Environment:** Supported (blocks public ingress)
- ✅ **Outbound Control:** Supports User Defined Routes (UDR)
- ⚠️ **Limitation:** Internal environments require private DNS configuration

**Inbound Access Requirements:**
- **Public Scenario:** Direct internet access via FQDN
- **Private Scenario:** Requires Azure Application Gateway, Front Door, or internal load balancer

**Outbound Dependencies:**
- ✅ Azure Container Registry (can use Private Endpoint)
- ✅ Azure OpenAI (can use Private Endpoint)
- ✅ Application Insights (can use Private Link)
- ⚠️ Azure Communication Services (limited Private Endpoint support)

---

#### 2.2.2 Azure Container Registry

**Current Configuration:** `infra/shared/host/container-registry.bicep`
```bicep
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  sku: {
    name: 'Basic'  // ⚠️ Does not support Private Endpoints
  }
  properties: {
    publicNetworkAccess: 'Enabled'
  }
}
```

**Private Networking Support:**
❌ **NOT SUPPORTED ON BASIC SKU**
✅ **SUPPORTED ON PREMIUM SKU**

**Required Configuration for Private Endpoints:**
```bicep
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  sku: {
    name: 'Premium'  // ✅ Required for Private Endpoints
  }
  properties: {
    publicNetworkAccess: 'Disabled'
    networkRuleSet: {
      defaultAction: 'Deny'
    }
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${containerRegistry.name}-pe'
  location: location
  properties: {
    subnet: {
      id: privateEndpointSubnet.id
    }
    privateLinkServiceConnections: [
      {
        name: '${containerRegistry.name}-pe-connection'
        properties: {
          privateLinkServiceId: containerRegistry.id
          groupIds: ['registry']
        }
      }
    ]
  }
}
```

**Required SKU Change:**
- **Current:** Basic SKU
- **Required:** Premium SKU

**Cost Impact:**
- **Basic:** ~$5/month
- **Premium:** ~$500/month (100x increase)

**Networking Model:**
- ❌ **Basic SKU:** Public endpoint only
- ✅ **Premium SKU:** Private Endpoint support
- ✅ **VNet Integration:** Supported via Private Endpoint

---

#### 2.2.3 Azure OpenAI

**Current Configuration:** Not managed by this accelerator (external dependency)

**Expected Configuration:** `infra/shared/ai/cognitiveservices.bicep`
```bicep
resource account 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  properties: {
    publicNetworkAccess: 'Enabled'  // Default
    networkAcls: {
      defaultAction: 'Allow'  // ⚠️ No restrictions
    }
  }
}
```

**Private Networking Support:**
✅ **SUPPORTED** - Azure OpenAI supports Private Endpoints

**Required Configuration:**
```bicep
resource account 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  properties: {
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      defaultAction: 'Deny'
      virtualNetworkRules: [
        {
          id: appSubnet.id
          ignoreMissingVnetServiceEndpoint: false
        }
      ]
    }
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${account.name}-pe'
  properties: {
    subnet: {
      id: privateEndpointSubnet.id
    }
    privateLinkServiceConnections: [
      {
        name: '${account.name}-pe-connection'
        properties: {
          privateLinkServiceId: account.id
          groupIds: ['account']
        }
      }
    ]
  }
}
```

**Private DNS Zone:**
- **Required Zone:** `privatelink.openai.azure.com`
- **A Record:** `<resource-name>.openai.azure.com` → Private IP

**Networking Model:**
- ✅ **Private Endpoint:** Supported
- ✅ **Service Endpoint:** Supported
- ✅ **Network ACLs:** Supported (IP and VNet restrictions)

**Limitation:**
⚠️ **WebRTC Regional Endpoint** (`https://<region>.realtimeapi-preview.ai.azure.com`) is a **shared public endpoint** and **does not support Private Endpoints**

**Impact on Locked-Down Deployment:**
- ⚠️ The WebRTC URL requires **outbound internet access** to the regional endpoint
- ❌ **Cannot be fully private** when using WebRTC mode
- ✅ **Can be private** when using WebSocket mode with Private Endpoint on Azure OpenAI resource

---

#### 2.2.4 Azure Communication Services

**Current Configuration:** Not managed by this accelerator (external dependency)

**Private Networking Support:**
⚠️ **LIMITED SUPPORT** - ACS has limited Private Link support

**Current Service Endpoints:**
1. **Call Automation API** - HTTPS endpoint for call control
2. **Media Streaming WebSocket** - WebSocket for real-time audio streams
3. **PSTN Gateway** - Phone call termination and origination

**Private Endpoint Support Matrix:**

| Service Component | Private Endpoint Support | Workaround |
|-------------------|--------------------------|------------|
| Call Automation API (HTTPS) | ❌ Not Supported | Service Endpoint + IP restrictions |
| Media Streaming (WebSocket) | ❌ Not Supported | VNet Service Endpoint |
| PSTN Gateway | ❌ Not Supported | N/A - External telecom network |
| SMS | ✅ Supported (Private Link) | N/A - Not used in this accelerator |
| Chat | ✅ Supported (Private Link) | N/A - Not used in this accelerator |

**Network Restrictions Available:**
```bicep
// ACS does not support networkAcls via Bicep currently
// Must be configured via Azure Portal or REST API
```

**Workaround for Locked-Down Environment:**
1. **Service Endpoint** - Enable Microsoft.Communication service endpoint on Container Apps subnet
2. **Firewall Rules** - Configure Azure Firewall to allow outbound to ACS endpoints
3. **IP Restrictions** - Configure ACS resource to only accept traffic from known public IPs (if available)

**Required Firewall Rules:**
```
# ACS Call Automation API
https://<resource-name>.communication.azure.com

# ACS Media Streaming
wss://<resource-name>.communication.azure.com

# PSTN Gateway (cannot be restricted)
*.communication.azure.com
```

**Networking Model:**
- ❌ **Private Endpoint:** Not supported for Call Automation
- ⚠️ **Service Endpoint:** Supported (partial protection)
- ❌ **Fully Private:** Not achievable

---

#### 2.2.5 Log Analytics & Application Insights

**Current Configuration:** `infra/shared/monitor/monitoring.bicep`

**Private Networking Support:**
✅ **SUPPORTED** - Azure Monitor supports Private Link Scope (AMPLS)

**Required Configuration:**
```bicep
resource ampls 'Microsoft.Insights/privateLinkScopes@2021-07-01-preview' = {
  name: 'ampls-${resourceToken}'
  location: 'global'
  properties: {
    accessModeSettings: {
      ingestionAccessMode: 'PrivateOnly'
      queryAccessMode: 'PrivateOnly'
    }
  }
}

resource amplsScopedResource 'Microsoft.Insights/privateLinkScopes/scopedResources@2021-07-01-preview' = {
  parent: ampls
  name: 'scoped-${applicationInsights.name}'
  properties: {
    linkedResourceId: applicationInsights.id
  }
}

resource amplsPrivateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'ampls-pe'
  properties: {
    subnet: {
      id: privateEndpointSubnet.id
    }
    privateLinkServiceConnections: [
      {
        name: 'ampls-connection'
        properties: {
          privateLinkServiceId: ampls.id
          groupIds: ['azuremonitor']
        }
      }
    ]
  }
}
```

**Private DNS Zones Required:**
- `privatelink.monitor.azure.com`
- `privatelink.oms.opinsights.azure.com`
- `privatelink.ods.opinsights.azure.com`
- `privatelink.agentsvc.azure-automation.net`
- `privatelink.blob.core.windows.net` (for Application Insights)

**Networking Model:**
- ✅ **Private Link Scope:** Supported
- ✅ **Fully Private:** Achievable with AMPLS
- ✅ **Ingestion & Query:** Both support private access

---

### 2.3 External Dependencies Requiring Public Internet Access

#### 1. **Azure OpenAI WebRTC Regional Endpoint**
- **Endpoint:** `https://<region>.realtimeapi-preview.ai.azure.com/v1/realtimertc`
- **Protocol:** HTTPS
- **Requirement:** Outbound internet access
- **Private Alternative:** Use WebSocket mode with Private Endpoint on Azure OpenAI resource
- **Impact:** ⚠️ **Blocks fully private WebRTC deployment**

#### 2. **Azure Communication Services PSTN**
- **Endpoints:** Multiple regional gateways (`*.communication.azure.com`)
- **Protocol:** SIP/RTP (phone network integration)
- **Requirement:** Outbound internet access to ACS infrastructure
- **Private Alternative:** ❌ None - PSTN requires external connectivity
- **Impact:** ⚠️ **Blocks fully private phone integration**

#### 3. **Azure Communication Services Call Automation API**
- **Endpoint:** `https://<resource-name>.communication.azure.com`
- **Protocol:** HTTPS
- **Requirement:** Outbound internet access
- **Private Alternative:** Service Endpoint (partial protection)
- **Impact:** ⚠️ **No Private Endpoint support**

#### 4. **Event Grid Webhooks (Inbound Callbacks)**
- **Direction:** Inbound from Event Grid to Container App
- **Protocol:** HTTPS POST
- **Requirement:** Publicly accessible webhook endpoint
- **Private Alternative:** ✅ Event Grid supports Private Endpoints for event delivery
- **Impact:** ✅ **Can be made private with configuration**

---

### 2.4 Required Network Configuration for Locked-Down Deployment

#### VNet Design

```
VNet: 10.0.0.0/16

Subnets:
├── ContainerAppsInfrastructure: 10.0.0.0/23 (512 IPs) - Required for ACA environment
├── PrivateEndpoints: 10.0.2.0/24 (256 IPs) - For all Private Endpoints
├── ApplicationGateway: 10.0.3.0/24 (256 IPs) - For inbound traffic (if needed)
└── AzureFirewall: 10.0.4.0/26 (64 IPs) - For controlled outbound (optional)
```

#### Private DNS Zones Required

| Service | Private DNS Zone | Purpose |
|---------|------------------|---------|
| Container Registry | `privatelink.azurecr.io` | ACR Private Endpoint |
| Azure OpenAI | `privatelink.openai.azure.com` | OpenAI Private Endpoint |
| Azure Monitor | `privatelink.monitor.azure.com` | Application Insights |
| Log Analytics | `privatelink.oms.opinsights.azure.com` | Log Analytics ingestion |
| Log Analytics | `privatelink.ods.opinsights.azure.com` | Log Analytics data |
| Storage Account | `privatelink.blob.core.windows.net` | App Insights blob storage |

#### Network Security Groups (NSGs)

**Container Apps Infrastructure Subnet NSG:**
```bicep
// Inbound Rules
- Allow: Azure Load Balancer → * (TCP 443, 80)
- Allow: VNet → Container Apps Subnet (all ports) - Internal communication
- Deny: Internet → * (all)

// Outbound Rules
- Allow: Container Apps → Private Endpoints Subnet (TCP 443, 5671, 5672) - Dependencies
- Allow: Container Apps → Internet (TCP 443) - External dependencies (ACS, WebRTC)
- Deny: * → * (all others)
```

**Private Endpoints Subnet NSG:**
```bicep
// Inbound Rules
- Allow: VNet → Private Endpoints Subnet (TCP 443)
- Deny: Internet → * (all)

// Outbound Rules
- Allow: * → VNet (all) - Response traffic
- Deny: * → Internet (all)
```

#### Required Firewall Rules (if using Azure Firewall)

**Application Rules:**
```
# Azure OpenAI WebRTC (if using WebRTC mode)
Rule: Allow-OpenAI-WebRTC
  Target FQDN: *.realtimeapi-preview.ai.azure.com
  Protocol: HTTPS
  Port: 443

# Azure Communication Services
Rule: Allow-ACS
  Target FQDN: *.communication.azure.com
  Protocol: HTTPS, WSS
  Port: 443

# Azure Container Registry (if not using Private Endpoint)
Rule: Allow-ACR
  Target FQDN: *.azurecr.io
  Protocol: HTTPS
  Port: 443
```

**Network Rules:**
```
# Azure Communication Services Media (if needed)
Rule: Allow-ACS-Media
  Destination IP: ACS service tag or IP ranges
  Protocol: UDP
  Port: 3478-3481 (STUN/TURN if used)
```

---

### 2.5 Feasibility Assessment: Fully Private Deployment

**Question:** Can this accelerator be deployed with **no public internet exposure**?

**Answer:** ❌ **NO** - A fully private deployment is **NOT currently achievable** due to the following blockers:

#### Blockers:

1. **Azure OpenAI WebRTC Regional Endpoint**
   - ❌ No Private Endpoint support
   - ⚠️ **Workaround:** Use WebSocket mode instead of WebRTC (see limitation below)
   - ⚠️ **Limitation:** WebSocket mode provides degraded user experience compared to WebRTC

2. **Azure Communication Services Call Automation**
   - ❌ No Private Endpoint support for Call Automation API
   - ❌ No Private Endpoint support for Media Streaming
   - ⚠️ **Partial Mitigation:** Use Service Endpoints (does not provide full isolation)

3. **Azure Communication Services PSTN Gateway**
   - ❌ PSTN requires external telecommunications network connectivity
   - ❌ Cannot be isolated to private network
   - ⚠️ **Alternative:** Disable phone integration (limits functionality)

#### Achievable Private Deployment Scenarios:

**Scenario 1: Private WebSocket-Only Mode (No Phone Integration)**
- ✅ Disable Azure Communication Services integration
- ✅ Use WebSocket mode (not WebRTC) with Private Endpoint on Azure OpenAI
- ✅ All other services use Private Endpoints
- ⚠️ **Limitation:** No phone call features, degraded browser experience

**Scenario 2: Locked-Down with Controlled Outbound**
- ✅ All services use Private Endpoints where supported
- ✅ Azure Firewall or NVA controls outbound traffic
- ✅ Explicit allow rules for required external dependencies
- ⚠️ **Limitation:** Still requires internet egress for ACS and WebRTC

**Scenario 3: Internal Ingress Only**
- ✅ Container Apps Environment configured as internal
- ✅ Access via Application Gateway or Azure Front Door with WAF
- ✅ No direct public access to Container Apps
- ⚠️ **Limitation:** Application Gateway/Front Door still have public IPs

#### Recommendation:

For enterprise environments requiring maximum security:

1. **Implement Scenario 2** (Locked-Down with Controlled Outbound)
   - Deploy all resources with Private Endpoints where supported
   - Use Azure Firewall Premium for outbound traffic inspection
   - Enable firewall logs and alerts for security monitoring
   - Implement NSGs on all subnets
   - Use Private DNS zones for name resolution

2. **Future-Proof Architecture**
   - Monitor Azure service updates for Private Endpoint support
   - Design infrastructure with VNet integration from the start
   - Document external dependencies and review quarterly

3. **Accept Controlled Internet Egress**
   - Azure Communication Services and WebRTC require internet access
   - Implement DDoS Protection on all public IPs
   - Use Azure Firewall threat intelligence to block malicious destinations
   - Monitor and alert on unexpected outbound connections

---

## 3. Required Azure SKUs for Fully Locked-Down Deployment

### 3.1 SKU Requirements by Service

| Azure Service | Current SKU | Required SKU for Private Networking | Reason | Cost Impact |
|---------------|-------------|-------------------------------------|--------|-------------|
| **Azure Container Apps Environment** | Consumption | Consumption | VNet integration supported on Consumption tier | None |
| **Azure Container Registry** | Basic | **Premium** | Private Endpoint support requires Premium SKU | ~$495/month increase |
| **Azure OpenAI** | S0 (Standard) | S0 (Standard) | Private Endpoint supported on Standard tier | None |
| **Azure Communication Services** | Standard | Standard | No SKU variations (service-based pricing) | None |
| **Log Analytics Workspace** | Pay-as-you-go | Pay-as-you-go | Private Link Scope supported on all tiers | None |
| **Application Insights** | Workspace-based | Workspace-based | AMPLS supported on workspace-based mode | None |
| **Azure Monitor Private Link Scope** | N/A | **Required** | New resource required for private ingestion | None (pay-as-you-go) |
| **Virtual Network** | N/A | **Required** | Foundation for private networking | ~$5-20/month (minimal) |
| **Private Endpoints** | N/A | **Required** | ~5-7 endpoints needed | ~$7/endpoint/month = ~$35-50/month |
| **Private DNS Zones** | N/A | **Required** | ~6-8 zones needed | ~$0.50/zone/month = ~$3-4/month |
| **Azure Firewall** (Optional) | N/A | Premium (recommended) | Outbound traffic control + TLS inspection | ~$1,250/month |
| **Application Gateway** (Optional) | N/A | Standard_v2 or WAF_v2 | Inbound traffic for internal ACA environment | ~$250-500/month |
| **NAT Gateway** (Optional) | N/A | Standard | Static outbound IP for Container Apps | ~$33/month + data transfer |

### 3.2 Detailed SKU Justifications

#### 3.2.1 Azure Container Registry - Premium SKU

**Current:** Basic SKU (~$5/month)  
**Required:** Premium SKU (~$500/month)

**Reason:**
- **Private Endpoint Support** - Only Premium SKU supports Private Link
- **VNet Integration** - Required for Container Apps to pull images privately
- **Geo-Replication** - Bonus capability for disaster recovery (not required but included)

**Features Unlocked:**
- ✅ Private Endpoints (up to 10)
- ✅ Customer-managed keys
- ✅ Content Trust for image signing
- ✅ Geo-replication for high availability
- ✅ Up to 500 GB storage included

**Cost-Benefit Analysis:**
- **Cost:** ~$495/month increase
- **Benefit:** Eliminates public internet access for container image pulls
- **Alternative:** Use Azure Container Apps with public ACR + IP restrictions (less secure)

**Recommendation:**
- **Required for:** Fully locked-down deployments
- **Optional for:** Development environments with network restrictions
- **Cost Mitigation:** Use Basic SKU in dev, Premium in production

---

#### 3.2.2 Azure Firewall Premium

**Current:** None (direct internet egress)  
**Optional:** Premium SKU (~$1,250/month)

**Reason:**
- **TLS Inspection** - Inspect encrypted traffic to external dependencies
- **IDPS** (Intrusion Detection and Prevention System)
- **URL Filtering** - Granular control over allowed FQDNs
- **Web Categories** - Block categories of websites

**Features Required for Enterprise Security:**
- ✅ TLS inspection for outbound HTTPS to ACS and Azure OpenAI WebRTC
- ✅ Threat intelligence-based filtering
- ✅ Application rules with FQDN filtering
- ✅ Network rules with IP filtering
- ✅ Logging and diagnostics integration

**Cost-Benefit Analysis:**
- **Cost:** ~$1,250/month base + data processing costs
- **Benefit:** Complete visibility and control over outbound traffic
- **Alternative:** Azure Firewall Standard (~$640/month) - No TLS inspection

**Recommendation:**
- **Required for:** Highly regulated industries (finance, healthcare, government)
- **Optional for:** General enterprise environments
- **Cost Mitigation:** Use Network Security Groups + Service Endpoints instead

---

#### 3.2.3 Application Gateway (WAF_v2)

**Current:** None (direct ingress to Container Apps)  
**Optional:** WAF_v2 SKU (~$300-500/month)

**Reason:**
- **Internal Container Apps Environment** - Requires Application Gateway for ingress
- **Web Application Firewall** - Protection against OWASP Top 10
- **SSL Offloading** - Centralized certificate management
- **URL-based Routing** - Advanced routing capabilities

**When Required:**
- Container Apps Environment configured with `internal: true`
- No direct public ingress to Container Apps
- Centralized ingress point with WAF protection

**Cost-Benefit Analysis:**
- **Cost:** ~$300-500/month depending on tier and capacity units
- **Benefit:** WAF protection + internal networking
- **Alternative:** Azure Front Door Premium (~$350/month base + traffic costs)

**Recommendation:**
- **Required for:** Internal Container Apps deployments
- **Optional for:** External Container Apps with built-in HTTPS
- **Alternative:** Azure Front Door for global distribution

---

#### 3.2.4 Private DNS Zones

**Current:** None (using public DNS)  
**Required:** 6-8 Private DNS Zones (~$3-4/month)

**Zones Required:**

1. `privatelink.azurecr.io` - Azure Container Registry
2. `privatelink.openai.azure.com` - Azure OpenAI
3. `privatelink.monitor.azure.com` - Azure Monitor
4. `privatelink.oms.opinsights.azure.com` - Log Analytics ingestion
5. `privatelink.ods.opinsights.azure.com` - Log Analytics data
6. `privatelink.blob.core.windows.net` - Application Insights storage
7. `privatelink.agentsvc.azure-automation.net` - Azure Monitor agent (if used)

**Cost:** ~$0.50 per zone per month = ~$3-4/month total

**Reason:**
- **Name Resolution** - Private Endpoints require DNS configuration
- **Automatic Registration** - Private DNS zones auto-update with Private Endpoint IPs
- **VNet Linking** - Links DNS zone to VNet for resolution

---

#### 3.2.5 Private Endpoints

**Current:** None  
**Required:** 5-7 Private Endpoints (~$35-50/month)

**Endpoints Required:**

1. **Azure Container Registry** (1 endpoint) - Container image pulls
2. **Azure OpenAI** (1 endpoint) - AI model access (WebSocket mode)
3. **Azure Monitor Private Link Scope** (1 endpoint) - Logs and metrics
4. **Storage Account** (1 endpoint, if used) - Application data
5. **Key Vault** (1 endpoint, optional) - Secrets management
6. **Event Grid** (1 endpoint, optional) - Event delivery

**Cost:** ~$7.30 per endpoint per month (~730 hours × $0.01/hour)

**Data Transfer:** Additional costs for inbound data through Private Endpoints

---

### 3.3 Minimum SKU Configuration for Locked-Down Deployment

**Scenario: Fully Locked-Down (Maximum Security)**

| Resource | SKU | Monthly Cost (Estimate) |
|----------|-----|-------------------------|
| Azure Container Apps | Consumption | Pay-per-use (~$50-200) |
| Azure Container Registry | **Premium** | ~$500 |
| Azure OpenAI | S0 Standard | Pay-per-token (~$100-500) |
| Azure Communication Services | Standard | Pay-per-use (~$50-200) |
| Log Analytics | Pay-as-you-go | ~$30-100 |
| Application Insights | Workspace-based | Included with Log Analytics |
| Virtual Network | Standard | ~$10 |
| Private Endpoints (7) | Standard | ~$50 |
| Private DNS Zones (7) | Standard | ~$4 |
| Azure Firewall | **Premium** | ~$1,250 |
| Application Gateway | WAF_v2 (2 CU) | ~$300 |
| NAT Gateway | Standard | ~$33 |
| **Total** | | **~$2,477-3,297/month** |

**Comparison to Baseline (No Private Networking):**

| Configuration | Monthly Cost | Security Level |
|---------------|--------------|----------------|
| Baseline (Public Endpoints) | ~$250-500 | ⚠️ Low |
| Locked-Down (without Firewall) | ~$1,147-1,997 | ✅ Medium-High |
| **Fully Locked-Down** | **~$2,477-3,297** | ✅ **High** |

**Cost Increase:** ~10x increase for maximum security

---

### 3.4 Cost Optimization Strategies

#### Strategy 1: Hybrid Approach (Recommended for Most Organizations)

**Environment-Specific SKUs:**

- **Development:** Basic ACR + Public endpoints (~$250/month)
- **Staging:** Premium ACR + Private Endpoints (~$1,200/month)
- **Production:** Full locked-down configuration (~$2,500/month)

**Savings:** ~50% overall by tiering security based on environment

---

#### Strategy 2: Selective Private Endpoints

**Priority-Based Implementation:**

**Phase 1: Critical Services (Required)**
- ✅ Azure Container Registry Private Endpoint
- ✅ Azure OpenAI Private Endpoint
- ✅ Azure Monitor Private Link Scope

**Phase 2: Enhanced Security (Recommended)**
- ⚠️ Azure Firewall Standard (not Premium)
- ⚠️ NSGs on all subnets
- ⚠️ Service Endpoints for ACS

**Phase 3: Maximum Security (Optional)**
- ⚠️ Azure Firewall Premium with TLS inspection
- ⚠️ Application Gateway with WAF
- ⚠️ Additional Private Endpoints (Key Vault, Storage)

**Savings:** ~40% by deferring Azure Firewall Premium

---

#### Strategy 3: Azure Firewall Alternatives

**Option A: Network Virtual Appliance (NVA)**
- Use third-party firewall (Palo Alto, Fortinet, etc.)
- Similar features to Azure Firewall Premium
- May offer better pricing for large deployments

**Option B: Network Security Groups Only**
- Use NSGs for basic traffic filtering
- No TLS inspection or IDPS
- Significant cost savings (~$1,250/month)

**Savings:** Up to 50% by avoiding Azure Firewall

---

#### Strategy 4: Azure Front Door vs. Application Gateway

**Comparison:**

| Feature | Application Gateway | Azure Front Door Premium |
|---------|---------------------|--------------------------|
| Base Cost | ~$300/month | ~$350/month + traffic |
| WAF | ✅ Included | ✅ Included (enhanced) |
| Global Distribution | ❌ Regional only | ✅ Global CDN |
| Private Link Support | ✅ Native | ✅ Private Link to origin |
| DDoS Protection | ⚠️ Standard | ✅ Enhanced |

**Recommendation:**
- **Use Application Gateway** if traffic is regional
- **Use Azure Front Door** if traffic is global or DDoS protection is critical

---

### 3.5 SKU Decision Matrix

| Requirement | Recommended SKU | Alternative | Cost Savings |
|-------------|-----------------|-------------|--------------|
| **Container image pulls must be private** | ACR Premium | None | N/A - Required |
| **AI model access must be private** | Azure OpenAI S0 + Private Endpoint | Service Endpoint + IP restrictions | ~$7/month (PE cost) |
| **Outbound traffic inspection required** | Azure Firewall Premium | Azure Firewall Standard | ~$600/month |
| **Inbound WAF protection required** | Application Gateway WAF_v2 | Azure Front Door Premium | Variable |
| **Log ingestion must be private** | AMPLS + Private Endpoint | Public ingress with IP restrictions | ~$7/month |
| **VNet integration required** | ACA Consumption | N/A | No cost (already supported) |
| **Static outbound IP required** | NAT Gateway | Load Balancer with outbound rules | Similar cost |

---

## 4. Summary and Recommendations

### 4.1 Identity & Secrets - Action Items

**Immediate Actions (High Priority):**
1. ✅ **Migrate Azure Communication Services to Managed Identity**
   - Update `audio_backend/acs/acs.py` to use credential-based authentication
   - Remove `AZURE_ACS_CONN_KEY` from infrastructure parameters
   - Grant Managed Identity appropriate RBAC roles

2. ⚠️ **Store Azure Voice Live API Key in Key Vault**
   - Create Key Vault module in infrastructure
   - Store `AZURE_VOICELIVE_API_KEY` as secret
   - Configure Container App to retrieve from Key Vault using Managed Identity

3. ✅ **Remove Optional API Keys**
   - Remove `gptRealtimeKey` and `azureOpenAiApiKey` from `infra/main.bicep`
   - Ensure production deployments rely exclusively on Managed Identity
   - Keep API keys only for local development (via `.env`)

**Short-Term Actions (Medium Priority):**
4. ✅ **Enhance Application Insights to Use Managed Identity**
   - Configure Azure Monitor OpenTelemetry with Managed Identity
   - Remove connection string dependency (if feasible)

5. ✅ **Document Credential Usage**
   - Create `AUTHENTICATION.md` documenting all authentication patterns
   - Specify RBAC roles required for Managed Identity
   - Provide migration guide for existing deployments

**Long-Term Actions (Low Priority):**
6. ⚠️ **Monitor Azure Voice Live Service Updates**
   - Track Azure Speech Service roadmap for Managed Identity support
   - Plan migration when WebSocket authentication supports Entra ID

---

### 4.2 Network Isolation - Action Items

**Immediate Actions (High Priority):**
1. ✅ **Implement VNet Integration**
   - Add VNet and subnet modules to infrastructure
   - Configure Container Apps Environment with VNet integration
   - Deploy Private Endpoints for ACR, Azure OpenAI, and Application Insights

2. ✅ **Upgrade Azure Container Registry to Premium SKU**
   - Required for Private Endpoint support
   - Plan for cost increase (~$495/month)
   - Implement in production first, then staging

3. ✅ **Configure Private DNS Zones**
   - Create required Private DNS zones
   - Link zones to VNet
   - Configure automatic registration for Private Endpoints

**Short-Term Actions (Medium Priority):**
4. ✅ **Implement Azure Monitor Private Link Scope**
   - Create AMPLS resource
   - Configure Private Endpoint for monitoring
   - Update Container Apps to use private ingestion

5. ⚠️ **Document External Dependencies**
   - Create network architecture diagram
   - List all external endpoints (ACS, WebRTC)
   - Document required firewall rules

6. ⚠️ **Implement Network Security Groups**
   - Create NSG for Container Apps infrastructure subnet
   - Create NSG for Private Endpoints subnet
   - Configure baseline deny-all rules with explicit allows

**Long-Term Actions (Low Priority):**
7. ⚠️ **Evaluate Azure Firewall Implementation**
   - Assess organization's security requirements
   - Calculate cost-benefit of Premium vs. Standard
   - Plan phased rollout (Standard → Premium)

8. ⚠️ **Consider Internal Container Apps Environment**
   - Evaluate need for Application Gateway
   - Plan for ingress architecture
   - Document access patterns for internal users

---

### 4.3 Deployment Readiness Matrix

| Deployment Scenario | Feasibility | Required Changes | Estimated Cost (Monthly) |
|---------------------|-------------|------------------|--------------------------|
| **Baseline (Current)** | ✅ Production Ready | None | ~$250-500 |
| **Development/POC** | ✅ Production Ready | None | ~$250-500 |
| **Enterprise (Basic Security)** | ✅ Achievable | Premium ACR + Private Endpoints | ~$1,200-2,000 |
| **Enterprise (Enhanced Security)** | ✅ Achievable | + Azure Firewall Standard + NSGs | ~$1,850-2,650 |
| **Highly Regulated (Maximum Security)** | ⚠️ Achievable with Limitations | + Azure Firewall Premium + App Gateway | ~$2,477-3,297 |
| **Zero Trust / Air-Gapped** | ❌ Not Achievable | Blockers: ACS and WebRTC require internet | N/A |

---

### 4.4 Architecture Recommendations by Industry

#### Financial Services / Banking
**Security Requirements:**
- PCI-DSS compliance
- Data residency
- Audit logging
- Network isolation

**Recommended Configuration:**
- ✅ Premium ACR with Private Endpoints
- ✅ Azure Firewall Premium with TLS inspection
- ✅ Application Gateway WAF_v2
- ✅ Azure Monitor Private Link Scope
- ✅ Internal Container Apps Environment
- ⚠️ Disable ACS/PSTN features (or accept controlled internet egress)

**Estimated Cost:** ~$2,500-3,500/month

---

#### Healthcare / HIPAA
**Security Requirements:**
- HIPAA compliance
- PHI protection
- Encryption at rest and in transit
- Access logging

**Recommended Configuration:**
- ✅ Premium ACR with Private Endpoints
- ✅ Azure Firewall Standard (TLS inspection may not be required)
- ✅ Application Insights with AMPLS
- ✅ VNet integration with NSGs
- ✅ Managed Identity for all services
- ⚠️ Store Voice Live API key in Key Vault with HSM backing

**Estimated Cost:** ~$1,850-2,650/month

---

#### Government / Public Sector
**Security Requirements:**
- FedRAMP compliance (Azure Government Cloud)
- Zero Trust architecture
- Complete network isolation
- No external dependencies

**Recommended Configuration:**
- ⚠️ **Blockers:** Azure Communication Services and WebRTC require internet access
- ✅ Premium ACR with Private Endpoints
- ✅ Azure Firewall Premium
- ✅ Internal Container Apps Environment
- ❌ **Cannot use phone integration** (ACS requires internet)
- ✅ WebSocket mode only (disable WebRTC)

**Estimated Cost:** ~$2,000-2,800/month (without phone features)

**Alternative:** Use on-premises telephony gateway instead of Azure Communication Services

---

#### General Enterprise / Corporate
**Security Requirements:**
- Standard enterprise security
- Cost optimization
- Moderate network isolation

**Recommended Configuration:**
- ✅ Premium ACR with Private Endpoints
- ⚠️ Service Endpoints instead of Azure Firewall
- ✅ NSGs on all subnets
- ✅ Managed Identity for all services
- ✅ External Container Apps Environment (public ingress)

**Estimated Cost:** ~$1,200-1,800/month

---

### 4.5 Compliance Mapping

| Compliance Framework | Requirement | Current Status | Remediation |
|----------------------|-------------|----------------|-------------|
| **NIST 800-53** | IA-5: Authenticator Management | ⚠️ Partial | Migrate ACS to Managed Identity |
| **NIST 800-53** | AC-2: Account Management | ✅ Compliant | Using Entra ID |
| **NIST 800-53** | SC-7: Boundary Protection | ⚠️ Partial | Implement Azure Firewall + NSGs |
| **NIST 800-53** | SC-8: Transmission Confidentiality | ✅ Compliant | TLS 1.2+ enforced |
| **PCI-DSS v4.0** | Req 1: Network Security Controls | ⚠️ Partial | Implement VNet + Private Endpoints |
| **PCI-DSS v4.0** | Req 2: Secure Configurations | ✅ Compliant | Infrastructure as Code |
| **PCI-DSS v4.0** | Req 8: Identity Management | ⚠️ Partial | Migrate to Managed Identity |
| **HIPAA** | Access Control (164.312(a)) | ✅ Compliant | RBAC + Managed Identity |
| **HIPAA** | Transmission Security (164.312(e)) | ✅ Compliant | TLS encryption |
| **ISO 27001** | A.9: Access Control | ✅ Compliant | Entra ID + RBAC |
| **ISO 27001** | A.13: Network Security | ⚠️ Partial | Implement Private Endpoints |
| **ISO 27001** | A.18: Compliance | ✅ Compliant | Audit logs enabled |

---

### 4.6 Migration Roadmap

**Phase 1: Identity Hardening (2-3 weeks)**
- Migrate ACS to Managed Identity authentication
- Store Voice Live API key in Key Vault
- Remove API key parameters from infrastructure templates
- Update documentation with RBAC role requirements

**Phase 2: Network Foundation (3-4 weeks)**
- Deploy VNet and subnets
- Upgrade ACR to Premium SKU
- Configure Private Endpoints for ACR and Azure OpenAI
- Set up Private DNS zones

**Phase 3: Monitoring Isolation (1-2 weeks)**
- Implement Azure Monitor Private Link Scope
- Configure Private Endpoint for monitoring
- Update Container Apps to use private ingestion

**Phase 4: Network Security (2-3 weeks)**
- Deploy Network Security Groups
- Configure Service Endpoints for ACS
- Document required firewall rules
- Implement Azure Firewall (if required)

**Phase 5: Production Validation (2 weeks)**
- Test all functionality in locked-down configuration
- Validate phone integration with ACS
- Verify monitoring and logging
- Perform penetration testing (if required)

**Total Timeline:** 10-14 weeks for complete locked-down deployment

---

### 4.7 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **ACR Premium cost increase** | High | Medium | Budget approval, phased rollout |
| **Azure Firewall Premium cost** | High | High | Use Standard tier or NSGs only |
| **ACS Private Endpoint unavailable** | High | Low | Accept Service Endpoint as mitigation |
| **WebRTC public endpoint required** | High | Medium | Use WebSocket mode or accept controlled egress |
| **Migration breaks existing deployments** | Medium | High | Test in dev/staging first, use feature flags |
| **Managed Identity RBAC misconfiguration** | Medium | Medium | Document roles, use IaC, test thoroughly |
| **Private DNS misconfiguration** | Low | High | Use Azure-managed zones, automate linking |
| **Performance impact of Private Endpoints** | Low | Low | Monitor latency, optimize routing |

---

### 4.8 Monitoring and Validation

**Post-Deployment Validation Checklist:**

- [ ] Verify Managed Identity authentication for Azure OpenAI
- [ ] Confirm ACR image pulls use Private Endpoint
- [ ] Test Azure Communication Services call automation
- [ ] Validate Application Insights telemetry ingestion
- [ ] Check Private Endpoint connectivity from Container Apps
- [ ] Verify DNS resolution for Private Endpoints
- [ ] Test phone call integration (if enabled)
- [ ] Validate WebRTC browser connections (if enabled)
- [ ] Review NSG flow logs for unexpected traffic
- [ ] Confirm no credentials stored in code or configuration

**Ongoing Monitoring:**

- Monitor for credential usage (Application Insights logs)
- Track Private Endpoint health metrics
- Review NSG flow logs monthly
- Audit RBAC role assignments quarterly
- Test disaster recovery procedures semi-annually
- Review Azure service updates for new Private Endpoint support

---

## 5. Conclusion

The GPT Realtime Agents accelerator demonstrates **strong security practices** with User-Assigned Managed Identity for core services. However, achieving a **fully locked-down enterprise deployment** requires:

1. **Identity Hardening:**
   - ⚠️ Medium effort to migrate ACS to Managed Identity
   - ⚠️ Medium effort to secure Voice Live API key in Key Vault
   - ✅ Already supports Managed Identity for Azure OpenAI

2. **Network Isolation:**
   - ⚠️ Achievable with limitations (ACS and WebRTC require internet egress)
   - ✅ Fully private deployment possible in WebSocket-only mode (no phone, no WebRTC)
   - ⚠️ Requires significant SKU upgrades (ACR Premium, Azure Firewall)

3. **Cost Considerations:**
   - Baseline deployment: ~$250-500/month
   - Enterprise locked-down: ~$1,200-2,000/month
   - Maximum security: ~$2,500-3,500/month (10x increase)

**Overall Assessment:** The accelerator is **deployable in enterprise environments with controlled network egress**. A **zero-trust air-gapped deployment is not achievable** due to Azure Communication Services and WebRTC limitations. Organizations should implement **defense-in-depth** with Private Endpoints, Azure Firewall, and NSGs rather than pursuing complete network isolation.

---

## Appendix A: Quick Reference - RBAC Roles Required

| Service | Managed Identity | Required Role | Role ID |
|---------|------------------|---------------|---------|
| Azure OpenAI | audio-backend | Cognitive Services OpenAI User | 5e0bd9bd-7b93-4f28-af87-19fc36ad61bd |
| Azure Container Registry | audio-backend | AcrPull | 7f951dda-4ed3-4680-a7ca-43fe172d538d |
| Azure Communication Services | audio-backend | Azure Communication Services User | TBD |
| Application Insights | audio-backend | Monitoring Metrics Publisher | 3913510d-42f4-4e42-8a64-420c390055eb |
| Key Vault | audio-backend | Key Vault Secrets User | 4633458b-17de-408a-b874-0445c86b69e6 |

---

## Appendix B: External Service Dependencies

| Service | Endpoint Pattern | Protocol | Port | Private Endpoint Support |
|---------|------------------|----------|------|--------------------------|
| Azure OpenAI WebRTC | `<region>.realtimeapi-preview.ai.azure.com` | HTTPS | 443 | ❌ No |
| Azure OpenAI WebSocket | `<resource>.openai.azure.com` | WSS | 443 | ✅ Yes |
| Azure Communication Services API | `<resource>.communication.azure.com` | HTTPS | 443 | ❌ No (Call Automation) |
| Azure Communication Services Media | `<resource>.communication.azure.com` | WSS | 443 | ❌ No |
| Azure Container Registry | `<resource>.azurecr.io` | HTTPS | 443 | ✅ Yes (Premium) |
| Application Insights | `<region>.monitoring.azure.com` | HTTPS | 443 | ✅ Yes (AMPLS) |
| Log Analytics | `<workspace>.ods.opinsights.azure.com` | HTTPS | 443 | ✅ Yes (AMPLS) |

---

## Appendix C: Infrastructure as Code Changes Required

See separate branch `feature/locked-down-networking` for complete Bicep implementation including:

- VNet and subnet modules
- Private Endpoint modules
- Private DNS zone modules
- NSG modules
- Azure Monitor Private Link Scope
- Updated Container Apps Environment with VNet integration
- Updated Container Registry with Premium SKU
- Updated main.bicep with networking parameters

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-16  
**Review Frequency:** Quarterly  
**Next Review:** 2026-04-16
