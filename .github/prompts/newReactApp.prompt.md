---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new React + Vite + Tailwind CSS application following best practices and a simplified structure'
---

# Create New React Application

- Create a new React application with Vite + Tailwind CSS under the src folder with a simplified structure.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-react-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-react-app}

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
- Review research collection findings for React-specific patterns, libraries, and configurations
- Use consolidated environment variables from collection template
- Reference code snippets from findings for implementation
- Validate against research gaps identified in collection phase

---

## Directory Structure

Create the following directory structure:
```text
src/
├── ${input:appName}/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .nvmrc
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── README.md
│   ├── index.html
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   ├── vite-env.d.ts
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── contexts/
│   │   │   └── ConfigContext.tsx
│   │   ├── hooks/
│   │   │   ├── useConfig.ts
│   │   │   └── useApi.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── telemetry.ts
│   │   ├── utils/
│   │   │   ├── config.ts
│   │   │   └── logger.ts
│   │   └── types/
│   │       ├── api.ts
│   │       └── config.ts
│   ├── tests/
│   │   ├── setup.ts
│   │   └── App.test.tsx
│   └── dist/ (build output)
```

## File Requirements

### 1. package.json

Generate a `package.json` file with:

- Project metadata (name: "${input:appName}", version, description, author)
- Node.js engine requirement (>=18.0.0)
- Scripts for dev, build, preview, test, lint, format
- Dependencies with safe version pinning (no major version upgrades):
  - react>=18.3.0,<19.0.0, react-dom>=18.3.0,<19.0.0
  - @microsoft/applicationinsights-react-js>=17.3.0,<18.0.0
  - @microsoft/applicationinsights-web>=3.3.0,<4.0.0
  - axios>=1.7.0,<2.0.0, react-router-dom>=6.26.0,<7.0.0
- Styling dependencies:
  - tailwindcss>=3.4.0,<4.0.0, autoprefixer>=10.4.0,<11.0.0, postcss>=8.4.0,<9.0.0
- DevDependencies:
  - vite>=5.4.0,<6.0.0, @vitejs/plugin-react>=4.3.0,<5.0.0
  - typescript>=5.6.0,<6.0.0, @types/react>=18.3.0,<19.0.0, @types/react-dom>=18.3.0,<19.0.0
  - vitest>=2.1.0,<3.0.0, @testing-library/react>=16.0.0,<17.0.0, @testing-library/jest-dom>=6.5.0,<7.0.0
  - eslint>=8.57.0,<9.0.0, @typescript-eslint/eslint-plugin>=8.8.0,<9.0.0, @typescript-eslint/parser>=8.8.0,<9.0.0
  - prettier>=3.3.0,<4.0.0, eslint-plugin-react>=7.37.0,<8.0.0, eslint-plugin-react-hooks>=4.6.0,<5.0.0

### 2. tsconfig.json

Create a `tsconfig.json` with:

- Modern TypeScript configuration for React
- Strict type checking enabled
- ES2022 target
- Modern module resolution
- JSX support with React 18
- Path mapping for clean imports
- Source maps enabled

### 3. tsconfig.node.json

Create a separate TypeScript config for Node.js tools (Vite config):

- Node.js-specific TypeScript configuration
- ES2022 target for build tools
- Module resolution for bundler

### 4. vite.config.ts

Create a Vite configuration with:

- React plugin configuration
- TypeScript support
- Path aliases for clean imports
- Development server configuration
- Build optimization settings
- Environment variable handling
- Proxy configuration for local API development

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Local FastAPI/Node.js API
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          telemetry: ['@microsoft/applicationinsights-react-js', '@microsoft/applicationinsights-web'],
        },
      },
    },
  },
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
})
```

### 5. tailwind.config.js

Create Tailwind CSS configuration with:

- Content paths for React components
- Custom theme extensions
- Plugin configurations
- Design system variables
- Responsive breakpoints

### 6. postcss.config.js

Create PostCSS configuration for Tailwind CSS processing.

### 7. .nvmrc

Generate a `.nvmrc` file specifying Node.js 18.

### 8. Dockerfile

Create a multi-stage Dockerfile optimized for React + Vite with:

- Multi-stage build for smaller production images
- Node.js 18+ base image (use Azure Linux base)
- npm ci for fast dependency installation
- Vite build optimization
- Nginx for serving static files
- Security best practices

```dockerfile
# Build stage
FROM mcr.microsoft.com/azurelinux/base/nodejs:18-cm2.0 AS build
WORKDIR /app

# Install CA certificates
RUN tdnf install -y ca-certificates && \
    update-ca-trust enable && \
    update-ca-trust extract && \
    tdnf clean all

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM mcr.microsoft.com/azurelinux/base/nginx:1.24-cm2.0
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 9. nginx.conf

Create Nginx configuration for serving React SPA:

- Single Page Application routing support
- Gzip compression
- Security headers
- Static file caching
- Health check endpoint

### 10. .dockerignore

Create a `.dockerignore` file to exclude:

- Development files (.git, .vscode, etc.)
- Node modules and build artifacts
- Test files and documentation
- IDE configuration files
- OS-specific files
- Source files (after build)

### 11. index.html

Create the main HTML template with:

- Modern HTML5 structure
- Meta tags for PWA support
- Viewport configuration
- Title and description
- Vite entry point

### 12. main.tsx

Create the main React entry point with:

- React 18 createRoot API
- Error boundary setup
- Application Insights initialization
- Global styles import
- Router setup

### 13. App.tsx

Create the main App component with:

- Router configuration
- ConfigContext provider
- Layout component
- Error boundary
- Loading states
- Route definitions

### 14. contexts/ConfigContext.tsx

Create a configuration context provider with:

- Configuration state management
- API call to fetch runtime configuration
- Loading and error states
- Type-safe configuration object
- Retry logic for failed requests

```typescript
import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { AppConfig } from '@/types/config';
import { fetchAppConfig } from '@/services/api';
import { logger } from '@/utils/logger';

interface ConfigContextType {
  config: AppConfig | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

interface ConfigProviderProps {
  children: ReactNode;
}

export const ConfigProvider: React.FC<ConfigProviderProps> = ({ children }) => {
  const [config, setConfig] = useState<AppConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchConfig = async () => {
    try {
      setLoading(true);
      setError(null);
      const configData = await fetchAppConfig();
      setConfig(configData);
      logger.info('Configuration loaded successfully', { config: configData });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load configuration';
      setError(errorMessage);
      logger.error('Failed to load configuration', { error: err });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  const value: ConfigContextType = {
    config,
    loading,
    error,
    refetch: fetchConfig,
  };

  return (
    <ConfigContext.Provider value={value}>
      {children}
    </ConfigContext.Provider>
  );
};

export const useConfigContext = (): ConfigContextType => {
  const context = useContext(ConfigContext);
  if (context === undefined) {
    throw new Error('useConfigContext must be used within a ConfigProvider');
  }
  return context;
};
```

### 15. hooks/useConfig.ts

Create a custom hook for accessing configuration:

- Easy access to configuration data
- Loading and error state handling
- Type-safe configuration access
- Automatic retries

```typescript
import { useConfigContext } from '@/contexts/ConfigContext';
import { AppConfig } from '@/types/config';

interface UseConfigReturn {
  config: AppConfig | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  isReady: boolean;
}

export const useConfig = (): UseConfigReturn => {
  const { config, loading, error, refetch } = useConfigContext();

  return {
    config,
    loading,
    error,
    refetch,
    isReady: !loading && !error && config !== null,
  };
};
```

### 16. hooks/useApi.ts

Create a custom hook for API calls with configuration:

- Axios instance with base configuration
- Authentication headers
- Error handling
- Request/response interceptors
- Retry logic
- **CRITICAL**: Follow [Azure Best Practices](../azure-bestpractices.md) when integrating with Azure services

### 17. services/api.ts

Create API service layer with:

- Axios configuration with interceptors
- Authentication token management
- Error handling and logging
- Request/response transformations
- Configuration endpoint

```typescript
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { AppConfig } from '@/types/config';
import { logger } from '@/utils/logger';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        logger.debug('API Request', { url: config.url, method: config.method });
        return config;
      },
      (error) => {
        logger.error('API Request Error', { error });
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        logger.debug('API Response', { url: response.config.url, status: response.status });
        return response;
      },
      (error) => {
        logger.error('API Response Error', { 
          url: error.config?.url, 
          status: error.response?.status,
          message: error.message 
        });
        return Promise.reject(error);
      }
    );
  }

  async fetchAppConfig(): Promise<AppConfig> {
    const response = await this.api.get<AppConfig>('/config');
    return response.data;
  }
}

export const apiService = new ApiService();
export const fetchAppConfig = () => apiService.fetchAppConfig();
```

### 18. services/telemetry.ts

Create Application Insights service with:

- React plugin initialization
- Custom telemetry tracking
- User authentication tracking
- Performance monitoring
- Error tracking integration

```typescript
import { ApplicationInsights } from '@microsoft/applicationinsights-web';
import { ReactPlugin } from '@microsoft/applicationinsights-react-js';
import { createBrowserHistory } from 'history';

const browserHistory = createBrowserHistory({ basename: '' });
const reactPlugin = new ReactPlugin();

class TelemetryService {
  private appInsights: ApplicationInsights | null = null;
  private isInitialized = false;

  initialize(connectionString: string) {
    if (this.isInitialized || !connectionString) {
      return;
    }

    this.appInsights = new ApplicationInsights({
      config: {
        connectionString,
        extensions: [reactPlugin],
        extensionConfig: {
          [reactPlugin.identifier]: { history: browserHistory }
        },
        enableAutoRouteTracking: true,
        enableCorsCorrelation: true,
        enableRequestHeaderTracking: true,
        enableResponseHeaderTracking: true,
      }
    });

    this.appInsights.loadAppInsights();
    this.isInitialized = true;
  }

  trackEvent(name: string, properties?: { [key: string]: any }) {
    if (this.appInsights) {
      this.appInsights.trackEvent({ name }, properties);
    }
  }

  trackException(error: Error, severityLevel?: number) {
    if (this.appInsights) {
      this.appInsights.trackException({ 
        exception: error,
        severityLevel: severityLevel || 3
      });
    }
  }

  setAuthenticatedUserContext(userId: string, accountId?: string) {
    if (this.appInsights) {
      this.appInsights.setAuthenticatedUserContext(userId, accountId);
    }
  }

  clearAuthenticatedUserContext() {
    if (this.appInsights) {
      this.appInsights.clearAuthenticatedUserContext();
    }
  }
}

export const telemetryService = new TelemetryService();
export { reactPlugin };
```

### 19. utils/config.ts

Create configuration utilities with:

- Environment variable management
- Type-safe configuration validation
- Default value handling
- Development vs production settings

### 20. utils/logger.ts

Create logging utility with:

- Structured logging for browser
- Log levels (debug, info, warn, error)
- Application Insights integration
- Development vs production logging

### 21. types/config.ts

Create TypeScript type definitions for configuration:

```typescript
export interface AppConfig {
  applicationInsights: {
    connectionString: string;
  };
  api: {
    baseUrl: string;
    timeout: number;
  };
  features: {
    enableTelemetry: boolean;
    enableDebugMode: boolean;
  };
  user?: {
    id: string;
    email: string;
    roles: string[];
  };
  environment: 'development' | 'staging' | 'production';
  version: string;
}

export interface ApiResponse<T = any> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}
```

### 22. types/api.ts

Create TypeScript type definitions for API responses and requests.

### 23. components/Layout.tsx

Create main layout component with:

- Header and footer integration
- Responsive design
- Navigation structure
- Content area
- Loading states

### 24. components/ErrorBoundary.tsx

Create React error boundary with:

- Error catching and logging
- Fallback UI
- Application Insights integration
- Recovery mechanisms

### 25. README.md

Create a comprehensive `README.md` for the React app with:

- Project description and features
- Prerequisites (Node.js 18+, npm, Docker)
- Installation instructions using npm
- Development setup with Vite
- Running the application (local and Docker)
- **Local API Development Setup**:
  - Instructions for running with local FastAPI backend
  - Proxy configuration for `/api` routes
  - Environment variable setup for local development
  - Example: `npm run dev` with `uvicorn main:app --reload --port 8000`
- Docker build and run instructions
- Configuration options and environment variables
- Application Insights setup and telemetry
- API integration documentation
- Testing instructions with Vitest
- Deployment guidance for Azure Container Apps
- Performance optimization tips
- Troubleshooting common issues

**Local Development with API Backend section**:
```markdown
## Local Development with API Backend

This React application is designed to work with a backend API. For local development:

### Running with FastAPI Backend
1. Start your FastAPI backend:
   ```bash
   # In your API project directory
   uvicorn main:app --reload --port 8000
   ```

2. Start the React development server:
   ```bash
   # In this React project directory
   npm run dev
   ```

The Vite proxy configuration will automatically forward `/api/*` requests to `http://localhost:8000`.

### Running with Node.js/Express Backend
1. Start your Node.js backend:
   ```bash
   # In your API project directory
   npm run dev  # Usually runs on port 8000
   ```

2. Start the React development server:
   ```bash
   npm run dev
   ```

### Environment Variables
Create a `.env.local` file for local development:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_INSIGHTS_CONNECTION_STRING=your-connection-string
VITE_ENVIRONMENT=development
```
```

### 26. Test Configuration

Generate test files with Vitest and React Testing Library:

- Component testing setup
- API mocking with MSW
- Context provider testing
- Custom hook testing
- Integration test examples
- Test utilities and helpers

### 27. ESLint and Prettier Configuration

Include proper ESLint and Prettier configuration:

- React-specific rules
- TypeScript integration
- Tailwind CSS class sorting
- Import organization
- Accessibility rules
- Performance best practices

### 28. Azure Developer CLI Configuration

Update the root `azure.yaml` file to include the new React application as a service:

- Add a new service entry under the `services` section
- Configure the service with:
  - Service name: "${input:appName}"
  - Language: js
  - Host: containerapp
  - Docker configuration with:
    - Remote builds enabled: `remoteBuild: true`
  - Environment variables for runtime configuration
  - **Critical**: Configure for SPA routing and static file serving
- Ensure proper service dependencies if needed
- Configure resource group and location references

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

### 12. Infrastructure Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for all infrastructure changes.

Update the `infra/main.bicep` file to include a new container app module for the React application:

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
  - Environment variables for React application configuration
  - Resource allocation (CPU and memory for SPA)
  - Container port (80 for Nginx)

Example module configuration:
```bicep
// ${input:appName} React Application
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
        name: 'VITE_API_BASE_URL'
        value: 'https://${apiApp.outputs.fqdn}'
      }
      {
        name: 'VITE_APP_INSIGHTS_CONNECTION_STRING'
        value: monitoring.outputs.applicationInsightsConnectionString
      }
      {
        name: 'VITE_ENVIRONMENT'
        value: environmentName
      }
    ]
    resources: {
      cpu: 0.5
      memory: '1Gi'
    }
  }
}
```

- Add a parameter for the container image at the top of main.bicep:
```bicep
@description('Container image for ${input:appName} React application')
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

- Use modern React 18+ features with TypeScript 5+
- Follow React and Vite best practices
- Implement proper state management with Context API
- Include comprehensive type definitions throughout
- Production-ready error handling and logging
- Environment-based configuration
- Responsive design with Tailwind CSS
- Clean, maintainable component architecture
- Docker containerization with Nginx
- Multi-stage builds for optimization
- Security best practices (CSP headers, secure defaults)
- Application Insights integration for telemetry
- Performance monitoring and optimization
- Accessibility compliance (WCAG guidelines)
- SEO optimization for SPA
- Progressive Web App features
- Safe dependency versioning (use >= and < operators to prevent major version upgrades)
- Comprehensive test coverage with Vitest and React Testing Library
- ESLint and Prettier for code quality
- Hot module replacement for development
- Code splitting and lazy loading
- Bundle optimization and tree shaking
- Runtime configuration loading via API
- Proxy support for local API development
- Error boundaries for graceful error handling
- Loading states and skeleton screens
- TypeScript strict mode compliance

## Research Artifacts Integration (If Available)

When implementing this React application, leverage any available research collection artifacts:

### Pre-Implementation Checklist
- [ ] Review research plan file (if exists) for scope validation
- [ ] Check research collection findings for React + Vite specific patterns
- [ ] Validate all consolidated environment variables against application requirements
- [ ] Review code snippets from findings for implementation references
- [ ] Check consolidated commands/infra for deployment prerequisites
- [ ] Identify any research gaps that may require additional documentation

### Key Integration Points
1. **Dependencies**: Cross-reference `package.json` dependencies with research findings for React, Vite, TypeScript, and Application Insights libraries
2. **Environment Variables**: Use consolidated environment variables from research collection (Section 4) as baseline for `.env.local` and Bicep configuration
3. **Code Patterns**: Implement code snippets from findings (Section 3) for Application Insights, telemetry, configuration context, and API integration
4. **Configuration**: Apply config/schema findings to `vite.config.ts`, `tsconfig.json`, and application configuration utilities
5. **Commands**: Reference consolidated commands (Section 5) for build, deployment, and infrastructure provisioning
6. **Integration**: Use integration/registration patterns from findings for Azure services and Application Insights setup

### Research Artifacts Reference Structure
```
.github/research/
├── plans/
│   └── [app-name]-react-app-plan.md          # Research plan with refined search terms
└── collections/
    └── [app-name]-react-app-collection.md    # Research findings with code snippets
```

### Implementation Validation
After implementation, validate against research artifacts:
- All environment variables from research collection are configured in Bicep
- Code patterns from findings are correctly implemented
- Dependencies match research recommendations with proper version constraints
- Configuration follows documented patterns from research
- Any research gaps are documented in application README

**Note**: If no research artifacts exist for this implementation, proceed with standard best practices as documented in this prompt.