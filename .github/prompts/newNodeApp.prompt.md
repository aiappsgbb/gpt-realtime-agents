---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new Node.js/TypeScript application following best practices and a simplified structure'
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
- Review research collection findings for Node.js/TypeScript API patterns, libraries, and configurations
- Use consolidated environment variables from collection template
- Reference code snippets from findings for implementation
- Validate against research gaps identified in collection phase

---

# Create New Node.js/TypeScript Application

- Create a new Node.js/TypeScript application under the src folder with a simplified structure.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-node-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-node-app}

## Directory Structure

Create the following directory structure:
```text
src/
├── ${input:appName}/
│   ├── package.json
│   ├── tsconfig.json
│   ├── .nvmrc
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── README.md
│   ├── src/
│   │   ├── index.ts
│   │   ├── app.ts
│   │   ├── routes/
│   │   │   └── health.ts
│   │   ├── middleware/
│   │   │   └── errorHandler.ts
│   │   └── utils/
│   │       ├── config.ts
│   │       └── logger.ts
│   ├── tests/
│   │   └── app.test.ts
│   └── dist/ (build output)
```

## File Requirements

### 1. package.json
   Generate a `package.json` file with:

- Project metadata (name: "${input:appName}", version, description, author)
- Node.js engine requirement (>=18.0.0)
- Scripts for build, start, dev, test, lint, format
- Dependencies with safe version pinning (no major version upgrades):
  - express>=4.19.0,<5.0.0, cors>=2.8.0,<3.0.0, helmet>=7.1.0,<8.0.0
  - dotenv>=16.4.0,<17.0.0, winston>=3.14.0,<4.0.0 (for structured logging)
- Azure integration dependencies:
  - @azure/identity>=4.4.0,<5.0.0, @azure/monitor-opentelemetry>=1.7.0,<2.0.0
- OpenTelemetry dependencies:
  - @opentelemetry/api>=1.9.0,<2.0.0, @opentelemetry/sdk-node>=0.54.0,<0.55.0
  - @opentelemetry/instrumentation-express>=0.42.0,<0.43.0
- DevDependencies: typescript>=5.6.0,<6.0.0, @types/node>=18.19.0,<19.0.0, @types/express>=4.17.0,<5.0.0, ts-node>=10.9.0,<11.0.0, nodemon>=3.1.0,<4.0.0, jest>=29.7.0,<30.0.0, @types/jest>=29.5.0,<30.0.0, eslint>=8.57.0,<9.0.0, prettier>=3.3.0,<4.0.0

### 2. tsconfig.json

Create a `tsconfig.json` with:

- Modern TypeScript configuration
- Strict type checking enabled
- ES2022 target
- Node.js module resolution
- Source maps enabled
- Output directory set to dist/
- Path mapping for clean imports

### 3. .nvmrc

Generate a `.nvmrc` file specifying Node.js 18.

### 4. Dockerfile

Create a multi-stage Dockerfile optimized for Node.js/TypeScript with:

- Multi-stage build for smaller production images
- Node.js 18+ base image (use Azure Linux base)
- npm ci for fast dependency installation
- Non-root user for security
- Proper layer caching
- Health check configuration
- Production-ready settings

```dockerfile
# Dockerfile structure for Node.js
FROM mcr.microsoft.com/azurelinux/base/nodejs:18-cm2.0
WORKDIR /app

# Install CA certificates
RUN tdnf install -y ca-certificates && \
    update-ca-trust enable && \
    update-ca-trust extract && \
    tdnf clean all

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build TypeScript
RUN npm run build

# Expose port 80 for Azure Container Apps
EXPOSE 80

# Set environment variables
ENV NODE_ENV=production
ENV PORT=80

# Run application
CMD ["npm", "start"]
```

### 5. .dockerignore

Create a `.dockerignore` file to exclude:

- Development files (.git, .vscode, etc.)
- Node modules and build artifacts
- Test files and documentation
- IDE configuration files
- OS-specific files
- TypeScript source files (after build)

### 6. index.ts

Create an `index.ts` file with:

- Express server setup
- Middleware configuration (cors, helmet, json parsing)
- Route registration
- Error handling middleware
- Graceful shutdown handling
- Environment configuration loading
- OpenTelemetry tracing integration
- Structured logging with Winston (never use console.log)

### 7. app.ts

Create an `app.ts` file with:

- Express application configuration
- Middleware setup
- Route definitions
- Error handling
- Health check endpoints
- Request/response logging

### 8. utils/config.ts

Create a configuration module with:

- Environment variable management
- Type-safe configuration object
- Common settings like HOST, PORT, NODE_ENV, LOG_LEVEL
- Azure Monitor configuration (APPLICATION_INSIGHTS_CONNECTION_STRING)
- Database and API configuration placeholders
- OpenTelemetry tracing settings
- Proper type definitions and defaults
- Azure credential management using best practices
- **CRITICAL**: Follow [Azure Best Practices](../azure-bestpractices.md) - NEVER use API keys for Azure services

Include a standard Azure credential helper function:
```typescript
import { ChainedTokenCredential, AzureDeveloperCliCredential, ManagedIdentityCredential } from '@azure/identity';

export function getAzureCredential(): ChainedTokenCredential {
  /**
   * Get Azure credential using best practice chain.
   * 
   * Returns ChainedTokenCredential that tries Azure Developer CLI first, then Managed Identity.
   * This works for both local development (azd) and production (Container Apps).
   */
  return new ChainedTokenCredential(
    new AzureDeveloperCliCredential(), // tries Azure Developer CLI (azd) for local development
    new ManagedIdentityCredential()    // fallback to managed identity for production
  );
}
```

This approach provides:
- Seamless local development experience (works with azd specifically)
- Production readiness (automatically uses managed identity in Azure Container Apps)
- No credential configuration needed
- Consistent authentication pattern across all Azure services

**Important**: Always ensure `AZURE_CLIENT_ID` environment variable is set in Azure Container Apps to specify which managed identity to use for authentication.

### 9. utils/logger.ts

Create a logging module using Winston with:

- Structured logging configuration
- JSON format for production environments
- Console and file transports
- Log levels (error, warn, info, debug)
- Request correlation IDs
- Performance logging
- Integration with OpenTelemetry tracing

### 10. routes/health.ts

Generate route files with:

- Health check endpoint for container monitoring
- Proper TypeScript types and interfaces
- Request/response handling with validation
- Error handling and logging
- OpenAPI/Swagger documentation
- Async/await patterns

### 11. middleware/errorHandler.ts

Create error handling middleware with:

- Global error handling
- Structured error logging
- HTTP status code mapping
- Error response formatting
- Request correlation tracking
- Security considerations (no stack traces in production)

### 12. README.md

Create a comprehensive `README.md` for the Node.js app with:

- Project description
- Prerequisites (Node.js 18+, npm, Docker, Azure Application Insights)
- Installation instructions using npm
- Development setup with TypeScript
- Running the application (local and Docker)
- Docker build and run instructions
- Configuration options (including Azure Monitor setup)
- API documentation and endpoints
- Testing instructions
- Container deployment guidance
- Monitoring and observability setup
- Azure Application Insights configuration
- Performance optimization tips

### 13. Test Configuration

Generate test files with Jest examples:

- Unit tests for routes and middleware
- Integration tests for API endpoints
- Test utilities and helpers
- Mock configurations for Azure services
- Test coverage configuration
- CI/CD testing setup

### 14. ESLint and Prettier Configuration

Include proper ESLint and Prettier configuration:

- TypeScript-specific rules
- Code formatting standards
- Import/export organization
- Security linting rules
- Performance best practices
- Consistent code style

### 15. Azure Developer CLI Configuration

Update the root `azure.yaml` file to include the new Node.js application as a service:

- Add a new service entry under the `services` section
- Configure the service with:
  - Service name: "${input:appName}"
  - Language: js
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
    language: js
    host: containerapp
    docker:
      remoteBuild: true
```

### 13. Infrastructure Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for all infrastructure changes.

Update the `infra/main.bicep` file to include a new container app module for the Node.js application:

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
  - Environment variables specific to the Node.js application
  - Resource allocation (CPU and memory)
  - Container port (80 for Azure Container Apps)

Example module configuration:
```bicep
// ${input:appName} Node.js Application
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
        name: 'NODE_ENV'
        value: 'production'
      }
      {
        name: 'PORT'
        value: '80'
      }
      {
        name: 'LOG_LEVEL'
        value: 'info'
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
@description('Container image for ${input:appName} Node.js application')
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

- Use modern Node.js 18+ features and TypeScript 5+
- Follow Express.js and TypeScript best practices
- Implement proper configuration management with type safety
- Include comprehensive type definitions throughout
- Production-ready error handling and logging
- Environment-based configuration
- Clean, maintainable code structure
- Docker containerization ready
- Multi-stage builds for optimization
- Security best practices (helmet, input validation, non-root user)
- Proper logging configuration using Winston (never use console.log)
- Structured logging with appropriate log levels (error, warn, info, debug)
- Azure Monitor integration via OpenTelemetry
- Distributed tracing for microservices
- Observability and monitoring ready
- Performance tracking and metrics
- Safe dependency versioning (use >= and < operators to prevent major version upgrades)
- Comprehensive test coverage with Jest
- ESLint and Prettier for code quality
- Graceful shutdown handling
- Health check endpoints for container orchestration
- Request correlation and tracing
- Input validation and sanitization
- Rate limiting and security headers
- API documentation with OpenAPI/Swagger