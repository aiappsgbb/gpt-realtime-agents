---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new Gradio application for interactive UIs and AI demos following best practices'
---

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
- Review research collection findings for Gradio UI patterns, AI demo integration, and configuration
- Use consolidated environment variables from collection template
- Reference code snippets from findings for implementation
- Validate against research gaps identified in collection phase

---
# Create New Gradio Application

- Create a new Gradio application using uv package manager under the src folder for interactive user interfaces and AI demos.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-gradio-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-gradio-app}

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
│   ├── __init__.py
│   ├── app.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── upload.py
│   │   └── visualization.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── ai_client.py
│   ├── assets/
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── images/
│   └── examples/
│       └── sample_data.json
```

## File Requirements

### 1. pyproject.toml

Generate a `pyproject.toml` file with the following structure:

```toml
[project]
name = "${input:appName}"
version = "0.1.0"
description = "A Gradio application for interactive UIs and AI demos"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
dependencies = [
    "gradio>=5.0.0,<6.0.0",
    "pydantic>=2.9.0,<3.0.0",
    "pydantic-settings>=2.6.0,<3.0.0",
    "python-dotenv>=1.0.0,<2.0.0",
    "httpx>=0.27.0,<0.28.0",
    "azure-identity>=1.19.0,<2.0.0",
    "azure-openai>=1.50.0,<2.0.0",
    "openai>=1.51.0,<2.0.0",
    "numpy>=1.26.0,<2.0.0",
    "pandas>=2.2.0,<3.0.0",
    "pillow>=10.4.0,<11.0.0",
    "matplotlib>=3.9.0,<4.0.0",
    "plotly>=5.24.0,<6.0.0",
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
- Safe dependency version pinning for Gradio and AI libraries
- Separates development dependencies into optional group
- Includes tool configurations for linting, formatting, and testing
- Compatible with uv package manager
- No build system needed for containerized applications

### 2. .python-version

Create a `.python-version` file specifying Python 3.11.

### 3. app.py

Generate an `app.py` file with:

- Main Gradio application setup
- Multiple interface tabs (Chat, File Upload, Visualization)
- Custom CSS styling integration
- Environment configuration loading
- Error handling and logging using Python's logging module (never use print statements)
- Structured logging with appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Authentication and security configurations
- Server launch configuration for containerization
- Integration with Azure OpenAI or other AI services

### 4. components/chat.py

Create a chat component module with:

- Chat interface using gr.ChatInterface or custom components
- Message history management
- AI model integration (Azure OpenAI, OpenAI, etc.)
- Streaming response support
- Error handling for API failures
- Conversation context management
- User input validation and sanitization

### 5. components/upload.py

Create a file upload component module with:

- File upload interface with supported formats
- File validation and size limits
- Processing for different file types (text, images, PDFs, etc.)
- Preview capabilities
- Batch processing support
- Secure file handling
- Integration with AI services for file analysis

### 6. components/visualization.py

Create a visualization component module with:

- Data visualization using matplotlib, plotly, or similar
- Interactive charts and graphs
- Real-time data updates
- Export capabilities
- Responsive design elements
- Custom styling options

### 7. utils/config.py

Create a configuration module using pydantic-settings with:

- BaseSettings class for environment configuration
- Gradio server settings (HOST, PORT, DEBUG, SHARE)
- AI service configuration (API keys, endpoints, models)
- File upload settings (max size, allowed types)
- Authentication settings
- Logging configuration
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

### 8. utils/logging_config.py

Create a logging configuration module with:

- Structured logging setup for Gradio applications
- JSON logging for production environments
- Console and file handlers
- Log rotation configuration
- Integration with Gradio's internal logging
- Custom formatters for different environments
- Performance logging for AI operations

### 9. utils/ai_client.py

Create an AI client module with:

- Azure OpenAI client configuration
- OpenAI API client setup
- Request/response handling
- Rate limiting and retry logic
- Error handling and fallback strategies
- Token usage tracking
- Async support for better performance
- Model switching capabilities

### 10. Dockerfile

Create a multi-stage Dockerfile optimized for Gradio with:

- Multi-stage build for smaller production images
- Python 3.11+ base image (use Azure Linux base)
- uv for fast dependency installation
- Non-root user for security
- Proper layer caching
- Health check configuration
- Gradio-specific optimizations
- GPU support (optional)

```dockerfile
# Dockerfile structure for Gradio
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

# Expose port 7860 for Gradio (or 80 for Azure Container Apps)
EXPOSE 80

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=80

WORKDIR /app

# Run Gradio application
CMD ["uv", "run", "python", "app.py"]
```

### 11. .dockerignore

Create a `.dockerignore` file to exclude:

- Development files (.git, .vscode, etc.)
- Python cache and build artifacts
- Virtual environments
- Test files and documentation
- Large model files (if any)
- IDE configuration files
- OS-specific files
- Temporary upload directories

### 12. assets/css/custom.css

Create custom CSS styling with:

- Modern, responsive design
- Dark/light theme support
- Brand colors and typography
- Component spacing and layout
- Mobile-friendly optimizations
- Accessibility improvements
- Custom animations and transitions

### 13. README.md

Create a comprehensive `README.md` for the Gradio app with:

- Project description and use cases
- Prerequisites (Python 3.11+, uv, Docker, AI service accounts)
- Installation instructions using uv
- Development setup
- Configuration guide (API keys, environment variables)
- Running the application (local and Docker)
- Docker build and run instructions
- Deployment options (Azure Container Apps, Hugging Face Spaces)
- API documentation and usage examples
- Customization guide
- Security considerations
- Performance optimization tips

### 14. examples/sample_data.json

Create sample data file with:

- Example inputs for testing
- Demo conversation flows
- Sample file formats
- Configuration examples
- Test scenarios

### 15. Azure Developer CLI Configuration

Update the root `azure.yaml` file to include the new Gradio application as a service:

- Add a new service entry under the `services` section
- Configure the service with:
  - Service name: "${input:appName}"
  - Language: python
  - Host: containerapp
  - Docker configuration with:
    - Remote builds enabled: `remoteBuild: true`
  - Environment variables for AI service integration and Azure Monitor
  - **Critical**: Always include `AZURE_CLIENT_ID` environment variable for managed identity authentication
  - Port configuration for Gradio server (port 80 for Azure Container Apps)
- Ensure proper service dependencies if needed
- Configure resource group and location references
- Add ingress configuration for external access
- Configure scaling rules for traffic management
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

### 16. Infrastructure Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for all infrastructure changes.

Update the `infra/main.bicep` file to include a new container app module for the Gradio application:

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
  - Environment variables specific to the Gradio application
  - Resource allocation (CPU and memory)
  - Container port (80 for Azure Container Apps)

Example module configuration:
```bicep
// ${input:appName} Gradio Application
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
        name: 'GRADIO_SERVER_NAME'
        value: '0.0.0.0'
      }
      {
        name: 'GRADIO_SERVER_PORT'
        value: '80'
      }
      {
        name: 'LOG_LEVEL'
        value: 'INFO'
      }
    ]
    resources: {
      cpu: 2
      memory: '4Gi'
    }
  }
}
```

- Add a parameter for the container image at the top of main.bicep:
```bicep
@description('Container image for ${input:appName} Gradio application')
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
- Follow Gradio best practices and latest API
- Implement proper configuration management
- Include type hints throughout
- Production-ready error handling
- Environment-based configuration
- Clean, maintainable code structure
- Docker containerization ready
- Multi-stage builds for optimization
- Security best practices (input validation, sanitization)
- Responsive UI design
- Proper logging configuration using Python's logging module
- Structured logging with JSON format for production environments
- Never use print() statements for application output
- Async support for better performance
- Integration with Azure AI services
- Authentication and authorization support
- File upload security and validation
- Rate limiting and usage tracking
- Accessibility compliance (WCAG guidelines)
- Mobile-responsive design
- Performance monitoring and optimization
- Error boundaries and graceful degradation
- Internationalization support (optional)
- Progressive web app features (optional)