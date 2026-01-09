# GitHub Copilot Instructions

This repository contains prompt files to help with common development tasks using GitHub Copilot.

## Available Prompts

### Application Creation
- **Python App**: `/newPythonApp` - Create a new Python FastAPI application with uv package manager under src/
- **Node.js/TypeScript App**: `/newNodeApp` - Create a new Node.js/TypeScript Express application under src/
- **.NET Web API**: `/newDotNetApp` - Create a new ASP.NET Core Web API application with .NET 9 under src/
- **React App**: `/newReactApp` - Create a new React + Vite + Tailwind CSS application under src/
- **Gradio App**: `/newGradioApp` - Create a new Gradio application for interactive UIs and AI demos under src/
- **Streamlit App**: `/newStreamlitApp` - Create a new Streamlit application for data science UIs and AI demos under src/
- **Agent App**: `/newAgentApp` - Create a new AI agent application using Microsoft Agent Framework under src/

### Infrastructure & Configuration
- **Setup Infrastructure**: `/setupInfra` - Configure main.bicep with all relevant Azure modules
- **Add AZD Service**: `/addAzdService` - Add a new service configuration to azure.yaml

### Best Practices Documentation
- **[Azure Best Practices](azure-bestpractices.md)** - Security guidelines enforcing zero API keys policy
- **[Bicep Deployment Best Practices](bicep-deployment-bestpractices.md)** - Infrastructure as Code guidelines for azd integration

### Documentation & Compliance
- **Create README**: `/newReadme` - Generate a comprehensive README with standard IP structure
- **IP Compliance**: `/ipCompliance` - Comprehensive compliance assessment for Azure Developer CLI templates

## Usage

Type the prompt command in any chat or inline chat session with GitHub Copilot to execute the corresponding task.

Examples:
```
/newPythonApp
/newNodeApp
/newDotNetApp
/newReactApp
/newGradioApp
/newStreamlitApp
/newAgentApp
/setupInfra
/addAzdService
/newReadme
/ipCompliance
```

## Prompt Files Location

All prompt files are located in `.github/prompts/` directory:
- `newPythonApp.prompt.md` - Python FastAPI application creation
- `newNodeApp.prompt.md` - Node.js/TypeScript Express application creation
- `newDotNetApp.prompt.md` - ASP.NET Core Web API application creation
- `newReactApp.prompt.md` - React + Vite + Tailwind CSS application creation
- `newGradioApp.prompt.md` - Gradio application creation for interactive UIs
- `newStreamlitApp.prompt.md` - Streamlit application creation for data science UIs
- `newAgentApp.prompt.md` - Microsoft Agent Framework application creation
- `setupInfra.prompt.md` - Infrastructure setup with Bicep
- `addAzdService.prompt.md` - Azure Developer CLI service configuration
- `newReadme.prompt.md` - README file generation
- `ipCompliance.prompt.md` - IP compliance validation and assessment

## Customization

Each prompt file can be customized to match your specific project requirements and coding standards. The prompts are designed to work with the existing repository structure and Azure infrastructure templates.

## Development Standards

When using these prompts, ensure adherence to the following standards:

### Logging & Error Handling
- **Logging**: Always use proper logging modules (Python's `logging`, Node.js `winston`) - never use `print()` or `console.log()` in production code
- **Structured Logging**: Use JSON format for production environments with appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Error Handling**: Implement structured error handling with meaningful error messages and proper exception handling
- **Observability**: Include OpenTelemetry tracing for distributed systems and performance monitoring

### Code Quality & Security
- **Type Safety**: Use TypeScript for Node.js/React applications and type hints throughout Python code
- **Linting & Formatting**: Configure ESLint/Prettier for TypeScript, Ruff/Black for Python
- **Testing**: Include comprehensive test coverage with Jest (Node.js/React) or pytest (Python)
- **Security**: Implement security best practices including input validation, sanitization, and proper authentication
- **Dependency Management**: Use safe version pinning (>= and < operators) to prevent major version upgrades

### Azure Integration
- **Authentication**: Use ChainedTokenCredential with AzureDeveloperCliCredential + ManagedIdentityCredential pattern
- **Environment Variables**: Always include `AZURE_CLIENT_ID` for managed identity authentication in Azure Container Apps
- **Configuration**: Always update `azure.yaml` when creating new applications to ensure proper deployment configuration
- **Infrastructure**: Update `infra/main.bicep` with new container app modules and proper parameter configuration
- **Monitoring**: Integrate Application Insights with OpenTelemetry for comprehensive observability
- **Security**: **NEVER use API keys** - follow [Azure Best Practices](./azure-bestpractices.md) for secure authentication

### Containerization
- **Multi-stage Builds**: Use optimized Dockerfiles with multi-stage builds for smaller production images
- **Base Images**: Use Azure Linux base images (mcr.microsoft.com/azurelinux/base/*)
- **Security**: Run containers as non-root user with proper health checks
- **Port Configuration**: Use port 80 for Azure Container Apps deployment

### Development Experience
- **Package Managers**: Use uv for Python, npm for Node.js/React applications
- **Environment Management**: Include .python-version (Python) and .nvmrc (Node.js) files
- **Documentation**: Provide comprehensive README files with setup, configuration, and deployment instructions
- **Git Workflow**: Create feature branches with descriptive names (feature/add-{app-name})

### Application Architecture
- **Clean Structure**: Follow modular architecture with clear separation of concerns
- **Configuration Management**: Use pydantic-settings (Python) or environment-based config (Node.js)
- **API Design**: Follow RESTful principles with proper HTTP status codes and error responses
- **Performance**: Implement caching strategies and async patterns where appropriate