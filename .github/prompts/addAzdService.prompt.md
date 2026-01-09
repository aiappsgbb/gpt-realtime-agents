## Research Context (Optional - If Available)

If research planning and collection templates were completed prior to this task, reference them here for implementation guidance:

**Plan File Used**: ${input:planFile:[plan filename or N/A]}
**Collection File Used**: ${input:collectionFile:[collection filename or N/A]}
**Date**: [YYYY-MM-DD]
**Collector**: ${input:collector:[Agent/User or N/A]}
**Initial Prompt (verbatim)**: ${input:initialPrompt:[original research question or N/A]}
**Referenced Research Plan**: ${input:researchPlan:[plan filename or N/A]}

**Research Artifacts Location**: 
- Plan: `.github/scratchpad/research-plan-[TIMESTAMP].md` (if exists)
- Collection: `.github/scratchpad/research-collection-[TIMESTAMP].md` (if exists)

**Implementation Notes**: 
- Review research collection findings for Azure service configuration, environment variables, and CLI integration
- Use consolidated environment variables from collection template
- Reference code snippets from findings for service addition
- Validate against research gaps identified in collection phase

---
# Add New Azure Developer CLI Service
---
mode: 'agent'
model: Auto (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'runCommands']
description: 'Add a new service to azure.yaml configuration'
---

# Add Service to Azure Developer CLI Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for infrastructure updates.

Add a new service to the `azure.yaml` file for deployment with Azure Developer CLI.

## Service Configuration Requirements

Update the root `azure.yaml` file to include a new service entry with the following structure:

### Basic Service Entry

Add to the `services` section:

```yaml
services:
  <service-name>:
    language: <python|js|dotnet>
    host: containerapp
    docker:
      path: ./src/<service-directory>
      context: ./src/<service-directory>
```

### Language-Specific Configurations

#### Python Services (FastAPI, Gradio, Flask)
```yaml
services:
  my-python-app:
    project: "./src/my-python-app"
    language: python
    host: containerapp
    docker:
      registry: "${AZURE_CONTAINER_REGISTRY_ENDPOINT}"
      remoteBuild: true
      buildArgs:
        - "--platform=linux/amd64"
    env:
      - AZURE_OPENAI_ENDPOINT
      - APPLICATION_INSIGHTS_CONNECTION_STRING
      - AZURE_CLIENT_ID  # REQUIRED for managed identity
      - LOG_LEVEL

# ⚠️ SECURITY: Follow Azure Best Practices
# NEVER include API keys in environment variables:
# ❌ AZURE_OPENAI_API_KEY (FORBIDDEN)
# ❌ AZURE_AI_SEARCH_KEY (FORBIDDEN)
# See: ../azure-bestpractices.md
```

#### Node.js/TypeScript Services
```yaml
services:
  my-node-app:
    project: "./src/my-node-app"
    language: js
    host: containerapp
    docker:
      registry: "${AZURE_CONTAINER_REGISTRY_ENDPOINT}"
      remoteBuild: true
      buildArgs:
        - "--platform=linux/amd64"
    env:
      - NODE_ENV
      - PORT
      - LOG_LEVEL
      - APPLICATION_INSIGHTS_CONNECTION_STRING
```

#### Gradio Applications
```yaml
services:
  my-gradio-app:
    project: "./src/my-gradio-app"
    language: python
    host: containerapp
    docker:
      registry: "${AZURE_CONTAINER_REGISTRY_ENDPOINT}"
      remoteBuild: true
      buildArgs:
        - "--platform=linux/amd64"
    env:
      - AZURE_OPENAI_ENDPOINT
      - AZURE_OPENAI_API_KEY
      - GRADIO_SERVER_PORT=7860
      - GRADIO_SERVER_NAME=0.0.0.0
      - APPLICATION_INSIGHTS_CONNECTION_STRING
```

### Environment Variables

Include common environment variables that should be available to the service:

#### AI/ML Services
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `AZURE_AI_SEARCH_ENDPOINT`
- `AZURE_AI_SEARCH_KEY`

#### Monitoring & Observability
- `APPLICATION_INSIGHTS_CONNECTION_STRING`
- `AZURE_MONITOR_CONNECTION_STRING`
- `LOG_LEVEL`

#### Database & Storage
- `AZURE_COSMOS_DB_ENDPOINT`
- `AZURE_STORAGE_ACCOUNT_NAME`
- `AZURE_KEY_VAULT_ENDPOINT`

#### Service Configuration
- `PORT` (for Node.js services)
- `HOST` (if needed)
- `DEBUG` (for development)
- `NODE_ENV` (for Node.js)

### Service Dependencies

If the service depends on other infrastructure components, add dependencies:

```yaml
services:
  my-app:
    language: python
    host: containerapp
    docker:
      path: ./src/my-app
    depends:
      - ai-search
      - cosmos-db
      - key-vault
```

### Ingress Configuration

For services that need external access (like Gradio UIs):

```yaml
services:
  my-gradio-app:
    language: python
    host: containerapp
    docker:
      path: ./src/my-gradio-app
    env:
      - GRADIO_SERVER_PORT=7860
    # Ingress will be configured automatically by AZD for container apps
```

### Resource Scaling

For services with specific scaling requirements:

```yaml
services:
  my-api:
    language: python
    host: containerapp
    docker:
      path: ./src/my-api
    env:
      - MIN_REPLICAS=1
      - MAX_REPLICAS=10
      - CPU_REQUESTS=0.25
      - MEMORY_REQUESTS=0.5Gi
```

## Validation Steps

After adding the service configuration:

1. **Syntax Check**: Ensure the YAML syntax is valid
2. **Environment Variables**: Verify all required environment variables are included
3. **Path Validation**: Confirm the Docker path points to the correct directory
4. **Dependencies**: Check that any service dependencies are properly configured
5. **Resource Names**: Ensure service names follow Azure naming conventions (lowercase, alphanumeric, hyphens)

## Integration with Infrastructure

The service configuration should align with the Bicep infrastructure templates:

- Container Apps environment in `infra/core/host/container-apps-environment.bicep`
- Container App deployment in `infra/core/host/container-app.bicep`
- Environment variables sourced from Key Vault or App Configuration
- Proper RBAC permissions for accessing Azure services

## Best Practices

- Use descriptive service names that match the application purpose
- Group related environment variables together
- Include only necessary environment variables to minimize configuration drift
- Use consistent naming conventions across all services
- Document any non-standard configurations
- Ensure environment variables are properly secured (use Key Vault references)
- Test the configuration with `azd up` in a development environment

## Example Complete Service Addition

```yaml
services:
  chat-assistant:
    language: python
    host: containerapp
    docker:
      path: ./src/chat-assistant
      context: ./src/chat-assistant
    env:
      - AZURE_OPENAI_ENDPOINT
      - AZURE_OPENAI_API_KEY
      - AZURE_OPENAI_DEPLOYMENT_NAME
      - APPLICATION_INSIGHTS_CONNECTION_STRING
      - LOG_LEVEL=INFO
      - GRADIO_SERVER_PORT=7860
    depends:
      - openai
      - monitoring
```

This configuration creates a Gradio-based chat assistant service that depends on OpenAI and monitoring infrastructure, with all necessary environment variables for Azure integration.