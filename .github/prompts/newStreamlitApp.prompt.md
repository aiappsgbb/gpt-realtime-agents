---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new Streamlit application for interactive data science UIs and AI demos following best practices'
---

# Create New Streamlit Application

- Create a new Streamlit application using uv package manager under the src folder for interactive data science applications and AI demos.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-streamlit-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-streamlit-app}

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
- Review research collection findings for Streamlit/data science-specific patterns, libraries, and configurations
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
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── .streamlit/
│   │   ├── config.toml
│   │   └── secrets.toml
│   ├── pages/
│   │   ├── 1_📊_Dashboard.py
│   │   ├── 2_💬_Chat.py
│   │   ├── 3_📁_File_Upload.py
│   │   └── 4_📈_Visualization.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── upload.py
│   │   ├── visualization.py
│   │   └── sidebar.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   ├── ai_client.py
│   │   └── data_processor.py
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── images/
│   │   └── data/
│   └── examples/
│       ├── sample_data.csv
│       └── sample_config.json
```

## File Requirements

### 1. pyproject.toml

Generate a `pyproject.toml` file with the following structure:

```toml
[project]
name = "${input:appName}"
version = "0.1.0"
description = "A Streamlit application for interactive data science UIs and AI demos"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.39.0,<2.0.0",
    "pydantic>=2.9.0,<3.0.0",
    "pydantic-settings>=2.6.0,<3.0.0",
    "python-dotenv>=1.0.0,<2.0.0",
    "httpx>=0.27.0,<0.28.0",
    "azure-identity>=1.19.0,<2.0.0",
    "azure-openai>=1.50.0,<2.0.0",
    "pandas>=2.2.0,<3.0.0",
    "numpy>=1.26.0,<2.0.0",
    "plotly>=5.24.0,<6.0.0",
    "altair>=5.4.0,<6.0.0",
    "matplotlib>=3.9.0,<4.0.0",
    "seaborn>=0.13.0,<0.14.0",
    "pillow>=10.4.0,<11.0.0",
    "scikit-learn>=1.5.0,<2.0.0",
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
- Safe dependency version pinning for Streamlit and data science libraries
- Separates development dependencies into optional group
- Includes tool configurations for linting, formatting, and testing
- Compatible with uv package manager
- No build system needed for containerized applications

### 2. .python-version

Create a `.python-version` file specifying Python 3.11.

### 3. streamlit_app.py

Generate a `streamlit_app.py` file (main entry point) with:

- Main Streamlit application setup with page configuration
- Navigation sidebar with page selection
- Session state management
- Environment configuration loading
- Error handling and logging using Python's logging module (never use print statements)
- Structured logging with appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Authentication and security configurations
- Integration with Azure OpenAI or other AI services
- Custom CSS and theming
- Performance monitoring and caching

### 4. .streamlit/config.toml

Create Streamlit configuration file with:

- Server configuration (port, address, headless mode)
- Theme customization (colors, fonts, layout)
- Browser and deployment settings
- File upload limits and security settings
- Performance optimizations
- Development vs production configurations

```toml
[server]
port = 80
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"  
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[client]
toolbarMode = "minimal"
```

### 5. pages/1_📊_Dashboard.py

Create a dashboard page with:

- Overview metrics and KPIs
- Interactive charts and visualizations
- Real-time data updates
- Filtering and selection controls
- Export capabilities
- Responsive layout design

### 6. pages/2_💬_Chat.py

Create a chat interface page with:

- Chat interface using st.chat_message and st.chat_input
- Message history management with session state
- AI model integration (Azure OpenAI, OpenAI, etc.)
- Streaming response support
- Error handling for API failures
- Conversation context management
- User input validation and sanitization
- Chat history export and import

### 7. pages/3_📁_File_Upload.py

Create a file upload page with:

- File upload interface with drag-and-drop support
- Multiple file format support (CSV, Excel, JSON, images, PDFs)
- File validation and size limits
- Preview capabilities for different file types
- Batch processing support
- Secure file handling and storage
- Integration with AI services for file analysis
- Data transformation and cleaning tools

### 8. pages/4_📈_Visualization.py

Create a visualization page with:

- Interactive charts using Plotly, Altair, and matplotlib
- Real-time data visualization
- Custom chart configurations
- Export capabilities (PNG, SVG, HTML)
- Responsive design elements
- Data filtering and selection
- Statistical analysis tools

### 9. components/chat.py

Create reusable chat components with:

- Chat message rendering functions
- Conversation state management
- AI response streaming
- Message formatting and styling
- Error handling components
- Chat history persistence

### 10. components/upload.py

Create file upload components with:

- Custom file uploader with validation
- File preview components
- Progress indicators for large files
- Error handling and user feedback
- File metadata extraction
- Secure file processing utilities

### 11. components/visualization.py

Create visualization components with:

- Reusable chart functions
- Data preprocessing utilities
- Interactive plot configurations
- Custom styling and themes
- Export functionality
- Performance optimization for large datasets

### 12. components/sidebar.py

Create sidebar components with:

- Navigation menu
- Settings and configuration panels
- User authentication status
- Application state indicators
- Help and documentation links
- Theme switching controls

### 13. utils/config.py

Create a configuration module using pydantic-settings with:

- BaseSettings class for environment configuration
- Streamlit server settings (HOST, PORT, DEBUG)
- AI service configuration (API keys, endpoints, models)
- File upload settings (max size, allowed types)
- Authentication settings
- Logging configuration
- Database connection settings
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

### 14. utils/logging_config.py

Create a logging configuration module with:

- Structured logging setup for Streamlit applications
- JSON logging for production environments
- Console and file handlers
- Log rotation configuration
- Integration with Streamlit's internal logging
- Custom formatters for different environments
- Performance logging for AI operations
- Request tracking and user interaction logging

### 15. utils/ai_client.py

Create an AI client module with:

- Azure OpenAI client configuration
- OpenAI API client setup
- Request/response handling with caching
- Rate limiting and retry logic
- Error handling and fallback strategies
- Token usage tracking and monitoring
- Async support for better performance
- Model switching capabilities
- Streaming response handling

### 16. utils/data_processor.py

Create a data processing module with:

- Data cleaning and transformation utilities
- File format conversion functions
- Statistical analysis helpers
- Data validation and quality checks
- Performance optimization for large datasets
- Integration with pandas and numpy
- Custom data processing pipelines

### 17. Dockerfile

Create a multi-stage Dockerfile optimized for Streamlit with:

- Multi-stage build for smaller production images
- Python 3.11+ base image (use Azure Linux base)
- uv for fast dependency installation
- Non-root user for security
- Proper layer caching
- Health check configuration
- Streamlit-specific optimizations

```dockerfile
# Dockerfile structure for Streamlit
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
ENV STREAMLIT_SERVER_PORT=80
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/_stcore/health || exit 1

# Run Streamlit application
CMD ["uv", "run", "streamlit", "run", "streamlit_app.py"]
```

### 18. .dockerignore

Create a `.dockerignore` file to exclude:

- Development files (.git, .vscode, etc.)
- Python cache and build artifacts
- Virtual environments
- Test files and documentation
- Large model files (if any)
- IDE configuration files
- OS-specific files
- Streamlit cache directories
- Temporary upload directories

### 19. assets/css/style.css

Create custom CSS styling with:

- Modern, responsive design
- Custom component styling
- Brand colors and typography
- Mobile-friendly optimizations
- Accessibility improvements
- Dark/light theme support
- Custom animations and transitions
- Print-friendly styles

### 20. README.md

Create a comprehensive `README.md` for the Streamlit app with:

- Project description and use cases
- Prerequisites (Python 3.11+, uv, Docker, AI service accounts)
- Installation instructions using uv
- Development setup and local running
- Configuration guide (API keys, environment variables, secrets.toml)
- Running the application (local and Docker)
- Docker build and run instructions
- Deployment options (Azure Container Apps, Streamlit Cloud)
- Multi-page application structure explanation
- API documentation and usage examples
- Customization guide (themes, components, layouts)
- Security considerations and best practices
- Performance optimization tips
- Troubleshooting common issues

**Local Development section**:
```markdown
## Local Development

### Running Locally
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables in `.streamlit/secrets.toml`:
   ```toml
   AZURE_OPENAI_ENDPOINT = "your-endpoint"
   AZURE_OPENAI_API_KEY = "your-key"
   ```

3. Run the application:
   ```bash
   uv run streamlit run streamlit_app.py
   ```

The application will be available at `http://localhost:8501`
```

### 21. examples/sample_data.csv

Create sample data files with:

- Example datasets for testing visualizations
- Demo data for chat interactions
- Sample file formats for upload testing
- Configuration examples
- Test scenarios and use cases

### 22. Azure Developer CLI Configuration

Update the root `azure.yaml` file to include the new Streamlit application as a service:

- Add a new service entry under the `services` section
- Configure the service with:
  - Service name: "${input:appName}"
  - Language: python
  - Host: containerapp
  - Docker configuration with:
    - Remote builds enabled: `remoteBuild: true`
  - Environment variables for AI service integration and Azure Monitor
  - **Critical**: Always include `AZURE_CLIENT_ID` environment variable for managed identity authentication
  - Port configuration for Streamlit server (port 80 for Azure Container Apps)
- Ensure proper service dependencies if needed
- Configure resource group and location references
- Add ingress configuration for external access
- Configure scaling rules for traffic management

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

### 23. Infrastructure Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for all infrastructure changes.

Update the `infra/main.bicep` file to include a new container app module for the Streamlit application:

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
  - Environment variables specific to the Streamlit application
  - Resource allocation (CPU and memory)
  - Container port (80 for Azure Container Apps)

Example module configuration:
```bicep
// ${input:appName} Streamlit Application
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
        name: 'STREAMLIT_SERVER_PORT'
        value: '80'
      }
      {
        name: 'STREAMLIT_SERVER_ADDRESS'
        value: '0.0.0.0'
      }
      {
        name: 'STREAMLIT_SERVER_HEADLESS'
        value: 'true'
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
@description('Container image for ${input:appName} Streamlit application')
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

- Use modern Python 3.11+ features with type hints
- Follow Streamlit best practices and latest API
- Implement proper configuration management with pydantic-settings
- Include comprehensive type definitions throughout
- Production-ready error handling and logging
- Environment-based configuration with secrets management
- Clean, maintainable code structure with reusable components
- Docker containerization ready for Azure Container Apps
- Multi-stage builds for optimization
- Security best practices (input validation, sanitization, HTTPS)
- Responsive UI design with mobile support
- Proper logging configuration using Python's logging module
- Structured logging with JSON format for production environments
- Never use print() statements for application output
- Async support for better performance where applicable
- Integration with Azure AI services using managed identities
- Session state management for user interactions
- File upload security and validation with size limits
- Rate limiting and usage tracking for AI services
- Accessibility compliance (WCAG guidelines)
- Performance monitoring and optimization with caching
- Error boundaries and graceful degradation
- Multi-page application architecture
- Custom CSS and theming support
- Data visualization best practices
- Scalable architecture for large datasets
- Progressive web app features (optional)
- SEO optimization for public applications