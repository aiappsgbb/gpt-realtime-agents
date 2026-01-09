---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new Python application using uv package manager following best practices and a simplified structure.'
---

# Create New Python Application

- Create a new Python application using uv package manager under the src folder with a simplified structure.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-python-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-python-app}

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
- Review research collection findings for FastAPI/Python-specific patterns, libraries, and configurations
- Use consolidated environment variables from collection template
- Reference code snippets from findings for implementation
- Validate against research gaps identified in collection phase

---

## Directory Structure

Create the following directory structure:

```text
src/
├── ${input:appName}/
│   ├── pyproject.toml
│   ├── README.md
│   ├── .python-version
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── gunicorn.conf.py
│   ├── __init__.py
│   ├── main.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── tracing.py
```

## File Requirements

### 1. pyproject.toml

Generate a `pyproject.toml` file with the following structure:

```toml
[project]
name = "${input:appName}"
version = "0.1.0"
description = "A FastAPI application built with modern Python practices"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0,<0.116.0",
    "uvicorn>=0.32.0,<0.33.0",
    "gunicorn>=23.0.0,<24.0.0",
    "pydantic>=2.9.0,<3.0.0",
    "pydantic-settings>=2.6.0,<3.0.0",
    "httpx>=0.27.0,<0.28.0",
    "python-dotenv>=1.0.0,<2.0.0",
    "azure-identity>=1.19.0,<2.0.0",
    "opentelemetry-api>=1.27.0,<2.0.0",
    "opentelemetry-sdk>=1.27.0,<2.0.0",
    "opentelemetry-instrumentation-fastapi>=0.48.0,<0.49.0",
    "opentelemetry-instrumentation-httpx>=0.48.0,<0.49.0",
    "azure-monitor-opentelemetry-exporter>=1.0.0,<2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0,<9.0.0",
    "pytest-asyncio>=0.24.0,<0.25.0",
    "black>=24.10.0,<25.0.0",
    "ruff>=0.7.0,<0.8.0",
    "mypy>=1.11.0,<2.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
asyncio_mode = "auto"
```

Key features of this configuration:
- Uses modern `[project]` table format for metadata
- Safe dependency version pinning to prevent major version upgrades
- Separates development dependencies into optional group
- Includes tool configurations for linting, formatting, and testing
- Compatible with uv package manager

### 2. .python-version

Create a `.python-version` file specifying Python 3.11.

### 3. main.py

Generate a `main.py` file with:

- A basic FastAPI application
- Health check endpoint for container monitoring
- Configuration loading using utils.config
- OpenTelemetry tracing integration using utils.tracing
- Proper async/await patterns
- Error handling and logging using Python's logging module (never use print statements)
- Structured logging with appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- CORS middleware configuration
- Uvicorn server configuration for containerization
- Tracing instrumentation for requests and external calls

### 4. Dockerfile

Create a multi-stage Dockerfile optimized for FastAPI with:

- Multi-stage build for smaller production images
- Python 3.11+ base image
- uv for fast dependency installation
- Non-root user for security
- Proper layer caching
- Health check configuration
- Production-ready settings

```dockerfile
# Dockerfile typical structure
FROM mcr.microsoft.com/azurelinux/base/python:3.12
WORKDIR /app

# Install CA certificates
RUN tdnf install -y ca-certificates && \
    update-ca-trust enable && \
    update-ca-trust extract && \
    tdnf clean all

# Set SSL_CERT_FILE for Python
ENV SSL_CERT_FILE=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --locked --no-dev

# Copy application code
COPY . .

# Expose port 80 for Azure Container Apps
EXPOSE 80

# Set environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# CHANGE AS APPROPRIATE
CMD ["uv", "run", "--", "gunicorn", "-c", "gunicorn.conf.py", "main:app"]
```

### 5. gunicorn.conf.py

Create a production-ready Gunicorn configuration file with:

- Bind to 0.0.0.0:80 for Azure Container Apps
- Worker process configuration based on CPU cores
- Worker class: uvicorn.workers.UvicornWorker for ASGI support
- Timeout settings for production workloads
- Logging configuration with structured JSON logs
- Preload application for better performance
- Keep-alive settings for connection reuse
- Security headers and configuration
- Error handling and graceful shutdowns

Example configuration:
```python
# gunicorn.conf.py
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:80"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
keepalive = 2

# Application
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()
access_log_format = '{\"time\": \"%(t)s\", \"method\": \"%(m)s\", \"url\": \"%(U)s\", \"status\": %(s)s, \"response_time\": %(D)s, \"user_agent\": \"%(a)s\"}'

# Process naming
proc_name = "fastapi-app"
```

### 6. .dockerignore

Create a `.dockerignore` file to exclude:

- Development files (.git, .vscode, etc.)
- Python cache and build artifacts
- Virtual environments
- Test files and documentation
- IDE configuration files
- OS-specific files

### 7. utils/config.py

Create a configuration module using pydantic-settings with:

- BaseSettings class for environment configuration
- Common settings like HOST, PORT, DEBUG, LOG_LEVEL
- Azure Monitor configuration (APPLICATION_INSIGHTS_CONNECTION_STRING)
- Database and API configuration placeholders
- OpenTelemetry tracing settings
- Proper type hints and defaults
- Environment variable loading
- DO REMEMBER to invoke load_dotenv(override=True) at the beginning!
- Azure credential management using ChainedTokenCredential best practice
- **CRITICAL**: Follow [Azure Best Practices](../azure-bestpractices.md) - NEVER use API keys for Azure services

Include a standard Azure credential helper function:
```python
from azure.identity import AzureDeveloperCliCredential, ManagedIdentityCredential, ChainedTokenCredential

def get_azure_credential() -> ChainedTokenCredential:
    """Get Azure credential using best practice chain.
    
    Returns:
        ChainedTokenCredential that tries Azure Developer CLI first, then Managed Identity.
        This works for both local development (azd) and production (Container Apps).
    """
    return ChainedTokenCredential(
        AzureDeveloperCliCredential(),  # tries Azure Developer CLI (azd) for local development
        ManagedIdentityCredential()     # fallback to managed identity for production
    )
```

This approach provides:
- Seamless local development experience (works with azd specifically)
- Production readiness (automatically uses managed identity in Azure Container Apps)
- No credential configuration needed
- Consistent authentication pattern across all Azure services

**Important**: Always ensure `AZURE_CLIENT_ID` environment variable is set in Azure Container Apps to specify which managed identity to use for authentication.

### 8. utils/tracing.py

Create an OpenTelemetry tracing module with:

- Azure Monitor OpenTelemetry exporter configuration
- FastAPI automatic instrumentation setup
- HTTPx instrumentation for external API calls
- Resource configuration with service name and version
- Trace provider initialization using config settings
- Custom trace decorators for business logic
- Error handling for tracing setup
- Integration with utils.config for configuration management

### 9. README.md

Create a comprehensive `README.md` for the Python app with:

- Project description
- Prerequisites (Python 3.11+, uv, Docker, Azure Application Insights)
- Installation instructions using uv
- Development setup
- Running the application (local and Docker)
- Docker build and run instructions
- Configuration options (including Azure Monitor setup)
- API documentation
- Container deployment guidance
- Monitoring and observability setup
- Azure Application Insights configuration

### 10. Package Structure

Include proper Python package structure with `__init__.py` files in:

- Root application directory
- utils/ directory (with config.py and tracing.py)

### 11. Azure Developer CLI Configuration

Update the root `azure.yaml` file to include the new Python application as a service:

- Add a new service entry under the `services` section
- Configure the service with:
  - Service name: "${input:appName}"
  - Language: python
  - Host: containerapp
  - Docker configuration with:
    - Remote builds enabled: `remoteBuild: true`
  - Environment variables for Azure Monitor integration
  - **Critical**: Always include `AZURE_CLIENT_ID` environment variable for managed identity authentication
- Ensure proper service dependencies if needed
- Configure resource group and location references
- Add any required environment-specific configurations

Example service configuration:
```yaml
services:
  ${input:appName}:
    project: "./src/${input:appName}"
    language: python
    host: containerapp
    docker:
      remoteBuild: true
```

### 17. Infrastructure Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for all infrastructure changes.

Update the `infra/main.bicep` file to include a new container app module for the FastAPI application:

- Add a new module declaration using the `infra/core/host/container-app.bicep` template
- Configure the module with:
  - Unique name for the container app (based on app name and environment)
  - Location parameter reference
  - Tags from the main template
  - Container Apps Environment ID reference
  - Container Registry name reference
  - User Assigned Identity ID for ACR access
  - Managed Identity Principal ID for RBAC
  - GitHub Actions parameter for deployment context
  - Container image parameter (will be updated during deployment)
  - Environment variables specific to the Python application
  - Resource allocation (CPU and memory)
  - Container port (typically 80 for FastAPI apps)

Example module configuration:
```bicep
// ${input:appName} Application
module ${input:appName}App 'core/host/container-app.bicep' = {
  name: '${input:appName}-app'
  params: {
    name: '${abbrs.appContainerApps}${input:appName}-${environmentName}'
    location: location
    tags: tags
    containerAppsEnvironmentId: containerAppsEnvironment.outputs.id
    containerRegistryName: containerRegistry.outputs.name
    userAssignedIdentityId: userAssignedIdentity.outputs.id
    managedIdentityPrincipalId: principalId
    githubActions: githubActions
    containerImage: ${input:appName}AppImage
    containerPort: 80
    environmentVariables: [
      {
        name: 'AZURE_CLIENT_ID'
        value: userAssignedIdentity.outputs.clientId
      }
      {
        name: 'APPLICATION_INSIGHTS_CONNECTION_STRING'
        value: monitoring.outputs.applicationInsightsConnectionString
      }
      {
        name: 'AZURE_KEY_VAULT_ENDPOINT'
        value: keyVault.outputs.endpoint
      }
      {
        name: 'LOG_LEVEL'
        value: 'INFO'
      }
    ]
    resources: {
      cpu: 1
      memory: '2Gi'
    }
  }
}
```

- Add a parameter for the container image at the top of main.bicep:
```bicep
@description('Container image for ${input:appName} application')
param ${input:appName}AppImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
```

- Add output values for the new container app:
```bicep
// ${input:appName} App Outputs
output ${upper(replace("${input:appName}", '-', '_'))}_APP_ENDPOINT string = ${input:appName}App.outputs.fqdn
output ${upper(replace("${input:appName}", '-', '_'))}_APP_NAME string = ${input:appName}App.outputs.name
output ${upper(replace("${input:appName}", '-', '_'))}_APP_ID string = ${input:appName}App.outputs.id
```

## Technical Requirements

- Use modern Python 3.11+ features
- Follow FastAPI best practices
- Implement proper configuration management
- Include type hints throughout
- Production-ready error handling
- Environment-based configuration
- Clean, maintainable code structure
- Docker containerization ready
- Multi-stage builds for optimization (if applicable)
- Security best practices (non-root user)
- Proper logging configuration using Python's logging module
- Never use print() statements for application output
- Azure Monitor integration via OpenTelemetry
- Distributed tracing for microservices
- Observability and monitoring ready
- Performance tracking and metrics
- Safe dependency versioning (use >= and < operators to prevent major version upgrades)
- Production-ready ASGI server configuration with Gunicorn
- Scalable worker process management
- Graceful shutdown handling
