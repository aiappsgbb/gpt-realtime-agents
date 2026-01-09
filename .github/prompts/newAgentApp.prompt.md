---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new AI agent application using Microsoft Agent Framework following best practices and modern patterns.'
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
- Review research collection findings for agent framework, workflow patterns, and AI integration
- Use consolidated environment variables from collection template
- Reference code snippets from findings for agent implementation
- Validate against research gaps identified in collection phase

---

# Create New Microsoft Agent Framework Application

- Create a new AI agent application using Microsoft Agent Framework under the src folder with a simplified structure.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-agent-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-agent-app}

## Configuration Options

### Agent Type Selection

Choose your preferred agent implementation:

**Option 1: Single Chat Agent** (Default)
- Simple conversational AI agent
- Direct question-answer interactions
- Function calling capabilities
- Suitable for: Customer service, Q&A bots, personal assistants

**Option 2: Multi-Agent Workflow**
- Orchestrated collaboration between multiple specialized agents
- Sequential or parallel agent execution
- Shared context and state management
- Suitable for: Complex document processing, collaborative analysis, multi-step workflows

**Option 3: Custom Workflow with Executors**
- Directed Acyclic Graph (DAG) workflow processing
- Custom business logic executors
- Function-based or class-based execution nodes
- Suitable for: Data processing pipelines, content transformation, business automation

### Framework Integration

**Azure Integration** (Recommended)
- Azure OpenAI for LLM capabilities
- Azure AI Foundry for advanced agent services
- Azure CLI authentication (local) + Managed Identity (production)
- Application Insights for observability

**OpenAI Integration**
- Direct OpenAI API integration
- API key or Azure CLI authentication
- Suitable for development and testing

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
│   ├── main.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── chat_agent.py
│   │   ├── multi_agent_workflow.py
│   │   └── custom_workflow.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── function_tools.py
│   │   ├── search_tools.py
│   │   └── file_tools.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── security_middleware.py
│   │   ├── logging_middleware.py
│   │   └── telemetry_middleware.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── azure_auth.py
│   ├── examples/
│   │   ├── simple_chat.py
│   │   ├── workflow_example.py
│   │   └── tool_usage.py
│   └── tests/
│       ├── __init__.py
│       ├── test_agents.py
│       ├── test_tools.py
│       └── test_workflows.py
```

## File Requirements

### 1. pyproject.toml

Generate a `pyproject.toml` file with:

- Project metadata (name: "${input:appName}", version, description, authors)
- Python version requirement (>=3.11)
- Microsoft Agent Framework dependencies with safe version pinning:
  - agent-framework>=0.1.0,<1.0.0 (core framework)
  - agent-framework-azure-ai>=0.1.0,<1.0.0 (Azure integration)
  - agent-framework-microsoft>=0.1.0,<1.0.0 (Microsoft services)
- Azure integration dependencies:
  - azure-identity>=1.19.0,<2.0.0
  - azure-ai-projects>=1.0.0,<2.0.0
  - azure-monitor-opentelemetry>=1.0.0,<2.0.0
- Core dependencies:
  - pydantic>=2.9.0,<3.0.0, pydantic-settings>=2.6.0,<3.0.0
  - python-dotenv>=1.0.0,<2.0.0, httpx>=0.27.0,<0.28.0
- Development dependencies: pytest>=8.3.0,<9.0.0, pytest-asyncio>=0.24.0,<0.25.0, black>=24.10.0,<25.0.0, ruff>=0.7.0,<0.8.0
- **CRITICAL**: Follow [Azure Best Practices](../azure-bestpractices.md) - NEVER use API keys for Azure services

### 2. .python-version

Create a `.python-version` file specifying Python 3.11.

### 3. main.py

Generate a `main.py` file with:

- Configuration loading and validation
- Agent initialization based on selected type
- Environment setup with Azure authentication
- Error handling and logging using Python's logging module
- Health check endpoints for container deployment
- Graceful shutdown handling
- OpenTelemetry tracing integration

Example structure:
```python
import asyncio
import logging
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential, ManagedIdentityCredential, ChainedTokenCredential
from utils.config import Settings
from utils.logging_config import setup_logging

async def main():
    # Setup logging and configuration
    setup_logging()
    settings = Settings()
    
    # Initialize Azure authentication
    credential = ChainedTokenCredential(
        AzureCliCredential(),
        ManagedIdentityCredential()
    )
    
    # Create agent based on configuration
    if settings.agent_type == "chat":
        from agents.chat_agent import create_chat_agent
        agent = await create_chat_agent(credential, settings)
    elif settings.agent_type == "workflow":
        from agents.multi_agent_workflow import create_workflow
        workflow = await create_workflow(credential, settings)
    else:
        from agents.custom_workflow import create_custom_workflow
        workflow = await create_custom_workflow(credential, settings)
    
    # Start agent service
    logger.info(f"Starting {settings.agent_type} agent...")
    # Implementation depends on agent type

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. agents/chat_agent.py

Create a single chat agent implementation:

```python
import asyncio
from typing import Annotated
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import ChainedTokenCredential
from tools.function_tools import get_weather, get_current_time
from middleware.security_middleware import SecurityAgentMiddleware
from middleware.logging_middleware import LoggingAgentMiddleware

async def create_chat_agent(credential: ChainedTokenCredential, settings) -> ChatAgent:
    """Create and configure a chat agent with tools and middleware."""
    
    # Initialize Azure OpenAI client
    client = AzureOpenAIResponsesClient(
        credential=credential,
        endpoint=settings.azure_openai_endpoint,
        deployment_name=settings.azure_openai_deployment
    )
    
    # Create agent with tools and middleware
    agent = ChatAgent(
        name=settings.agent_name,
        instructions=settings.agent_instructions,
        client=client,
        tools=[get_weather, get_current_time],
        middleware=[
            SecurityAgentMiddleware(),
            LoggingAgentMiddleware()
        ]
    )
    
    return agent
```

### 5. agents/multi_agent_workflow.py

Create a multi-agent workflow implementation:

```python
import asyncio
from agent_framework import AgentRunEvent, WorkflowBuilder, ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import ChainedTokenCredential

async def create_workflow(credential: ChainedTokenCredential, settings):
    """Create a multi-agent workflow with specialized agents."""
    
    # Create specialized agents
    chat_client = AzureOpenAIChatClient(
        credential=credential,
        endpoint=settings.azure_openai_endpoint,
        deployment_name=settings.azure_openai_deployment
    )
    
    # Writer agent
    writer = ChatAgent(
        name="Writer",
        instructions="You are a creative writer. Write engaging content based on the input.",
        client=chat_client
    )
    
    # Reviewer agent
    reviewer = ChatAgent(
        name="Reviewer",
        instructions="You are an editor. Review and improve the provided content.",
        client=chat_client
    )
    
    # Build workflow
    workflow = (
        WorkflowBuilder()
        .add_agent(writer)
        .add_agent(reviewer)
        .add_edge(writer, reviewer)
        .build()
    )
    
    return workflow
```

### 6. agents/custom_workflow.py

Create a custom DAG workflow implementation:

```python
import asyncio
from agent_framework import Executor, WorkflowBuilder, WorkflowContext, executor
from typing_extensions import Never

class TextProcessor(Executor):
    """Custom executor for text processing."""
    
    def __init__(self, id: str, operation: str):
        super().__init__(id)
        self.operation = operation
    
    async def execute(self, text: str, ctx: WorkflowContext) -> None:
        if self.operation == "uppercase":
            result = text.upper()
        elif self.operation == "reverse":
            result = text[::-1]
        else:
            result = text
        
        await ctx.yield_output(result)

@executor(id="sentiment_analyzer")
async def analyze_sentiment(text: str, ctx: WorkflowContext[Never, str]) -> None:
    """Analyze sentiment of the input text."""
    # Implement sentiment analysis logic
    sentiment = "positive" if "good" in text.lower() else "neutral"
    result = f"Text: {text} | Sentiment: {sentiment}"
    await ctx.yield_output(result)

async def create_custom_workflow(credential, settings):
    """Create a custom DAG workflow with executors."""
    
    # Create executors
    uppercase_executor = TextProcessor(id="uppercase", operation="uppercase")
    reverse_executor = TextProcessor(id="reverse", operation="reverse")
    
    # Build workflow
    workflow = (
        WorkflowBuilder()
        .add_executor(uppercase_executor)
        .add_executor(reverse_executor)
        .add_executor(analyze_sentiment)
        .add_edge("uppercase", "reverse")
        .add_edge("reverse", "sentiment_analyzer")
        .build()
    )
    
    return workflow
```

### 7. tools/function_tools.py

Create function tools for agents:

```python
from typing import Annotated
from datetime import datetime
from random import randint
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")]
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

def get_current_time() -> str:
    """Get the current UTC time."""
    current_time = datetime.utcnow()
    return f"The current UTC time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}."

def calculate_sum(
    numbers: Annotated[list[float], Field(description="List of numbers to sum")]
) -> float:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)
```

### 8. middleware/security_middleware.py

Create security middleware:

```python
from agent_framework import AgentMiddleware, AgentRunContext

class SecurityAgentMiddleware(AgentMiddleware):
    """Middleware for security checks."""
    
    BLOCKED_KEYWORDS = ["password", "secret", "confidential", "classified"]
    
    async def process(
        self,
        context: AgentRunContext,
        next_middleware
    ) -> None:
        # Check for sensitive content
        message_content = str(context.messages[-1].content).lower()
        
        if any(keyword in message_content for keyword in self.BLOCKED_KEYWORDS):
            context.result = "I cannot process requests containing sensitive information."
            return
        
        # Continue to next middleware
        await next_middleware(context)
```

### 9. middleware/logging_middleware.py

Create logging middleware:

```python
import time
import logging
from agent_framework import AgentMiddleware, AgentRunContext

logger = logging.getLogger(__name__)

class LoggingAgentMiddleware(AgentMiddleware):
    """Middleware for request logging."""
    
    async def process(
        self,
        context: AgentRunContext,
        next_middleware
    ) -> None:
        start_time = time.time()
        
        logger.info(f"Agent request started: {context.messages[-1].content[:100]}...")
        
        try:
            await next_middleware(context)
            duration = time.time() - start_time
            logger.info(f"Agent request completed in {duration:.2f}s")
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Agent request failed after {duration:.2f}s: {e}")
            raise
```

### 10. utils/config.py

Create configuration management:

```python
from pydantic import BaseSettings, Field
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class Settings(BaseSettings):
    """Application settings with Azure best practices."""
    
    # Agent configuration
    agent_name: str = Field(default="AI Assistant", description="Name of the AI agent")
    agent_type: Literal["chat", "workflow", "custom"] = Field(default="chat", description="Type of agent to create")
    agent_instructions: str = Field(
        default="You are a helpful AI assistant. Be concise and accurate in your responses.",
        description="Instructions for the agent"
    )
    
    # Azure OpenAI configuration (NO API KEYS - use managed identity)
    azure_openai_endpoint: str = Field(..., description="Azure OpenAI endpoint URL")
    azure_openai_deployment: str = Field(default="gpt-4o-mini", description="Azure OpenAI deployment name")
    
    # Azure authentication
    azure_client_id: str | None = Field(default=None, description="Azure Client ID for managed identity")
    
    # Application settings
    log_level: str = Field(default="INFO", description="Logging level")
    port: int = Field(default=80, description="Server port")
    host: str = Field(default="0.0.0.0", description="Server host")
    
    # Observability
    application_insights_connection_string: str | None = Field(
        default=None, 
        description="Application Insights connection string"
    )
    
    class Config:
        env_prefix = "AGENT_"
        case_sensitive = False
```

### 11. utils/azure_auth.py

Create Azure authentication helper:

```python
from azure.identity import AzureCliCredential, ManagedIdentityCredential, ChainedTokenCredential

def get_azure_credential(client_id: str | None = None) -> ChainedTokenCredential:
    """Get Azure credential using best practice chain.
    
    Returns:
        ChainedTokenCredential that tries Azure Developer CLI first, then Managed Identity.
        This works for both local development (azd) and production (Container Apps).
    """
    credentials = [AzureCliCredential()]
    
    if client_id:
        credentials.append(ManagedIdentityCredential(client_id=client_id))
    else:
        credentials.append(ManagedIdentityCredential())
    
    return ChainedTokenCredential(*credentials)
```

### 12. examples/simple_chat.py

Create example implementations:

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIResponsesClient
from utils.azure_auth import get_azure_credential
from utils.config import Settings
from tools.function_tools import get_weather, get_current_time

async def main():
    """Simple chat agent example."""
    settings = Settings()
    credential = get_azure_credential(settings.azure_client_id)
    
    # Create client and agent
    client = AzureOpenAIResponsesClient(
        credential=credential,
        endpoint=settings.azure_openai_endpoint,
        deployment_name=settings.azure_openai_deployment
    )
    
    agent = ChatAgent(
        name="Weather Assistant",
        instructions="You are a helpful weather assistant. Use the available tools to provide weather information.",
        client=client,
        tools=[get_weather, get_current_time]
    )
    
    # Example conversation
    response = await agent.run("What's the weather like in Seattle?")
    print(f"Agent: {response}")
    
    response = await agent.run("What time is it now?")
    print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 13. Dockerfile

Create a production-ready Dockerfile:

```dockerfile
# Multi-stage build for Microsoft Agent Framework
FROM mcr.microsoft.com/azurelinux/base/python:3.12 AS base
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
ENV AGENT_PORT=80
ENV AGENT_HOST=0.0.0.0

# Create non-root user
RUN groupadd -r agentuser && useradd -r -g agentuser agentuser
RUN chown -R agentuser:agentuser /app
USER agentuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.exit(0)"

WORKDIR /app
CMD ["uv", "run", "python", "main.py"]
```

### 14. README.md

Create comprehensive documentation:

- Project description and capabilities
- Microsoft Agent Framework overview
- Agent type explanations (Chat vs Workflow vs Custom)
- Prerequisites (Python 3.11+, Azure CLI, uv)
- Installation and setup instructions
- Configuration options and environment variables
- Running different agent types (examples)
- Tool development guide
- Middleware creation guide
- Docker deployment instructions
- Azure Container Apps deployment
- Observability and monitoring setup
- Troubleshooting guide

### 15. Azure Developer CLI Configuration

Update the root `azure.yaml` file to include the new Agent Framework application:

```yaml
services:
  ${input:appName}:
    project: "./src/${input:appName}"
    language: python
    host: containerapp
    docker:
      remoteBuild: true
    env:
      - AZURE_OPENAI_ENDPOINT
      - AZURE_CLIENT_ID  # REQUIRED for managed identity
      - APPLICATION_INSIGHTS_CONNECTION_STRING
      - AGENT_LOG_LEVEL
      - AGENT_TYPE  # chat, workflow, or custom
```

### 16. Infrastructure Configuration

**Important**: Follow [Bicep Deployment Best Practices](../bicep-deployment-bestpractices.md) for all infrastructure changes.

Update `infra/main.bicep` with Agent Framework container app:

```bicep
// ${input:appName} Microsoft Agent Framework Application
module ${input:appName}App 'core/host/container-app.bicep' = {
  name: '${input:appName}-agent-app'
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
        name: 'AZURE_OPENAI_ENDPOINT'
        value: openAi.outputs.endpoint
      }
      {
        name: 'APPLICATION_INSIGHTS_CONNECTION_STRING'
        value: monitoring.outputs.applicationInsightsConnectionString
      }
      {
        name: 'AGENT_TYPE'
        value: 'chat'  // or 'workflow' or 'custom'
      }
      {
        name: 'AGENT_LOG_LEVEL'
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

## Technical Requirements

- Use Python 3.11+ with modern async/await patterns
- Follow Microsoft Agent Framework best practices and patterns
- Implement proper configuration management with pydantic-settings
- Include comprehensive type hints throughout
- Production-ready error handling and middleware
- Environment-based configuration without API keys
- Clean, maintainable code structure with clear separation
- Docker containerization ready for Azure Container Apps
- Security best practices with middleware and validation
- Proper logging using Python's logging module (never print statements)
- Structured logging with JSON format for production
- Azure Monitor integration via OpenTelemetry
- Distributed tracing for agent interactions
- **CRITICAL**: Follow [Azure Best Practices](../azure-bestpractices.md) - NO API KEYS
- Support for multiple agent patterns (chat, workflow, custom)
- Extensible tool and middleware architecture
- Comprehensive testing with pytest
- Documentation and examples for all patterns
- Graceful shutdown and health check endpoints
- Performance monitoring and metrics collection
- Safe dependency versioning to prevent breaking changes