================
CODE SNIPPETS
================
TITLE: Create Azure OpenAI Agent with Azure CLI Authentication (Python)
DESCRIPTION: This Python snippet demonstrates how to initialize an AI agent using Azure OpenAI Responses Client with `AzureCliCredential` for authentication. It shows setting up a "HaikuBot" agent and running a prompt. Environment variables can be used for configuration.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/README.md

LANGUAGE: python
CODE:
```
import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential


async def main():
    # Initialize a chat agent with Azure OpenAI Responses
    # the endpoint, deployment name, and api version can be set via environment variables
    # or they can be passed in directly to the AzureOpenAIResponsesClient constructor
    agent = AzureOpenAIResponsesClient(
        # endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        # deployment_name=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
        # api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        # api_key=os.environ["AZURE_OPENAI_API_KEY"],  # Optional if using AzureCliCredential
        credential=AzureCliCredential(), # Optional, if using api_key
    ).create_agent(
        name="HaikuBot",
        instructions="You are an upbeat assistant that writes beautifully.",
    )

    print(await agent.run("Write a haiku about Microsoft Agent Framework."))

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

TITLE: Configure Azure OpenAI Chat Client Programmatically (Python)
DESCRIPTION: This Python snippet demonstrates how to initialize the AzureOpenAIChatClient by passing configuration parameters like deployment name and endpoint directly. It uses AzureCliCredential for authentication but shows where an API key could be supplied.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/multimodal_input/README.md

LANGUAGE: python
CODE:
```
# Example: Pass deployment_name directly
client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    deployment_name="your-deployment-name",
    endpoint="https://your-resource.openai.azure.com"
)
```

--------------------------------

TITLE: Integrate OpenTelemetry and Azure Application Insights for Agent Observability (Python)
DESCRIPTION: This Python example integrates OpenTelemetry with Azure Application Insights for agent telemetry. It sets up an `AzureAIAgentClient` and `AIProjectClient`, enables observability, and traces a `ChatAgent` interaction. The agent uses a custom `get_weather` tool to answer questions, with trace IDs logged.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
import os
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import get_tracer
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

async def main():
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(
            endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            credential=credential
        ) as project,
        AzureAIAgentClient(project_client=project) as client
    ):
        # Enable Azure AI observability - sends telemetry to Application Insights
        await client.setup_azure_ai_observability()

        with get_tracer().start_as_current_span("Single Agent Chat", kind=SpanKind.CLIENT) as span:
            print(f"Trace ID: {format_trace_id(span.get_span_context().trace_id)}")

            agent = ChatAgent(
                chat_client=client,
                tools=get_weather,
                name="WeatherAgent",
                instructions="You are a weather assistant."
            )

            thread = agent.get_new_thread()
            questions = [
                "What's the weather in Amsterdam?",
                "and in Paris, and which is better?"
            ]

            for question in questions:
                print(f"User: {question}")
                async for update in agent.run_stream(question, thread=thread):
                    if update.text:
                        print(update.text, end="")

asyncio.run(main())
```

--------------------------------

TITLE: Python: Create Dataset with Connection
DESCRIPTION: This Python code snippet demonstrates how to create a dataset using a specified connection string. It assumes the existence of a client object and a connection named 'my-azure-blob-connection'. This is part of simplifying external Azure resource consumption.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/specs/spec-template.md

LANGUAGE: python
CODE:
```
client.datasets.create_dataset(
    name="evaluation_dataset",
    file="myblob/product1.pdf",
    connection = "my-azure-blob-connection"
)
```

--------------------------------

TITLE: Import Path for Azure Services
DESCRIPTION: Defines the import path for all Azure services, consolidating them under the 'azure' vendor folder, regardless of their specific feature or brand.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: python
CODE:
```
from agent_framework.azure import AzureOpenAIClient, FoundryConnector
```

--------------------------------

TITLE: Setup Observability with Default Azure Credential
DESCRIPTION: This snippet demonstrates how to initialize observability with the DefaultAzureCredential, which is recommended for local development. It imports the necessary function and credential type from the azure-identity library.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
from azure.identity import DefaultAzureCredential

setup_observability(..., credential=DefaultAzureCredential())
```

--------------------------------

TITLE: Override API Key Configuration in Azure OpenAI Chat Client (Python)
DESCRIPTION: This Python code demonstrates how to explicitly pass API key, endpoint, and deployment name parameters directly to the `AzureOpenAIChatClient` constructor. This method overrides any environment variables, providing precise control over client configuration.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/README.md

LANGUAGE: python
CODE:
```
from agent_framework.azure import AzureOpenAIChatClient

chat_client = AzureOpenAIChatClient(
    api_key='',
    endpoint='',
    deployment_name='',
    api_version='',
)
```

--------------------------------

TITLE: Python: Create Azure AI Search Index with Connection
DESCRIPTION: This Python code snippet shows how to initialize and create an Azure AI Search index using a predefined connection. It utilizes the `AzureAISearchIndex` model and a connection named 'my-ai-search-connection'. This facilitates the integration of external search capabilities.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/specs/spec-template.md

LANGUAGE: python
CODE:
```
from azure.ai.projects.models import AzureAISearchIndex

azure_ai_search_index = AzureAISearchIndex(
    name="azure-search-index",
    connection="my-ai-search-connection",
    index_name="my-index-in-azure-search",
)

created_index = client.indexes.create_index(azure_ai_search_index)
```

--------------------------------

TITLE: Configure Azure OpenAI Chat Client with Parameters in Python
DESCRIPTION: This Python code illustrates an alternative method to set up API keys by passing configuration parameters directly to the AzureOpenAIChatClient constructor. This approach allows programmatic control over credentials and endpoints, useful when environment variables are not preferred.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: python
CODE:
```
from agent_framework.azure import AzureOpenAIChatClient

chat_client = AzureOpenAIChatClient(
    api_key="",
    endpoint="",
    deployment_name="",
    api_version="",
)
```

--------------------------------

TITLE: Import Path for Microsoft Copilot Studio
DESCRIPTION: Specifies the designated import path for Microsoft services that are not part of Azure, using 'microsoft' as the vendor folder.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: python
CODE:
```
from agent_framework.microsoft import CopilotStudioClient
```

--------------------------------

TITLE: Install Specific Microsoft Agent Framework Integrations (Python)
DESCRIPTION: These commands demonstrate how to selectively install components of the Microsoft Agent Framework to manage dependencies. Options include installing only the core, or adding specific integrations like Azure AI or Microsoft Copilot Studio, using the `--pre` flag.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/README.md

LANGUAGE: bash
CODE:
```
pip install agent-framework-core --pre

pip install agent-framework-azure-ai --pre

pip install agent-framework-copilotstudio --pre

pip install agent-framework-microsoft agent-framework-azure-ai --pre
```

--------------------------------

TITLE: Configure API Keys via Environment Variables (Shell)
DESCRIPTION: This snippet shows how to set up API keys for OpenAI and Azure OpenAI services using environment variables. These variables can be defined directly in the shell or placed within a `.env` file at the project root for easy access.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/README.md

LANGUAGE: bash
CODE:
```
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL_ID=...
...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
...
AZURE_AI_PROJECT_ENDPOINT=...
AZURE_AI_MODEL_DEPLOYMENT_NAME=...
```

--------------------------------

TITLE: Kusto Query for Analyzing Application Insights Logs
DESCRIPTION: This Kusto query is designed to analyze logs within Azure Application Insights. It focuses on retrieving dependency information, correlating tool call durations, and projecting relevant fields for analysis, ordered by timestamp.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: kusto
CODE:
```
dependencies
| where operation_Id in (dependencies
    | project operation_Id, timestamp
    | order by timestamp desc
    | summarize operations = make_set(operation_Id), timestamp = max(timestamp) by operation_Id
    | order by timestamp desc
    | project operation_Id
    | take 2)
| evaluate bag_unpack(customDimensions)
| extend tool_call_id = tostring(["gen_ai.tool.call.id"])
| join kind=leftouter (customMetrics
    | extend tool_call_id = tostring(customDimensions['gen_ai.tool.call.id'])
    | where isnotempty(tool_call_id)
    | project tool_call_duration = value, tool_call_id)
    on tool_call_id
| project-keep timestamp, target, operation_Id, tool_call_duration, duration, gen_ai*
| order by timestamp asc
```

--------------------------------

TITLE: Stateful Functions - Azure AI Foundry
DESCRIPTION: Describes how to define Azure Functions as stateful tools in the Azure AI Foundry Agent Service.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Azure AI Foundry Agent Service - Stateful Functions

### Description
This section details the structure for defining Azure Functions as stateful tools within the Azure AI Foundry Agent Service.

### Method
Not applicable (Configuration)

### Endpoint
Not applicable (Configuration)

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools to be used by the agent.
  - **type** (string) - Required - The type of the tool, should be "azure_function".
  - **azure_function** (object) - Required - Configuration for the Azure Function tool.
    - **function** (object) - Required - Details of the Azure Function.
      - **name** (string) - Required - The name of the function.
      - **description** (string) - Optional - A description of the function.
      - **parameters** (object) - Required - The JSON Schema object defining the function's parameters.
    - **input_binding** (object) - Optional - Configuration for the input binding.
      - **type** (string) - Required - The type of the input binding, e.g., "storage_queue".
      - **storage_queue** (object) - Required if type is "storage_queue".
        - **queue_service_endpoint** (string) - Required - The endpoint of the storage queue service.
        - **queue_name** (string) - Required - The name of the storage queue.
    - **output_binding** (object) - Optional - Configuration for the output binding.
      - **type** (string) - Required - The type of the output binding, e.g., "storage_queue".
      - **storage_queue** (object) - Required if type is "storage_queue".
        - **queue_service_endpoint** (string) - Required - The endpoint of the storage queue service.
        - **queue_name** (string) - Required - The name of the storage queue.

### Request Example
```json
{
  "tools": [
    {
      "type": "azure_function",
      "azure_function": {
        "function": {
          "name": "{string}",
          "description": "{string}",
          "parameters": "{JSON Schema object}"
        },
        "input_binding": {
          "type": "storage_queue",
          "storage_queue": {
            "queue_service_endpoint": "{string}",
            "queue_name": "{string}"
          }
        },
        "output_binding": {
          "type": "storage_queue",
          "storage_queue": {
            "queue_service_endpoint": "{string}",
            "queue_name": "{string}"
          }
        }
      }
    }
  ]
}
```

### Response
#### Success Response (200)
Tool Call Response: Not specified in the documentation.
```

--------------------------------

TITLE: Authenticate with Azure CLI (PowerShell)
DESCRIPTION: This snippet shows how to log in to Azure using the Azure CLI, which is a prerequisite for accessing Azure OpenAI resources. It requires the Azure CLI to be installed and configured.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/Agents/Agent_Step14_Middleware/README.md

LANGUAGE: powershell
CODE:
```
az login
```

--------------------------------

TITLE: Set Azure AI Environment Variables (Bash)
DESCRIPTION: This snippet demonstrates how to set the necessary environment variables in a Bash shell for an Azure AI project. It includes variables for the project endpoint, model deployment name, and an optional Bing connection ID, which is required for web search functionalities. These variables are crucial for running the provided examples and connecting to Azure AI services.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/azure_ai/README.md

LANGUAGE: bash
CODE:
```
export AZURE_AI_PROJECT_ENDPOINT="your-project-endpoint"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="your-model-deployment-name"
export BING_CONNECTION_ID="your-bing-connection-id" # Optional, only needed for web search samples
```

--------------------------------

TITLE: Execute Python Code with Hosted Code Interpreter Tool in Agent (Python)
DESCRIPTION: This Python snippet demonstrates using a `HostedCodeInterpreterTool` with a `ChatAgent` and `OpenAIResponsesClient`. The agent is configured to write and execute Python code, exemplified by calculating a factorial. It also shows how to extract the generated code from the agent's raw response.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import ChatAgent, HostedCodeInterpreterTool
from agent_framework.openai import OpenAIResponsesClient

async def main():
    agent = ChatAgent(
        chat_client=OpenAIResponsesClient(),
        instructions="You are a helpful assistant that can write and execute Python code.",
        tools=HostedCodeInterpreterTool()
    )

    result = await agent.run("Use code to get the factorial of 100?")
    print(f"Result: {result}")

    # Access generated code from raw representation
    if (isinstance(result.raw_representation, ChatResponse)
        and isinstance(result.raw_representation.raw_representation, OpenAIResponse)
        and len(result.raw_representation.raw_representation.output) > 0
        and isinstance(result.raw_representation.raw_representation.output[0],
                      ResponseCodeInterpreterToolCall)):)
        generated_code = result.raw_representation.raw_representation.output[0].code
        print(f"Generated code:\n{generated_code}")

asyncio.run(main())
```

--------------------------------

TITLE: Import Agent Framework Vendor/Platform Connectors in Python
DESCRIPTION: Illustrates how to import vendor-specific connectors like `OpenAIChatClient` from `agent_framework.openai` and `AzureOpenAIChatClient` from `agent_framework.azure`. This pattern is for integrating with external services.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework.openai import OpenAIChatClient
from agent_framework.azure import AzureOpenAIChatClient
```

--------------------------------

TITLE: Implement Logging Middleware for Agent Functions (Python)
DESCRIPTION: This Python code defines a `LoggingFunctionMiddleware` class that extends `FunctionMiddleware` to log function invocations within an agent. It records the start and end of function calls, including their duration, providing insights into agent tool usage. The middleware is then added to an `AzureAIAgentClient` instance during agent creation.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
class LoggingFunctionMiddleware(FunctionMiddleware):
    async def process(
        self,
        context: FunctionInvocationContext,
        next: Callable[[FunctionInvocationContext], Awaitable[None]]
    ) -> None:
        function_name = context.function.name
        print(f"[LoggingFunctionMiddleware] Calling function: {function_name}")

        start_time = time.time()
        await next(context)
        duration = time.time() - start_time

        print(f"[LoggingFunctionMiddleware] Function {function_name} completed in {duration:.5f}s")

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential).create_agent(
            name="WeatherAgent",
            instructions="You are a helpful weather assistant.",
            tools=get_weather,
            middleware=[SecurityAgentMiddleware(), LoggingFunctionMiddleware()]
        ) as agent
    ):
        result = await agent.run("What's the weather like in Seattle?")
        print(f"Agent: {result.text}")

asyncio.run(main())
```

--------------------------------

TITLE: Configure FSDP Offloading for GPU Memory Optimization (Python)
DESCRIPTION: This Python dictionary configuration demonstrates how to enable FSDP (Fully Sharded Data Parallel) offloading for both parameters and the optimizer. This is a technique to reduce GPU memory usage during training.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: python
CODE:
```
"fsdp_config": {
    "param_offload": True,
    "optimizer_offload": True,
}
```

--------------------------------

TITLE: Run Multimodal AI Agent Examples (Bash)
DESCRIPTION: This snippet provides bash commands to run the different multimodal examples, including OpenAI, Azure Chat, and Azure Responses clients. Users need to ensure `az login` or an API key is configured for Azure examples.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/multimodal_input/README.md

LANGUAGE: bash
CODE:
```
# Run OpenAI example
python openai_chat_multimodal.py

# Run Azure Chat example (requires az login or API key)
python azure_chat_multimodal.py

# Run Azure Responses example (requires az login or API key)
python azure_responses_multimodal.py
```

--------------------------------

TITLE: Define Azure AI Foundry Stateful Function Tool
DESCRIPTION: Configures a stateful function tool for the Azure AI Foundry Agent Service. This includes defining the function's name, description, parameters, and input/output bindings using Azure Storage Queues.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "azure_function",
      "azure_function": {
        "function": {
          "name": "{string}",
          "description": "{string}",
          "parameters": "{JSON Schema object}"
        },
        "input_binding": {
          "type": "storage_queue",
          "storage_queue": {
            "queue_service_endpoint": "{string}",
            "queue_name": "{string}"
          }
        },
        "output_binding": {
          "type": "storage_queue",
          "storage_queue": {
            "queue_service_endpoint": "{string}",
            "queue_name": "{string}"
          }
        }
      }
    }
  ]
}
```

--------------------------------

TITLE: Programmatically Launch DevUI with a Custom Agent (Python)
DESCRIPTION: This Python code demonstrates how to define a `ChatAgent` with an `OpenAIChatClient` and a custom tool, then programmatically launch the DevUI server to host this agent. The `serve` function automatically opens the browser to `http://localhost:8080`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: python
CODE:
```
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from agent_framework.devui import serve

def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72°F and sunny"

# Create your agent
agent = ChatAgent(
    name="WeatherAgent",
    chat_client=OpenAIChatClient(),
    tools=[get_weather]
)

# Launch debug UI - that's it!
serve(entities=[agent], auto_open=True)
# → Opens browser to http://localhost:8080
```

--------------------------------

TITLE: Directly Use OpenAI Chat Client for Custom Workflows (Python)
DESCRIPTION: This Python snippet demonstrates how to directly use the `OpenAIChatClient` to interact with an LLM without an agent wrapper. It constructs a list of `ChatMessage` objects for a conversation and retrieves a response, suitable for advanced or custom chat interaction patterns.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import ChatMessage
from agent_framework.openai import OpenAIChatClient

async def main():
    client = OpenAIChatClient()

    messages = [
        ChatMessage(role="system", text="You are a helpful assistant."),
        ChatMessage(role="user", text="Write a haiku about Agent Framework.")
    ]

    response = await client.get_response(messages)
    print(response.messages[0].text)

    """
    Output:

    Agents work in sync,
    Framework threads through each task—
    Code sparks collaboration.
    """

asyncio.run(main())
```

--------------------------------

TITLE: Define and use Python function tools with Agent Framework ChatAgent
DESCRIPTION: This Python snippet demonstrates how to define synchronous function tools (`get_weather`, `get_time`) and integrate them with `ChatAgent` from `agent_framework`. Tools can be registered globally during agent creation or passed per-query for dynamic selection, enabling the agent to use external capabilities like fetching weather or current time. It utilizes `AzureOpenAIResponsesClient` and `AzureCliCredential` for AI model interaction.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from datetime import datetime, timezone
from random import randint
from typing import Annotated
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")]
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

def get_time() -> str:
    """Get the current UTC time."""
    current_time = datetime.now(timezone.utc)
    return f"The current UTC time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}."

async def main():
    # Tools defined at agent creation - available for all queries
    agent = ChatAgent(
        chat_client=AzureOpenAIResponsesClient(credential=AzureCliCredential()),
        instructions="You are a helpful assistant that can provide weather and time information.",
        tools=[get_weather, get_time]
    )

    result1 = await agent.run("What's the weather like in New York?")
    print(f"Agent: {result1}")

    result2 = await agent.run("What's the weather in London and what's the current UTC time?")
    print(f"Agent: {result2}")

    # Tools can also be passed per query for dynamic tool selection
    agent_no_tools = ChatAgent(
        chat_client=AzureOpenAIResponsesClient(credential=AzureCliCredential()),
        instructions="You are a helpful assistant."
    )

    result3 = await agent_no_tools.run(
        "What's the weather like in Seattle?",
        tools=[get_weather]  # Tool only for this query
    )
    print(f"Agent: {result3}")

asyncio.run(main())
```

--------------------------------

TITLE: Installing Extras: Azure Purview Example
DESCRIPTION: Shows how users can install specific combinations of subpackages using 'extras'. This example demonstrates installing only the Azure Purview Middleware.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: bash
CODE:
```
pip install agent-framework[azure-purview]
```

--------------------------------

TITLE: Python: Set up observability with setup_observability()
DESCRIPTION: This Python code snippet demonstrates how to easily enable telemetry for the Agent Framework by calling the `setup_observability()` function. This function automatically configures exporters and providers for traces, logs, and metrics based on environment variables, simplifying the initial setup process.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
from agent_framework.observability import setup_observability

setup_observability()
```

--------------------------------

TITLE: Azure AI Foundry Agent Service - Azure AI Search
DESCRIPTION: This endpoint integrates with Azure AI Search for retrieval purposes within the Azure AI Foundry Agent Service.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /agents/azure_ai_search

### Description
This endpoint performs a search using Azure AI Search. It requires index connection details and query types.

### Method
POST

### Endpoint
/agents/azure_ai_search

### Parameters
#### Request Body
- **tools** (array) - Required - List of tools to use, must include `{"type": "azure_ai_search"}`.
- **tool_resources** (object) - Required - Resources for the tools.
  - **azure_ai_search** (object) - Required - Configuration for Azure AI Search.
    - **indexes** (array) - Required - List of Azure AI Search indexes to query.
      - **index_connection_id** (string) - Required - The connection ID for the Azure AI Search index.
      - **index_name** (string) - Required - The name of the Azure AI Search index.
      - **query_type** (string) - Required - The type of query to perform (e.g., "simple", "full").

### Request Example
```json
{
  "tools": [
    {
      "type": "azure_ai_search"
    }
  ],
  "tool_resources": {
    "azure_ai_search": {
      "indexes": [
        {
          "index_connection_id": "{string}",
          "index_name": "{string}",
          "query_type": "{string}"
        }
      ]
    }
  }
}
```

### Response
#### Success Response (200)
- **tool_calls** (array) - List of tool calls made.
  - **id** (string) - Unique identifier for the tool call.
  - **type** (string) - Type of the tool, expected to be "azure_ai_search".
  - **azure_ai_search** (object) - Response from Azure AI Search (reserved for future use).

#### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "azure_ai_search",
      "azure_ai_search": {}
    }
  ]
}
```
```

--------------------------------

TITLE: Set Azure OpenAI Environment Variables (PowerShell)
DESCRIPTION: Configures the necessary environment variables for connecting to Azure OpenAI. This includes the endpoint and optionally the deployment name. Ensure you replace placeholder values with your actual Azure OpenAI resource details.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_AzureOpenAIChatCompletion/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" # Replace with your Azure OpenAI resource endpoint
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini
```

--------------------------------

TITLE: Console Telemetry Export Setup (Python)
DESCRIPTION: This snippet demonstrates how to set up OpenTelemetry exporters for console output. It's a simplified example, and many advanced configuration options are available. It's useful for initial debugging or when the Aspire Dashboard is not accessible.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ALWAYS_ON

# Configure TracerProvider
tracer_provider = TracerProvider(
    resource=Resource.create({"service.name": "my-service"}),
    sampler=ALWAYS_ON
)

# Configure console exporter (this is a placeholder, actual exporter setup varies)
# For demonstration, we'll just log to console without a specific exporter class.
# In a real scenario, you would import and configure an exporter like ConsoleSpanExporter
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter
# span_processor = BatchSpanProcessor(ConsoleSpanExporter())

# A more realistic setup would involve setting up a specific exporter and processor
# For example:
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# span_processor = BatchSpanProcessor(OTLPSpanExporter())

# Without a concrete exporter, we can't add a processor that writes to console
# tracer_provider.add_span_processor(span_processor)

# Get a tracer instance
tracer = trace.get_tracer_provider().get_tracer(__name__)

# Example of starting and ending a span
with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("input", 123)
    print("Performing operation...")

print("Operation completed.")

```

--------------------------------

TITLE: Orchestrate Multi-Agent Workflow in Python
DESCRIPTION: This Python example illustrates how to set up and run a multi-agent workflow using the Agent Framework. It involves creating a 'writer' and a 'reviewer' agent with specific instructions, building a workflow to connect them, and then executing the workflow to get a collaborative output.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import AgentRunEvent, WorkflowBuilder
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

async def main():
    # Create chat client and agents
    chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())

    writer_agent = chat_client.create_agent(
        instructions="You are an excellent content writer. You create new content and edit based on feedback.",
        name="writer"
    )

    reviewer_agent = chat_client.create_agent(
        instructions="You are an excellent content reviewer. Provide actionable feedback in the most concise manner.",
        name="reviewer"
    )

    # Build workflow: writer -> reviewer
    workflow = (WorkflowBuilder()
        .set_start_executor(writer_agent)
        .add_edge(writer_agent, reviewer_agent)
        .build())

    # Run workflow
    events = await workflow.run(
        "Create a slogan for a new electric SUV that is affordable and fun to drive."
    )

    # Print agent outputs
    for event in events:
        if isinstance(event, AgentRunEvent):
            print(f"{event.executor_id}: {event.data}")

    print(f"{'=' * 60}\nWorkflow Outputs: {events.get_outputs()}")
    print("Final state:", events.get_final_state())

asyncio.run(main())
```

--------------------------------

TITLE: Installing Extras: All Azure Connectors Example
DESCRIPTION: Illustrates installing a broader set of related subpackages with a single extra. This example installs all Azure-related connectors.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: bash
CODE:
```
pip install agent-framework[azure]
```

--------------------------------

TITLE: Run Copilot Studio Agent Using Environment Variables (Python)
DESCRIPTION: This Python snippet demonstrates basic usage of the CopilotStudioAgent. It initializes the agent by implicitly loading configuration from environment variables and then executes a simple query, printing the result. This approach simplifies setup by relying on external configuration.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/copilotstudio/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework.microsoft import CopilotStudioAgent

async def main():
    # Create agent using environment variables
    agent = CopilotStudioAgent()

    # Run a simple query
    result = await agent.run("What is the capital of France?")
    print(result)

asyncio.run(main())
```

--------------------------------

TITLE: Build Python Agent with Custom Tools and Function Calling
DESCRIPTION: This Python snippet demonstrates how to create a `ChatAgent` using the `agent-framework` library, integrating custom tools like `get_weather` and `get_menu_specials`. The agent is configured with instructions and a list of callable tools, enabling it to process natural language queries by invoking the appropriate functions to gather and respond with information.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/README.md

LANGUAGE: python
CODE:
```
import asyncio
from typing import Annotated
from random import randint
from pydantic import Field
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


def get_menu_specials() -> str:
    """Get today's menu specials."""
    return """
    Special Soup: Clam Chowder
    Special Salad: Cobb Salad
    Special Drink: Chai Tea
    """


async def main():
    agent = ChatAgent(
        chat_client=OpenAIChatClient(),
        instructions="You are a helpful assistant that can provide weather and restaurant information.",
        tools=[get_weather, get_menu_specials]
    )

    response = await agent.run("What's the weather in Amsterdam and what are today's specials?")
    print(response)

    """
    Output:
    The weather in Amsterdam is sunny with a high of 22°C. Today's specials include
    Clam Chowder soup, Cobb Salad, and Chai Tea as the special drink.
    """

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

TITLE: Configure Azure OpenAI Environment Variables
DESCRIPTION: Set the required environment variables for connecting to Azure OpenAI Service, specifying the endpoint and an optional deployment name. These variables enable the console application to authenticate and interact with the AI model via Azure CLI credentials.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentOpenTelemetry/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
```

--------------------------------

TITLE: Configure Azure AI Foundry Environment Variables (PowerShell)
DESCRIPTION: This code snippet sets the necessary environment variables for connecting to Azure AI Foundry using the OpenAI SDK. It includes the endpoint URL, an optional API key (if not using Azure CLI authentication), and the name of the model deployment. Remember to replace placeholder values with your specific resource details.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_AzureFoundryModel/README.md

LANGUAGE: powershell
CODE:
```
# Replace with your Azure AI Foundry resource endpoint
# Ensure that you have the "/openai/v1/" path in the URL, since this is required when using the OpenAI SDK to access Azure Foundry models.
$env:AZURE_FOUNDRY_OPENAI_ENDPOINT="https://ai-foundry-<myresourcename>.services.ai.azure.com/openai/v1/"

# Optional, defaults to using Azure CLI for authentication if not provided
$env:AZURE_FOUNDRY_OPENAI_APIKEY="************"

# Optional, defaults to Phi-4-mini-instruct
$env:AZURE_FOUNDRY_MODEL_DEPLOYMENT="Phi-4-mini-instruct"
```

--------------------------------

TITLE: Example Google-style Docstring for Python Function
DESCRIPTION: Demonstrates the preferred Google-style docstring format for public API functions in Python. It includes sections for arguments, return values, and raised exceptions, providing clear documentation for developers.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
def create_agent(name: str, chat_client: ChatClientProtocol) -> Agent:
    """Create a new agent with the specified configuration.

    Args:
        name: The name of the agent.
        chat_client: The chat client to use for communication.

    Returns:
        True if the strings are the same, False otherwise.

    Raises:
        ValueError: If one of the strings is empty.
    """
    ...
```

--------------------------------

TITLE: Basic Copilot Studio Agent Execution (Python)
DESCRIPTION: Demonstrates basic non-streaming and streaming execution of a Copilot Studio agent using environment variables for configuration. It requires the agent_framework and relies on environment variables for authentication and agent identification.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/copilotstudio/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework.microsoft import CopilotStudioAgent

# Uses environment variables for configuration
async def main():
    # Create agent using environment variables
    agent = CopilotStudioAgent()

    # Run a simple query
    result = await agent.run("What is the capital of France?")
    print(result)

asyncio.run(main())
```

--------------------------------

TITLE: Copilot Studio Agent with Explicit Settings (Python)
DESCRIPTION: Shows how to configure and use a Copilot Studio agent with explicit connection settings and manual token acquisition using MSAL. This method bypasses environment variables for configuration and requires direct provision of client ID, tenant ID, and environment details.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/copilotstudio/README.md

LANGUAGE: python
CODE:
```
from agent_framework.microsoft import CopilotStudioAgent, acquire_token
from microsoft_agents.copilotstudio.client import ConnectionSettings, CopilotClient, PowerPlatformCloud, AgentType

# Acquire token manually
token = acquire_token(
    client_id="your-client-id",
    tenant_id="your-tenant-id"
)

# Create settings and client
settings = ConnectionSettings(
    environment_id="your-environment-id",
    agent_identifier="your-agent-schema-name",
    cloud=PowerPlatformCloud.PROD,
    copilot_agent_type=AgentType.PUBLISHED,
    custom_power_platform_cloud=None
)

client = CopilotClient(settings=settings, token=token)
agent = CopilotStudioAgent(client=client)
```

--------------------------------

TITLE: OpenAI Assistants Agent with Code Interpreter
DESCRIPTION: Shows how to use the `HostedCodeInterpreterTool` with OpenAI agents for writing and executing Python code. Includes helper methods for accessing code interpreter data from response chunks.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.code_interpreter.hosted_code_interpreter import HostedCodeInterpreterTool

# Initialize the tool and the client
code_interpreter_tool = HostedCodeInterpreterTool()
client = OpenAIAssistantsClient(tools=[code_interpreter_tool])
agent = ChatAgent(client=client)

# Example: Ask the agent to write and execute Python code
code_to_execute = "print(2 + 2)"
response = agent.chat(f"Write and execute the following Python code: {code_to_execute}")

print(f"Code interpreter response: {response}")

# Accessing data from response chunks (if applicable and structured)
# for chunk in agent.chat_stream(f"Write and execute: {code_to_execute}"):
#     if chunk.code_interpreter_output:
#         print(f"Output: {chunk.code_interpreter_output}")

```

--------------------------------

TITLE: LangChain Python Callbacks for Interception
DESCRIPTION: Demonstrates using custom callback handlers in LangChain Python to intercept chain execution. Handlers can modify inputs and outputs, influencing the execution flow.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
from langchain_core.callbacks import BaseCallbackHandler

class MyHandler(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        inputs['number'] += 1  # Modify inputs (write capability)
        print("Chain started!")

handler = MyHandler()

# Pass callback at runtime
chain.invoke({"number": 25}, {"callbacks": [handler]})

# Or at constructor time
chain = SomeChain(callbacks=[handler])
chain.invoke({"number": 25})
```

--------------------------------

TITLE: OpenAI Responses Agent with Code Interpreter
DESCRIPTION: Shows how to use the `HostedCodeInterpreterTool` with OpenAI agents for writing and executing Python code. Includes helper methods for accessing code interpreter data from response chunks.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.responses import OpenAIResponsesClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.code_interpreter.hosted_code_interpreter import HostedCodeInterpreterTool

# Initialize the tool and the client
code_interpreter_tool = HostedCodeInterpreterTool()
client = OpenAIResponsesClient(tools=[code_interpreter_tool])
agent = ChatAgent(client=client)

# Example: Ask the agent to write and execute Python code
code_to_execute = "print(10 * 5)"
response = agent.chat(f"Execute the following Python code: {code_to_execute}")

print(f"Code interpreter response: {response}")

# Accessing data from response chunks (if applicable and structured)
# for chunk in agent.chat_stream(f"Execute: {code_to_execute}"):
#     if chunk.code_interpreter_output:
#         print(f"Output: {chunk.code_interpreter_output}")

```

--------------------------------

TITLE: Implement and Run a Basic Agent with Tools using Agent Framework Python
DESCRIPTION: This Python example demonstrates how to define an AI agent using the Agent Framework, integrate a custom tool (`get_weather`), and execute a simple prompt. It showcases the use of `Agent`, `ai_function` decorator, and `OpenAIChatClient` for model interaction, providing a quick start for agent development.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/design/python-package-setup.md

LANGUAGE: python
CODE:
```
from typing import Annotated
from agent_framework import Agent, ai_function
from agent_framework.openai import OpenAIChatClient

@ai_function(description="Get the current weather in a given location")
async def get_weather(location: Annotated[str, "The location as a city name"]) -> str:
    """Get the current weather in a given location."""
    # Implementation of the tool to get weather
    return f"The current weather in {location} is sunny."

agent = Agent(
    name="MyAgent",
    model_client=OpenAIChatClient(),
    tools=get_weather,
    description="An agent that can get the current weather.",
)
response = await agent.run("What is the weather in Amsterdam?")
print(response)
```

--------------------------------

TITLE: Python Semantic Kernel Function Invocation Filters
DESCRIPTION: Shows how to implement function invocation filters in Python, both as standalone asynchronous functions and using the @kernel.filter decorator. These filters can intercept and modify function arguments and results. Requires the semantic-kernel library.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
import logging
from typing import Callable, Coroutine, Any
from semantic_kernel import Kernel
from semantic_kernel.filters import FilterTypes, FunctionInvocationContext
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.exceptions import OperationCancelledException

logger = logging.getLogger(__name__)

async def input_output_filter(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Coroutine[Any, Any, None]],
) -> None:
    if context.function.plugin_name != "chat":
        await next(context)
        return
    try:
        user_input = input("User:>")
    except (KeyboardInterrupt, EOFError) as exc:
        raise OperationCancelledException("User stopped the operation") from exc
    if user_input == "exit":
        raise OperationCancelledException("User stopped the operation")
    context.arguments["chat_history"].add_user_message(user_input)  # Modify arguments by adding message (write capability)

    await next(context)

    if context.result:
        logger.info(f"Usage: {context.result.metadata.get('usage')}")
        context.arguments["chat_history"].add_message(context.result.value[0])
        print(f"Mosscap:> {context.result!s}")

kernel = Kernel()
kernel.add_service(AzureChatCompletion(service_id="chat-gpt"))

# Add filter as a standalone function
kernel.add_filter("function_invocation", input_output_filter)

# Add filter via decorator
@kernel.filter(filter_type=FilterTypes.FUNCTION_INVOCATION)
async def exception_catch_filter(
    context: FunctionInvocationContext,
    next: Coroutine[FunctionInvocationContext, Any, None]
):
    try:
        await next(context)
    except Exception as e:
        logger.info(e)

# Example invocation (assuming a "chat" plugin is added)
history = ChatHistory()
result = await kernel.invoke(
    function_name="chat",
    plugin_name="chat",
    chat_history=history,
)
```

--------------------------------

TITLE: Azure AI Search Tool Call Response
DESCRIPTION: The response structure for an Azure AI Search tool call. Currently, the 'azure_ai_search' field is reserved for future use.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "azure_ai_search",
      "azure_ai_search": {} 
    }
  ]
}
```

--------------------------------

TITLE: Python: Register Reply Functions for Message Interception
DESCRIPTION: Python's AutoGen allows registering reply functions to intercept and process messages. These functions can modify message content before it's sent, supporting read/write capabilities. The `register_reply` method is used for this purpose.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
def print_messages(recipient, messages, sender, config):
    if "callback" in config and config["callback"] is not None:
        callback = config["callback"]
        callback(sender, recipient, messages[-1])
    messages[-1]["content"] += " modified"  # Modify last message content (write capability)
    print(f"Messages sent to: {recipient.name} | num messages: {len(messages)}")
    return False, None  # required to ensure the agent communication flow continues

user_proxy.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

assistant.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)
```

--------------------------------

TITLE: Renaming Chat-Specific Types - Python
DESCRIPTION: Demonstrates renaming chat-specific types like 'ChatRole' and 'ChatFinishReason' to shorter, contextually clear names in Python.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0005-python-naming-conventions.md

LANGUAGE: python
CODE:
```
class Role:
    pass

class FinishReason:
    pass
```

--------------------------------

TITLE: Create Azure OpenAI Agent with Azure CLI Authentication (C#)
DESCRIPTION: This C# snippet demonstrates initializing an AI agent using Azure OpenAI with token-based authentication via `AzureCliCredential`. It configures the agent with an endpoint and deployment name, then creates a "HaikuBot" to respond to a prompt. It requires the `Microsoft.Agents.AI.OpenAI` and `Azure.Identity` packages.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/README.md

LANGUAGE: c#
CODE:
```
// dotnet add package Microsoft.Agents.AI.OpenAI --prerelease
// dotnet add package Azure.Identity
// Use `az login` to authenticate with Azure CLI
using System;
using OpenAI;

// Replace <resource> and gpt-4o-mini with your Azure OpenAI resource name and deployment name.
var agent = new OpenAIClient(
    new BearerTokenPolicy(new AzureCliCredential(), "https://ai.azure.com/.default"),
    new OpenAIClientOptions() { Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1") })
    .GetOpenAIResponseClient("gpt-4o-mini")
    .CreateAIAgent(name: "HaikuBot", instructions: "You are an upbeat assistant that writes beautifully.");

Console.WriteLine(await agent.RunAsync("Write a haiku about Microsoft Agent Framework."));
```

--------------------------------

TITLE: Run Azure OpenAI Sample (Bash)
DESCRIPTION: Shows the command to execute an Azure OpenAI sample using `dotnet run` after navigating to the appropriate directory. This is a standard way to run .NET console applications intended for demonstrating Azure OpenAI integrations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: bash
CODE:
```
cd "AzureOpenAI\Step01_Basics"
dotnet run
```

--------------------------------

TITLE: Install Microsoft Agent Framework with pip
DESCRIPTION: This code block demonstrates how to install the Microsoft Agent Framework's core components and an optional Azure AI integration using the pip package manager. It specifies the use of '--pre' for pre-release versions, indicating ongoing development.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: bash
CODE:
```
pip install agent-framework-core --pre
# Optional: Add Azure AI integration
pip install agent-framework-azure-ai --pre
```

--------------------------------

TITLE: Set Azure OpenAI Environment Variables (PowerShell)
DESCRIPTION: Demonstrates setting environment variables for Azure OpenAI, including the endpoint and optionally the deployment name. These variables are required for applications and samples interacting directly with Azure OpenAI services or Azure OpenAI Assistants.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_OPENAI_ENDPOINT = "https://<your-project>.cognitiveservices.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o" # Optional, defaults to gpt-4o
```

--------------------------------

TITLE: Set Azure Foundry Environment Variables (PowerShell)
DESCRIPTION: This PowerShell snippet demonstrates how to configure the `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL_DEPLOYMENT_NAME` environment variables. These variables are crucial for authenticating and connecting to your Azure Foundry service. Remember to replace the placeholder for the project endpoint with your specific Azure Foundry resource.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/ModelContextProtocol/FoundryAgent_Hosted_MCP/README.md

LANGUAGE: powershell
CODE:
```
$env:FOUNDRY_PROJECT_ENDPOINT="https://your-foundry-service.services.ai.azure.com/api/projects/your-foundry-project" # Replace with your Azure Foundry resource endpoint
$env:FOUNDRY_MODEL_DEPLOYMENT_NAME="gpt-4.1-mini"  # Optional, defaults to gpt-4.1-mini
```

--------------------------------

TITLE: Configure OpenAI API Keys in .env File (Plaintext)
DESCRIPTION: Example content for the `.env` file, showing how to set `OPENAI_API_KEY` and optionally `OPENAI_CHAT_MODEL_ID` for OpenAI, or `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` for Azure OpenAI. This configures the necessary API credentials for the application.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: plaintext
CODE:
```
# For OpenAI (minimum required)
OPENAI_API_KEY="your-api-key-here"
OPENAI_CHAT_MODEL_ID="gpt-4o-mini"

# Or for Azure OpenAI
AZURE_OPENAI_ENDPOINT="your-endpoint"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="your-deployment-name"
```

--------------------------------

TITLE: Create GAIA Evaluation Script in Python
DESCRIPTION: A Python script demonstrating how to set up and run a GAIA evaluation. It defines a task runner function and initializes the GAIA runner, optionally with telemetry enabled.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/gaia/README.md

LANGUAGE: python
CODE:
```
from agent_framework.lab.gaia import GAIA, Task, Prediction, GAIATelemetryConfig

async def run_task(task: Task) -> Prediction:
    return Prediction(prediction="answer here", messages=[])

async def main() -> None:
    # Optional: Enable telemetry for detailed tracing
    telemetry_config = GAIATelemetryConfig(
        enable_tracing=True,
        trace_to_file=True,
        file_path="gaia_traces.jsonl"
    )

    runner = GAIA(telemetry_config=telemetry_config)
    await runner.run(run_task, level=1, max_n=5, parallel=2)
```

--------------------------------

TITLE: Orchestrate Sequential Multi-Agent Workflow in Python
DESCRIPTION: This Python snippet demonstrates a sequential multi-agent orchestration pattern using the `agent_framework` library. It initializes two `ChatAgent` instances, a 'Writer' and a 'Reviewer', both powered by `OpenAIChatClient`, and orchestrates their interaction to collaboratively refine a slogan through a series of steps.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


async def main():
    # Create specialized agents
    writer = ChatAgent(
        chat_client=OpenAIChatClient(),
        name="Writer",
        instructions="You are a creative content writer. Generate and refine slogans based on feedback."
    )

    reviewer = ChatAgent(
        chat_client=OpenAIChatClient(),
        name="Reviewer",
        instructions="You are a critical reviewer. Provide detailed feedback on proposed slogans."
    )

    # Sequential workflow: Writer creates, Reviewer provides feedback
    task = "Create a slogan for a new electric SUV that is affordable and fun to drive."

    # Step 1: Writer creates initial slogan
    initial_result = await writer.run(task)
    print(f"Writer: {initial_result}")

    # Step 2: Reviewer provides feedback
    feedback_request = f"Please review this slogan: {initial_result}"
    feedback = await reviewer.run(feedback_request)
    print(f"Reviewer: {feedback}")

    # Step 3: Writer refines based on feedback
    refinement_request = f"Please refine this slogan based on the feedback: {initial_result}\nFeedback: {feedback}"
    final_result = await writer.run(refinement_request)
    print(f"Final Slogan: {final_result}")

    # Example Output:
    # Writer: "Charge Forward: Affordable Adventure Awaits!"
    # Reviewer: "Good energy, but 'Charge Forward' is overused in EV marketing..."
    # Final Slogan: "Power Up Your Adventure: Premium Feel, Smart Price!"

if __name__ == "__main__":
    asyncio.run(main())
```

--------------------------------

TITLE: Import GAIA Module from Agent Framework Lab
DESCRIPTION: This Python code demonstrates how to import the GAIA class from the agent_framework.lab.gaia module. This is a common pattern for utilizing specific lab modules within the Agent Framework.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/README.md

LANGUAGE: python
CODE:
```
# Using GAIA module
from agent_framework.lab.gaia import GAIA
```

--------------------------------

TITLE: Renaming Acronyms and Method Calls - Python
DESCRIPTION: Shows the renaming of acronyms to uppercase in class names and the shortening of method names for streaming operations in Python, aligning with PEP 8 and common practices.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0005-python-naming-conventions.md

LANGUAGE: python
CODE:
```
class MCP:
    pass

class HTTP:
    pass

class Agent:
    def run_stream(self):
        pass

class Workflow:
    def run_stream(self):
        pass
```

--------------------------------

TITLE: Use Structured Outputs with OpenAI Agents (Python)
DESCRIPTION: Shows how to configure OpenAI agents to return structured data in predefined formats. This is useful for parsing agent responses into specific data structures like JSON. Requires OpenAI API key and model IDs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from openai_responses_client import OpenAIResponsesClient
from pydantic import BaseModel

# Define a Pydantic model for the desired structured output
class UserProfile(BaseModel):
    name: str
    email: str
    age: int

# Initialize the OpenAIResponsesClient
client = OpenAIResponsesClient(
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_chat_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID"),
    openai_responses_model_id=os.environ.get("OPENAI_RESPONSES_MODEL_ID"),
)

# Create an agent specifying the structured output type
agent = client.create_agent(
    response_model=UserProfile
)

# Query the agent, expecting a structured output
response = agent.query("Create a user profile for John Doe, email john.doe@example.com, age 30.")

# Access the structured data
print(f"User Name: {response.output.name}")
print(f"User Email: {response.output.email}")
print(f"User Age: {response.output.age}")
```

--------------------------------

TITLE: Python Sample Output Comment
DESCRIPTION: Shows the recommended format for documenting the expected output of a Python sample at the end of the script. This helps users verify the sample's execution.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/SAMPLE_GUIDELINES.md

LANGUAGE: python
CODE:
```
'''
Sample output:
User:> Why is the sky blue in one sentence?
Mosscap:> The sky is blue due to the scattering of sunlight by the molecules in the Earth's atmosphere,
a phenomenon known as Rayleigh scattering, which causes shorter blue wavelengths to become more
prominent in our visual perception.
'''
```

--------------------------------

TITLE: Create and Run a Simple Chat Agent in Python
DESCRIPTION: This Python example demonstrates how to create a basic ChatAgent using the Agent Framework. It initializes an agent with an OpenAI chat client and specific instructions, then runs it asynchronously to process a query and print the result. The agent adheres to provided rules for generating responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

async def main():
    agent = ChatAgent(
        chat_client=OpenAIChatClient(),
        instructions="""
        1) A robot may not injure a human being...
        2) A robot must obey orders given it by human beings...
        3) A robot must protect its own existence...

        Give me the TLDR in exactly 5 words.
        """
    )

    result = await agent.run("Summarize the Three Laws of Robotics")
    print(result)

asyncio.run(main())
# Output: Protect humans, obey, self-preserve, prioritized.
```

--------------------------------

TITLE: Renaming Content and Annotation Types - Python
DESCRIPTION: Illustrates renaming conventions for content and annotation types in Python. It focuses on using plural for union types and 'Base' prefixes for base classes, while maintaining clarity and consistency.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0005-python-naming-conventions.md

LANGUAGE: python
CODE:
```
class BaseContent:
    pass

class Contents:
    pass

class Annotations:
    pass

class BaseAnnotation:
    pass
```

--------------------------------

TITLE: Configure and Run Copilot Studio Agent with Explicit Settings (Python)
DESCRIPTION: This example shows how to explicitly configure the CopilotStudioAgent by manually acquiring an authentication token and defining connection settings. It provides greater control over the agent's behavior, allowing for custom token acquisition and specific connection parameters, before running a query and printing its output.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/copilotstudio/README.md

LANGUAGE: python
CODE:
```
import asyncio
import os
from agent_framework.microsoft import CopilotStudioAgent, acquire_token
from microsoft_agents.copilotstudio.client import ConnectionSettings, CopilotClient, PowerPlatformCloud, AgentType

async def main():
    # Acquire authentication token
    token = acquire_token(
        client_id=os.environ["COPILOTSTUDIOAGENT__AGENTAPPID"],
        tenant_id=os.environ["COPILOTSTUDIOAGENT__TENANTID"]
    )

    # Create connection settings
    settings = ConnectionSettings(
        environment_id=os.environ["COPILOTSTUDIOAGENT__ENVIRONMENTID"],
        agent_identifier=os.environ["COPILOTSTUDIOAGENT__SCHEMANAME"],
        cloud=PowerPlatformCloud.PROD,
        copilot_agent_type=AgentType.PUBLISHED,
        custom_power_platform_cloud=None
    )

    # Create client and agent
    client = CopilotClient(settings=settings, token=token)
    agent = CopilotStudioAgent(client=client)

    # Run a query
    result = await agent.run("What is the capital of Italy?")
    print(result)

asyncio.run(main())
```

--------------------------------

TITLE: Renaming Chat Protocols and Base Classes - Python
DESCRIPTION: Demonstrates renaming conventions for chat-related protocols and base classes in Python. It shows how to adopt shorter, contextually clear names and use 'Base' prefixes for common ancestor classes.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0005-python-naming-conventions.md

LANGUAGE: python
CODE:
```
class ChatClientProtocol:
    pass

class BaseChatClient:
    pass
```

--------------------------------

TITLE: Convert Python Class to Pydantic AFBaseModel
DESCRIPTION: Demonstrates how to convert a standard Python class into a Pydantic `AFBaseModel` for serialization. It shows inheriting from `AFBaseModel` and using `pydantic.Field` for default factory values, similar to dataclasses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from pydantic import Field
from ._pydantic import AFBaseModel

class A(AFBaseModel):
    # The notation for the fields is similar to dataclasses.
    a: int
    b: float
    c: list[float]
    # Only, instead of using dataclasses.field, you would use pydantic.Field
    d: dict[str, tuple[float, str]] = Field(default_factory=dict)
```

--------------------------------

TITLE: Set Azure Foundry Environment Variables (PowerShell)
DESCRIPTION: This PowerShell script sets two critical environment variables: AZURE_FOUNDRY_PROJECT_ENDPOINT and AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME. These variables are used to specify the Azure Foundry service endpoint and the desired deployment name (e.g., gpt-4o-mini). Ensure you replace the placeholder endpoint with your actual Azure Foundry resource endpoint for proper connectivity.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_AzureFoundryAgent/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_FOUNDRY_PROJECT_ENDPOINT="https://your-foundry-service.services.ai.azure.com/api/projects/your-foundry-project" # Replace with your Azure Foundry resource endpoint
$env:AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini
```

--------------------------------

TITLE: Connect and Run Pipeline Components (Python)
DESCRIPTION: Demonstrates how to connect different components within a pipeline and then run the pipeline with initial input. This involves establishing communication channels between components like 'generator', 'router', and 'tool_invoker', and then executing the pipeline to process a user query.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
pipeline.connect("generator.replies", "router.replies")
pipeline.connect("router.there_are_tool_calls", "tool_invoker.messages")
pipeline.connect("tool_invoker.messages", "message_collector.messages")
pipeline.connect("router.final_replies", "message_collector.messages")

result = pipeline.run({"generator": {"messages": [ChatMessage.from_user("What's the weather in Berlin?")]}})
print(result["message_collector"]["messages"])
```

--------------------------------

TITLE: Use Function Tools with OpenAI Agents (Python)
DESCRIPTION: Demonstrates integrating function tools with OpenAI agents. This includes defining tools at the agent level and providing tools dynamically with specific queries. Requires OpenAI API key and model IDs to be set as environment variables.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools import FunctionTool
from openai_responses_client import OpenAIResponsesClient

# Example function tool definition
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location.

    Args:
        location (str): The city and state, e.g. San Francisco, CA
        unit (str): The unit of measurement to use from the following set: degrees Celsius, degrees Fahrenheit.

    Returns:
        str: The current weather conditions in the specified location and unit.
    """
    return f"The weather in {location} is {unit}."

# Initialize the OpenAIResponsesClient
client = OpenAIResponsesClient(
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_chat_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID"),
    openai_responses_model_id=os.environ.get("OPENAI_RESPONSES_MODEL_ID"),
)

# Define agent-level tools
agent_tools = [
    FunctionTool.from_function(get_current_weather, name="get_weather", description="Get the current weather in a given location.")
]

# Create an agent with tools
agent = client.create_agent(tools=agent_tools)

# Query the agent with a tool provided at run-level
response = agent.query("What is the weather in Boston, MA?", tools=[FunctionTool.from_function(get_current_weather, name="get_weather", description="Get the current weather in a given location.")])
print(response.output)

# Query the agent using agent-level tools
response_agent_tools = agent.query("What is the weather in London, UK using celsius?")
print(response_agent_tools.output)
```

--------------------------------

TITLE: Implement Vector Store-Based File Search for Document Retrieval (Python)
DESCRIPTION: This Python example illustrates how to perform vector store-based file search for document retrieval using `HostedFileSearchTool`. It involves creating a vector store, uploading a document, and then querying an agent to answer questions based on the stored content. Cleanup for the vector store and file is also included.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import HostedFileSearchTool, HostedVectorStoreContent
from agent_framework.openai import OpenAIResponsesClient

async def main():
    client = OpenAIResponsesClient()

    # Create vector store with document
    file = await client.client.files.create(
        file=("todays_weather.txt", b"The weather today is sunny with a high of 75F."),
        purpose="user_data"
    )

    vector_store = await client.client.vector_stores.create(
        name="knowledge_base",
        expires_after={"anchor": "last_active_at", "days": 1}
    )

    result = await client.client.vector_stores.files.create_and_poll(
        vector_store_id=vector_store.id,
        file_id=file.id
    )

    if result.last_error:
        raise Exception(f"Vector store processing failed: {result.last_error.message}")

    # Query with file search
    vector_store_content = HostedVectorStoreContent(vector_store_id=vector_store.id)
    response = await client.get_response(
        "What is the weather today? Do a file search to find the answer.",
        tools=[HostedFileSearchTool(inputs=vector_store_content)],
        tool_choice="auto"
    )

    print(f"Assistant: {response}")

    # Cleanup
    await client.client.vector_stores.delete(vector_store_id=vector_store.id)
    await client.client.files.delete(file_id=file.id)

asyncio.run(main())
```

--------------------------------

TITLE: Renaming Agent and Tool Protocols - Python
DESCRIPTION: This snippet illustrates renaming conventions for agent and tool-related protocols in Python. It follows the guidance to remove redundant prefixes like 'AI' and use 'Protocol' suffixes for interfaces.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0005-python-naming-conventions.md

LANGUAGE: python
CODE:
```
class AgentProtocol:
    pass

class ToolProtocol:
    pass
```

--------------------------------

TITLE: Set Azure OpenAI Environment Variables (PowerShell)
DESCRIPTION: Sets the necessary environment variables for connecting to Azure OpenAI, including the endpoint and deployment name. Ensure you replace placeholder values with your actual Azure OpenAI resource details.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/Agents/Agent_Step11_UsingImages/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" # Replace with your Azure OpenAI endpoint
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o" # Replace with your model deployment name (optional, defaults to gpt-4o)
```

--------------------------------

TITLE: Set Up Python Environment with UV (Bash)
DESCRIPTION: Navigates to the Python project directory, installs development dependencies using `uv sync --dev`, and activates the Python virtual environment. This prepares the environment for running Python-based components.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
cd python
uv sync --dev
source .venv/bin/activate
```

--------------------------------

TITLE: Azure AI Search Request
DESCRIPTION: JSON structure for initiating a search request using Azure AI Search within the agent framework. It specifies the index connection details and query type.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "azure_ai_search"
    }
  ],
  "tool_resources": {
    "azure_ai_search": {
      "indexes": [
        {
          "index_connection_id": "{string}",
          "index_name": "{string}",
          "query_type": "{string}"
        }
      ]
    }
  }
}
```

--------------------------------

TITLE: Avoid Direct Python Logging Module Imports
DESCRIPTION: Illustrates an anti-pattern for logging within the `agent_framework` project. Directly importing and using Python's standard `logging` module is discouraged in favor of the project's centralized `get_logger` utility.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
# ❌ Avoid this
import logging
logger = logging.getLogger(__name__)
```

--------------------------------

TITLE: Run Azure OpenAI Assistants Sample (Bash)
DESCRIPTION: Shows the console commands to navigate to an Azure OpenAI Assistants sample directory and execute it using `dotnet run`. This is the procedure for running .NET console applications designed to showcase Azure OpenAI Assistants.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: bash
CODE:
```
cd "AzureOpenAIAssistants\Step01_Basics"
dotnet run
```

--------------------------------

TITLE: Run Redis Basics Example
DESCRIPTION: Executes the 'redis_basics.py' example script, demonstrating standalone provider usage, agent integration, and tool usage with memory persistence.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/context_providers/redis/README.md

LANGUAGE: python
CODE:
```
python redis_basics.py
```

--------------------------------

TITLE: Manage Threads with OpenAI Agents (Python)
DESCRIPTION: Demonstrates thread management for maintaining conversation context with OpenAI agents. Includes automatic thread creation for stateless interactions and explicit management for stateful conversations. Requires OpenAI API key and model IDs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from openai_responses_client import OpenAIResponsesClient

# Initialize the OpenAIResponsesClient
client = OpenAIResponsesClient(
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_chat_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID"),
    openai_responses_model_id=os.environ.get("OPENAI_RESPONSES_MODEL_ID"),
)

# Example 1: Automatic thread creation (stateless conversation)
# Each query starts a new thread by default if no thread_id is provided.
response_stateless = client.query("Hello, who are you?")
print(f"Stateless response: {response_stateless.output}")

# Example 2: Explicit thread management (stateful conversation)
# Create a new thread
thread = client.create_thread()
print(f"Created thread with ID: {thread.id}")

# Query within the created thread
response_stateful_1 = client.query("What is the capital of France?", thread_id=thread.id)
print(f"Stateful response 1: {response_stateful_1.output}")

# Continue the conversation in the same thread
response_stateful_2 = client.query("And what is its population?", thread_id=thread.id)
print(f"Stateful response 2: {response_stateful_2.output}")

# Retrieve conversation history from the thread
messages = client.list_messages(thread_id=thread.id)
print("\nConversation History:")
for msg in messages:
    print(f"{msg.role}: {msg.content}")
```

--------------------------------

TITLE: Microsoft Fabric Data Agent Tool Definition (JSON)
DESCRIPTION: Defines a data agent tool for Microsoft Fabric within the Azure AI Foundry Agent Service. The request includes connection details specifying a connection ID.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "fabric_dataagent",
      "fabric_dataagent": {
        "connections": [
          {
            "connection_id": "{string}"
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: Set API Keys as Environment Variables for Agent Framework
DESCRIPTION: This snippet shows how to configure API keys and model IDs for OpenAI and Azure OpenAI services using environment variables. These variables provide authentication credentials and model specifications, which are essential for the framework to interact with Large Language Models.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: bash
CODE:
```
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL_ID=...
OPENAI_RESPONSES_MODEL_ID=...
...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
...
AZURE_AI_PROJECT_ENDPOINT=...
AZURE_AI_MODEL_DEPLOYMENT_NAME=...
```

--------------------------------

TITLE: Python Code Section Comments
DESCRIPTION: Illustrates how to use comments within Python code to delineate and explain different sections or steps of a sample. This aids in tracking complexity and understanding the code flow.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/SAMPLE_GUIDELINES.md

LANGUAGE: python
CODE:
```
# 1. Create the instance of the Kernel to register the plugin and service.
...

# 2. Create the agent with the kernel instance.
...
```

--------------------------------

TITLE: Install Microsoft Agent Framework in Development Mode (Python)
DESCRIPTION: This command installs the complete Microsoft Agent Framework for Python, including all core components and integration packages. It's recommended for local development and exploration, using the `--pre` flag for preview versions.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/README.md

LANGUAGE: bash
CODE:
```
pip install agent-framework --pre
```

--------------------------------

TITLE: Original Python Class for Pydantic Conversion Example
DESCRIPTION: Presents a standard Python class `A` initialized with various data types, including a list and a dictionary. This serves as the starting point to demonstrate how to convert a regular class into a Pydantic `AFBaseModel` for serialization.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
class A:
    def __init__(self, a: int, b: float, c: List[float], d: dict[str, tuple[float, str]] = {}):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
```

--------------------------------

TITLE: Set Azure OpenAI Endpoint (Console)
DESCRIPTION: This command sets the Azure OpenAI service endpoint as an environment variable. This is crucial for the agent to connect to the correct Azure OpenAI resource. Replace the placeholder with your actual resource endpoint.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/ModelContextProtocol/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" # Replace with your Azure OpenAI resource endpoint
```

--------------------------------

TITLE: Use Agent Framework Chat Clients Directly in Python
DESCRIPTION: This Python snippet shows how to interact directly with the underlying chat client, bypassing the agent wrapper for more granular control. It demonstrates sending a list of ChatMessage objects to an OpenAIChatClient to get a response, which is useful for custom conversational flows.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework.openai import OpenAIChatClient
from agent_framework import ChatMessage, Role

async def main():
    client = OpenAIChatClient()

    messages = [
        ChatMessage(role=Role.SYSTEM, text="You are a helpful assistant."),
        ChatMessage(role=Role.USER, text="Write a haiku about Agent Framework.")
    ]

    response = await client.get_response(messages)
    print(response.messages[0].text)

    """
    Output:

    Agents work in sync,
    Framework threads through each task—
    Code sparks collaboration.
    """

asyncio.run(main())
```

--------------------------------

TITLE: LangGraph Python Callbacks with Langfuse Integration
DESCRIPTION: Illustrates using LangGraph's inherited callback functionality, specifically integrating with Langfuse for observability. This example shows how to modify input messages within a streaming context.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
from langfuse.langchain import CallbackHandler
from langchain_core.messages import HumanMessage

class MyLangfuseHandler(CallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        inputs['messages'][0].content += " modified"  # Modify input messages (write capability)
        super().on_chain_start(serialized, inputs, **kwargs)

langfuse_handler = MyLangfuseHandler()

# Stream with callback in config
for s in graph.stream(
    {"messages": [HumanMessage(content="What is Langfuse?")]},
    config={"callbacks": [langfuse_handler]}
):
    print(s)
```

--------------------------------

TITLE: Implement Agent Middleware for Security Checks in Python
DESCRIPTION: This Python example shows how to create a class-based `AgentMiddleware` to intercept and process agent run requests. The `SecurityAgentMiddleware` checks for sensitive keywords in the input message and blocks the request if found, demonstrating how to prevent further execution using the `context.result` property.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
import time
from collections.abc import Awaitable, Callable
from agent_framework import (
    AgentMiddleware, AgentRunContext, AgentRunResponse, ChatMessage, Role,
    FunctionInvocationContext, FunctionMiddleware
)
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Agent middleware: security check
class SecurityAgentMiddleware(AgentMiddleware):
    async def process(
        self,
        context: AgentRunContext,
        next: Callable[[AgentRunContext], Awaitable[None]]
    ) -> None:
        last_message = context.messages[-1] if context.messages else None
        if last_message and last_message.text:
            query = last_message.text
            if "password" in query.lower() or "secret" in query.lower():
                print("[SecurityAgentMiddleware] Blocking sensitive request")
                context.result = AgentRunResponse(
                    messages=[ChatMessage(
                        role=Role.ASSISTANT,
                        text="Detected sensitive information, request blocked."
                    )]
                )
                return  # Don't call next() to block execution

        print("[SecurityAgentMiddleware] Security check passed")
        await next(context)
```

--------------------------------

TITLE: Define Azure AI Foundry OpenAPI Tool
DESCRIPTION: Defines an OpenAPI tool for the Azure AI Foundry Agent Service. This configuration allows the agent to understand and interact with external services described by an OpenAPI specification.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "openapi",
      "openapi": {
        "description": "{string}",
        "name": "{string}",
        "auth": {
          "type": "{string}"
        },
        "spec": "{OpenAPI specification object}"
      }
    }
  ]
}
```

--------------------------------

TITLE: Python Sample Summary Comment
DESCRIPTION: Demonstrates the required format for a summary comment at the beginning of Python sample files. This comment should explain the sample's purpose, main components, and any specific concepts involved.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/SAMPLE_GUIDELINES.md

LANGUAGE: python
CODE:
```
'''
This sample shows how to create a chatbot. This sample uses the following two main components:
- a ChatCompletionService: This component is responsible for generating responses to user messages.
- a ChatHistory: This component is responsible for keeping track of the chat history.
The chatbot in this sample is called Mosscap, who responds to user messages with long flowery prose.
'''
```

--------------------------------

TITLE: Instantiate OpenAIChatClient with custom .env file
DESCRIPTION: This Python code demonstrates how to initialize an `OpenAIChatClient` instance, specifying a custom environment file path. This allows the client to load API keys and other configuration from a file like `openai.env` instead of relying solely on system environment variables.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework.openai import OpenAIChatClient

chat_client = OpenAIChatClient(env_file_path="openai.env")
```

--------------------------------

TITLE: Encode File to Data URI for Multimodal Content (Python)
DESCRIPTION: This Python code demonstrates how to open a file, encode its binary data to base64, and format it as a Data URI. The resulting Data URI can then be used with `DataContent` for sending multimodal input to AI agents.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/multimodal_input/README.md

LANGUAGE: python
CODE:
```
import base64

# Load and encode your file
with open("path/to/your/image.jpg", "rb") as f:
    image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    image_uri = f"data:image/jpeg;base64,{image_base64}"

# Use in DataContent
DataContent(
    uri=image_uri,
    media_type="image/jpeg"
)
```

--------------------------------

TITLE: Function Calling: Azure AI Foundry Agent Service (JSON)
DESCRIPTION: Defines the JSON structure for message requests and tool call responses when using function calling with the Azure AI Foundry Agent Service. This includes specifying tool types, function descriptions, names, and parameters.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "function",
      "function": {
        "description": "{string}",
        "name": "{string}",
        "parameters": "{JSON Schema object}"
      }
    }
  ]
}
```

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "function",
      "function": {
        "name": "{string}",
        "arguments": "{JSON object}"
      }
    }
  ]
}
```

--------------------------------

TITLE: Run Azure AI Foundry Sample (Bash)
DESCRIPTION: Illustrates how to navigate to an Azure AI Foundry sample directory and run it using `dotnet run` within a bash-like shell. This command compiles and executes the console application, initiating the sample's functionality.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: bash
CODE:
```
cd "AzureAIFoundry\Step01_Basics"
dotnet run
```

--------------------------------

TITLE: Azure AI Foundry File Search Request
DESCRIPTION: Defines the JSON structure for a file search request in Azure AI Foundry Agent Service. It specifies the tools to be used and the configuration for file search, including vector store IDs and data source URIs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "tool_resources": {
    "file_search": {
      "vector_store_ids": ["{string}"],
      "vector_stores": [
        {
          "name": "{string}",
          "configuration": {
            "data_sources": [
              {
                "type": {
                  "id_asset": "{string}",
                  "uri_asset": "{string}"
                },
                "uri": "{string}"
              }
            ]
          }
        }
      ]
    }
  }
}
```

--------------------------------

TITLE: Azure AI Foundry Agent Service Code Interpreter Request and Response
DESCRIPTION: Defines the JSON structure for a message request to enable the code interpreter tool and the corresponding tool call response. It includes parameters for file IDs and data sources in the request, and output types like images and logs in the response. .NET support is confirmed.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "tool_resources": {
    "code_interpreter": {
      "file_ids": ["{string}"],
      "data_sources": [
        {
          "type": {
            "id_asset": "{string}",
            "uri_asset": "{string}"
          },
          "uri": "{string}"
        }
      ]
    }
  }
}
```

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "code_interpreter",
      "code_interpreter": {
        "input": "{string}",
        "outputs": [
          {
            "type": "image",
            "file_id": "{string}"
          },
          {
            "type": "logs",
            "logs": "{string}"
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: Build Python workflows with custom and function-based executors
DESCRIPTION: This Python example demonstrates constructing a directed acyclic graph (DAG) workflow using `WorkflowBuilder` from `agent_framework`. It defines a custom `UpperCase` `Executor` class and a function-based `reverse_text` executor. The workflow processes an input string by first converting it to uppercase and then reversing it, showcasing how to connect executors with edges and retrieve workflow outputs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import Executor, WorkflowBuilder, WorkflowContext, executor, handler
from typing_extensions import Never

# Custom Executor class
class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert input to uppercase and forward to next node.

        WorkflowContext[str] indicates this executor sends str messages downstream.
        """
        result = text.upper()
        await ctx.send_message(result)

# Function-based executor
@executor(id="reverse_text_executor")
async def reverse_text(text: str, ctx: WorkflowContext[Never, str]) -> None:
    """Reverse the input string and yield workflow output.

    WorkflowContext[Never, str] means:
    - Never: doesn't send messages to downstream nodes
    - str: yields workflow output of type str
    """
    result = text[::-1]
    await ctx.yield_output(result)

async def main():
    upper_case = UpperCase(id="upper_case_executor")

    # Build workflow: upper_case -> reverse_text
    workflow = (WorkflowBuilder()
        .add_edge(upper_case, reverse_text)
        .set_start_executor(upper_case)
        .build())

    # Run workflow
    events = await workflow.run("hello world")
    print(events.get_outputs())  # ['DLROW OLLEH']
    print("Final state:", events.get_final_state())  # WorkflowRunState.COMPLETED

asyncio.run(main())
```

--------------------------------

TITLE: Instantiating an OpenAI Chat Client in Python
DESCRIPTION: This code snippet shows how to instantiate an `OpenAIChatClient` by specifying the path to an environment file. This is an example of using specific `kwargs` for configuration rather than a generic `**kwargs`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
chat_completion = OpenAIChatClient(env_file_path="openai.env")
```

--------------------------------

TITLE: Azure AI Foundry Agent Service - Function Calling
DESCRIPTION: Documentation for function calling within the Azure AI Foundry Agent Service, detailing the structure of message requests and tool call responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Azure AI Foundry Agent Service - Function Calling

### Description
This section details the message request and tool call response formats for function calling in the Azure AI Foundry Agent Service.

### Method
Not specified (details provided for request/response bodies)

### Endpoint
Not specified

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools available to the agent.
  - **type** (string) - Required - Must be "function".
  - **function** (object) - Required - Describes the function.
    - **description** (string) - Required - A natural language description of what the function does, used to match requests to functions.
    - **name** (string) - Required - The name of the function.
    - **parameters** (object) - Required - The parameters the function expects, represented as a JSON Schema object.

### Request Example
```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "description": "{string}",
        "name": "{string}",
        "parameters": "{JSON Schema object}"
      }
    }
  ]
}
```

### Response
#### Tool Call Response
- **tool_calls** (array) - Contains the tool calls made by the agent.
  - **id** (string) - The ID of the tool call.
  - **type** (string) - Must be "function".
  - **function** (object) - Details of the function call.
    - **name** (string) - The name of the function to call.
    - **arguments** (object) - The arguments to pass to the function, in JSON format.

#### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "function",
      "function": {
        "name": "{string}",
        "arguments": "{JSON object}"
      }
    }
  ]
}
```
```

--------------------------------

TITLE: Enhance Agent Framework Agents with Custom Tools and Functions in Python
DESCRIPTION: This advanced Python example illustrates how to extend an Agent Framework ChatAgent with custom tools (functions) to perform specific actions. It defines 'get_weather' and 'get_menu_specials' functions, then registers them with the agent, allowing the agent to use these tools based on user prompts to provide enriched responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/README.md

LANGUAGE: python
CODE:
```
import asyncio
from typing import Annotated
from random import randint
from pydantic import Field
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


def get_menu_specials() -> str:
    """Get today's menu specials."""
    return """
    Special Soup: Clam Chowder
    Special Salad: Cobb Salad
    Special Drink: Chai Tea
    """


async def main():
    agent = ChatAgent(
        chat_client=OpenAIChatClient(),
        instructions="You are a helpful assistant that can provide weather and restaurant information.",
        tools=[get_weather, get_menu_specials]
    )

    response = await agent.run("What's the weather in Amsterdam and what are today's specials?")
    print(response)

    # Output:
    # The weather in Amsterdam is sunny with a high of 22°C. Today's specials include
    # Clam Chowder soup, Cobb Salad, and Chai Tea as the special drink.

asyncio.run(main())
```

--------------------------------

TITLE: Manage Persistent Agent Conversations with Redis (Python)
DESCRIPTION: This Python example demonstrates how to maintain conversation state across sessions using `AgentThread` and `RedisChatMessageStore`. It shows how to store and retrieve chat messages in Redis, allowing an agent to remember previous interactions even after an application restart. The `conversation_id` is crucial for linking messages to a specific thread.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework import AgentThread
from agent_framework.openai import OpenAIChatClient
from agent_framework.redis import RedisChatMessageStore

async def main():
    conversation_id = "persistent_chat_001"

    # Phase 1: Start conversation
    store1 = RedisChatMessageStore(
        redis_url="redis://localhost:6379",
        thread_id=conversation_id
    )

    thread1 = AgentThread(message_store=store1)
    agent = OpenAIChatClient().create_agent(
        name="PersistentBot",
        instructions="You are a helpful assistant. Remember our conversation history."
    )

    # Initial conversation
    response1 = await agent.run(
        "Hello! I'm working on a Python project about machine learning.",
        thread=thread1
    )
    print(f"Agent: {response1.text}")

    response2 = await agent.run(
        "I'm specifically interested in neural networks.",
        thread=thread1
    )
    print(f"Agent: {response2.text}")

    print(f"Stored {len(await store1.list_messages())} messages")
    await store1.aclose()

    # Phase 2: Resume conversation (simulating app restart)
    store2 = RedisChatMessageStore(
        redis_url="redis://localhost:6379",
        thread_id=conversation_id  # Same thread ID
    )

    thread2 = AgentThread(message_store=store2)

    # Agent remembers previous context
    response3 = await agent.run("What was I working on before?", thread=thread2)
    print(f"Agent: {response3.text}")

    # Cleanup
    await store2.clear()
    await store2.aclose()

asyncio.run(main())
```

--------------------------------

TITLE: Convert Python Class with Generics to Pydantic AFBaseModel
DESCRIPTION: Illustrates how to make a Python class with generic types (`T1`, `T2`) serializable using `AFBaseModel` and `typing.Generic`. It's crucial to specify `T1` and `T2` in the `Generic` argument for Pydantic to handle serialization correctly.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from typing import Generic, TypeVar

from ._pydantic import AFBaseModel

T1 = TypeVar("T1")
T2 = TypeVar("T2", bound=<some class>)

class A(AFBaseModel, Generic[T1, T2]):
    # T1 and T2 must be specified in the Generic argument otherwise, pydantic will
    # NOT be able to serialize this class
    a: int
    b: T1
    c: T2
```

--------------------------------

TITLE: Authenticate with Entra ID using DefaultAzureCredential
DESCRIPTION: Illustrates how to authenticate with Application Insights using Entra ID by passing a `DefaultAzureCredential` object to the `setup_observability()` function. This is an alternative to using a connection string.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
from azure.identity import DefaultAzureCredential

# Assuming setup_observability can accept a credential parameter
# setup_observability(credential=DefaultAzureCredential())

```

--------------------------------

TITLE: OpenAPI Spec Tool - Azure AI Foundry
DESCRIPTION: Defines how to use an OpenAPI specification as a tool within the Azure AI Foundry Agent Service.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Azure AI Foundry Agent Service - OpenAPI Spec Tool

### Description
This section describes the structure for defining an OpenAPI specification as a tool for the Azure AI Foundry Agent Service.

### Method
Not applicable (Configuration)

### Endpoint
Not applicable (Configuration)

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools to be used by the agent.
  - **type** (string) - Required - The type of the tool, should be "openapi".
  - **openapi** (object) - Required - Configuration for the OpenAPI tool.
    - **description** (string) - Optional - A description of the OpenAPI tool.
    - **name** (string) - Optional - The name of the OpenAPI tool.
    - **auth** (object) - Optional - Authentication configuration for the OpenAPI tool.
      - **type** (string) - Required - The type of authentication.
    - **spec** (object) - Required - The OpenAPI specification object.

### Request Example
```json
{
  "tools": [
    {
      "type": "openapi",
      "openapi": {
        "description": "{string}",
        "name": "{string}",
        "auth": {
          "type": "{string}"
        },
        "spec": "{OpenAPI specification object}"
      }
    }
  ]
}
```

### Response
#### Success Response (200)
- **tool_calls** (array) - A list of tool calls made by the agent.
  - **id** (string) - The unique identifier for the tool call.
  - **type** (string) - The type of the tool call, should be "openapi".
  - **openapi** (object) - Reserved for future use.

#### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "openapi",
      "openapi": {}
    }
  ]
}
```
```

--------------------------------

TITLE: Configure Application Insights Connection String
DESCRIPTION: This optional configuration sets the connection string for Azure Application Insights, allowing the agent to send telemetry data for production monitoring. Replace the placeholder with your actual Application Insights connection string.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentOpenTelemetry/README.md

LANGUAGE: powershell
CODE:
```
$env:APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=XXXX;IngestionEndpoint=https://XXXX.applicationinsights.azure.com/;LiveEndpoint=https://XXXXX.livediagnostics.monitor.azure.com/;ApplicationId=XXXXX"
```

--------------------------------

TITLE: Azure AI Foundry Agent Service - Code Interpreter
DESCRIPTION: This section describes the Code Interpreter tool integration within the Azure AI Foundry Agent Service, including its message request and tool call response structure.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Azure AI Foundry Agent Service - Code Interpreter

### Description
This describes the integration of the code interpreter tool within the Azure AI Foundry Agent Service. It includes the structure for message requests and the expected tool call responses.

### Method
POST (implied, as part of a larger message request)

### Endpoint
Not explicitly defined, assumed to be part of a broader agent service endpoint.

### Parameters
#### Request Body
- **tools** (array) - Required - Specifies the tools to be used, including 'code_interpreter'.
  - **type** (string) - Required - Must be 'code_interpreter'.
- **tool_resources** (object) - Optional - Resources for the tools.
  - **code_interpreter** (object) - Optional - Configuration for the code interpreter.
    - **file_ids** (array of strings) - Optional - A list of file IDs to be used by the code interpreter.
    - **data_sources** (array of objects) - Optional - Data sources for the code interpreter.
      - **type** (object) - Required - The type of data source.
        - **id_asset** (string) - Required - Asset ID of the data source.
        - **uri_asset** (string) - Required - Asset URI of the data source.
      - **uri** (string) - Required - URI of the data source.

### Response
#### Success Response (200 OK)
- **tool_calls** (array) - Contains the results of the tool execution.
  - **id** (string) - Unique identifier for the tool call.
  - **type** (string) - Type of the tool call, should be 'code_interpreter'.
  - **code_interpreter** (object) - Details of the code interpreter execution.
    - **input** (string) - The code executed.
    - **outputs** (array of objects) - The results of the code execution.
      - **type** (string) - Type of the output ('image' or 'logs').
      - **file_id** (string) - (if type is 'image') The ID of the generated image file.
      - **logs** (string) - (if type is 'logs') The execution logs.

### Request Example
```json
{
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "tool_resources": {
    "code_interpreter": {
      "file_ids": ["{string}"],
      "data_sources": [
        {
          "type": {
            "id_asset": "{string}",
            "uri_asset": "{string}"
          },
          "uri": "{string}"
        }
      ]
    }
  }
}
```

### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "code_interpreter",
      "code_interpreter": {
        "input": "{string}",
        "outputs": [
          {
            "type": "image",
            "file_id": "{string}"
          },
          {
            "type": "logs",
            "logs": "{string}"
          }
        ]
      }
    }
  ]
}
```
```

--------------------------------

TITLE: Run Orchestration and Workflow Samples (Python)
DESCRIPTION: Demonstrates advanced agent orchestration and workflow patterns, including sequential, concurrent, and fan-out/fan-in processes. This involves setting up a virtual environment, installing necessary SDKs, and running specific workflow scripts.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/semantic-kernel-migration/README.md

LANGUAGE: Python
CODE:
```
cd samantic-kernel-migration
uv venv --python 3.10 .venv-migration
source .venv-migration/bin/activate
uv pip install semantic-kernel agent-framework
uv run python orchestrations/sequential.py
```

LANGUAGE: Python
CODE:
```
uv run python processes/fan_out_fan_in_process.py
```

--------------------------------

TITLE: Create Basic AI Agent with Azure OpenAI
DESCRIPTION: This example demonstrates how to create a basic AI agent using the Microsoft Agent Framework, configuring it with Azure OpenAI. It shows how to authenticate using Azure CLI credentials and define the agent's persona. The agent is then used to generate both non-streaming and streaming text responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

async def main():
    # Create agent with Azure OpenAI Responses Client
    # Automatically uses AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME,
    # and AZURE_OPENAI_API_VERSION from environment variables
    agent = AzureOpenAIResponsesClient(
        credential=AzureCliCredential()
    ).create_agent(
        name="HaikuBot",
        instructions="You are an upbeat assistant that writes beautifully."
    )

    # Non-streaming response
    result = await agent.run("Write a haiku about Microsoft Agent Framework.")
    print(result)

    # Streaming response
    async for chunk in agent.run_stream("Write another haiku about AI agents."):
        if chunk.text:
            print(chunk.text, end="", flush=True)

asyncio.run(main())
```

LANGUAGE: csharp
CODE:
```
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;
using OpenAI;

// Create agent with Azure OpenAI
var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
var deploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME")
    ?? "gpt-4o-mini";

AIAgent agent = new AzureOpenAIClient(
    new Uri(endpoint),
    new AzureCliCredential())
    .GetChatClient(deploymentName)
    .CreateAIAgent(
        name: "HaikuBot",
        instructions: "You are an upbeat assistant that writes beautifully.");

// Non-streaming response
Console.WriteLine(await agent.RunAsync("Write a haiku about Microsoft Agent Framework."));

// Streaming response
await foreach (var update in agent.RunStreamingAsync("Write another haiku about AI agents."))
{
    Console.WriteLine(update);
}
```

--------------------------------

TITLE: Disallowed Logger Initialization Using `__name__` (Python)
DESCRIPTION: Illustrates a logger initialization method that is explicitly disallowed within the `agent_framework` project. Using `logging.getLogger(__name__)` is discouraged as it bypasses the standardized `get_logger` function, potentially leading to inconsistent logging configurations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/design/python-package-setup.md

LANGUAGE: python
CODE:
```
import logging

logger = logging.getLogger(__name__)
```

--------------------------------

TITLE: Initialize Logger in Agent Framework (Python)
DESCRIPTION: Demonstrates the recommended way to obtain a logger instance using the `get_logger` function provided by the `agent_framework` package. It shows how to get a logger for the base package and for a specific subpackage, ensuring consistent logging practices across the project.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/design/python-package-setup.md

LANGUAGE: python
CODE:
```
from agent_framework import get_logger

logger = get_logger()
#or in a subpackage:
logger = get_logger('agent_framework.openai')
```

--------------------------------

TITLE: Azure AI Foundry Agent Service - File Search
DESCRIPTION: This endpoint allows for file searching within the Azure AI Foundry Agent Service. It supports specifying vector stores and their configurations for retrieval.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /agents/file_search

### Description
This endpoint performs a file search operation using specified vector stores and configurations.

### Method
POST

### Endpoint
/agents/file_search

### Parameters
#### Request Body
- **tools** (array) - Required - List of tools to use, must include `{"type": "file_search"}`.
- **tool_resources** (object) - Required - Resources for the tools.
  - **file_search** (object) - Required - Configuration for file search.
    - **vector_store_ids** (array) - Optional - IDs of vector stores to use.
    - **vector_stores** (array) - Optional - Details of vector stores.
      - **name** (string) - Required - Name of the vector store.
      - **configuration** (object) - Required - Configuration for the vector store.
        - **data_sources** (array) - Required - Data sources for the vector store.
          - **type** (object) - Required - Type of the data source.
            - **id_asset** (string) - Required - ID of the asset.
            - **uri_asset** (string) - Required - URI of the asset.
          - **uri** (string) - Required - URI of the data source.

### Request Example
```json
{
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "tool_resources": {
    "file_search": {
      "vector_store_ids": ["{string}"],
      "vector_stores": [
        {
          "name": "{string}",
          "configuration": {
            "data_sources": [
              {
                "type": {
                  "id_asset": "{string}",
                  "uri_asset": "{string}"
                },
                "uri": "{string}"
              }
            ]
          }
        }
      ]
    }
  }
}
```

### Response
#### Success Response (200)
- **tool_calls** (array) - List of tool calls made.
  - **id** (string) - Unique identifier for the tool call.
  - **type** (string) - Type of the tool, expected to be "file_search".
  - **file_search** (object) - Results from the file search.
    - **ranking_options** (object) - Options for ranking results.
      - **ranker** (string) - The ranking algorithm used.
      - **score_threshold** (float) - The minimum score for results to be included.
    - **results** (array) - List of search results.
      - **file_id** (string) - ID of the file.
      - **file_name** (string) - Name of the file.
      - **score** (float) - Relevance score of the result.
      - **content** (array) - Content snippets from the file.
        - **text** (string) - The text content.
        - **type** (string) - The type of content (e.g., "text/plain").

#### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "file_search",
      "file_search": {
        "ranking_options": {
          "ranker": "{string}",
          "score_threshold": "{float}"
        },
        "results": [
          {
            "file_id": "{string}",
            "file_name": "{string}",
            "score": "{float}",
            "content": [
              {
                "text": "{string}",
                "type": "{string}"
              }
            ]
          }
        ]
      }
    }
  ]
}
```
```

--------------------------------

TITLE: Original Python Class with Generics for Pydantic Conversion
DESCRIPTION: Shows a standard Python class `A` that incorporates generic types `T1` and `T2`, where `T2` is bound to a specific class. This example illustrates a complex scenario for conversion to a Pydantic serializable class, highlighting the use of `TypeVar`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from typing import TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2", bound=<some class>)

class A:
    def __init__(a: int, b: T1, c: T2):
        self.a = a
        self.b = b
        self.c = c
```

--------------------------------

TITLE: Load File as Raw Bytes for Multimodal Content (Python)
DESCRIPTION: This Python snippet shows how to open a file in binary read mode and load its content directly as raw bytes. These raw bytes can then be passed to `DataContent` along with the appropriate media type for multimodal input.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/multimodal_input/README.md

LANGUAGE: python
CODE:
```
# Load raw bytes
with open("path/to/your/image.jpg", "rb") as f:
    image_bytes = f.read()

# Use in DataContent
DataContent(
    data=image_bytes,
    media_type="image/jpeg"
)
```

--------------------------------

TITLE: Azure OpenAI - File Search
DESCRIPTION: This section details the API structure for performing file searches using Azure OpenAI's capabilities, including request parameters and response format for retrieval-augmented generation.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /openai/deployments/{AzureOpenAI}/chat/completions

### Description
This endpoint is used for chat completions with file search capabilities enabled via Azure OpenAI.

### Method
POST

### Endpoint
`/openai/deployments/{AzureOpenAI}/chat/completions`

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for chat completions.
- **messages** (array) - Required - An array of message objects representing the conversation history.
- **extra_headers** (object) - Optional - Extra headers to include in the request.
  - **"x-ms-user-api-version"** (string) - Required - The user API version.
- **tool_choice** (object) - Optional - Specifies how to use the tool.
  - **type** (string) - Required - The type of tool choice, e.g., "auto" or "required".
  - **function** (object) - Required if type is "required".
    - **name** (string) - Required - The name of the function to call, e.g., "search".
- **tools** (array) - Optional - A list of tools available to the model.
  - **type** (string) - Required - The type of tool, e.g., "file_search".
  - **file_search** (object) - Required if type is "file_search".
    - **vector_store_ids** (array) - Required - A list of vector store IDs to use for file search.
    - **kind** (string) - Optional - The kind of file search, e.g., "semantic".

### Request Example
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is the total amount of sales for the last quarter?"
    }
  ],
  "tool_choice": {
    "type": "auto"
  },
  "tools": [
    {
      "type": "file_search",
      "file_search": {
        "vector_store_ids": ["my-vector-store-id"]
      }
    }
  ]
}
```

### Response
#### Success Response (200)
- **id** (string) - The ID of the completion.
- **choices** (array) - An array of completion choices.
  - **message** (object) - The message content.
    - **content** (string) - The text content of the message.
    - **tool_calls** (array) - An array of tool calls made by the model.
      - **id** (string) - The ID of the tool call.
      - **type** (string) - The type of tool call, e.g., "function".
      - **function** (object) - Details of the function call.
        - **name** (string) - The name of the function called.
        - **arguments** (string) - JSON string of arguments for the function call.
- **usage** (object) - Usage statistics for the completion.
  - **completion_tokens** (integer) - Number of completion tokens used.
  - **prompt_tokens** (integer) - Number of prompt tokens used.
  - **total_tokens** (integer) - Total number of tokens used.

#### Response Example
```json
{
  "id": "chatcmpl-12345",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The total amount of sales for the last quarter was $1.2 million."
      }
    }
  ],
  "usage": {
    "completion_tokens": 15,
    "prompt_tokens": 50,
    "total_tokens": 65
  }
}
```
```

--------------------------------

TITLE: OpenAI Assistants Agent with Existing Assistant ID
DESCRIPTION: Shows how to utilize a pre-existing OpenAI assistant by providing its ID to the `OpenAIAssistantsClient`. This example includes proper cleanup procedures for manually created assistants.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent

# Replace with your existing assistant ID
existing_assistant_id = "asst_YOUR_EXISTING_ASSISTANT_ID"

client = OpenAIAssistantsClient(assistant_id=existing_assistant_id)
agent = ChatAgent(client=client)

response = agent.chat("How can you help me today?")
print(f"Response from existing assistant: {response}")

# If you manually created the assistant and want to clean it up later:
# agent.cleanup_assistant()

```

--------------------------------

TITLE: Run Aspire Dashboard Container with Docker
DESCRIPTION: This bash command demonstrates how to pull and run the Aspire Dashboard container locally using Docker. It exposes the web UI and OTLP endpoint on specified ports, making it accessible for local telemetry viewing.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: bash
CODE:
```
# Pull and run the Aspire Dashboard container
docker run --rm -it -d \
    -p 18888:18888 \
    -p 4317:18889 \
    --name aspire-dashboard \
    mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

--------------------------------

TITLE: Implement Standard Logger Retrieval Function (Python)
DESCRIPTION: Provides the implementation details for the `get_logger` function, intended to be located in `_logging.py`. This function acts as a centralized point for logger creation, ensuring all loggers are named consistently and can be configured with specific levels and handlers.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/design/python-package-setup.md

LANGUAGE: python
CODE:
```
# in file _logging.py
import logging

def get_logger(name: str = "agent_framework") -> logging.Logger:
    """
    Get a logger with the specified name, defaulting to 'agent_framework'.

    Args:
        name (str): The name of the logger. Defaults to 'agent_framework'.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    # create the specifics for the logger, such as setting the level, handlers, etc.
    return logger
```

--------------------------------

TITLE: Setup Observability with Custom OTLP Exporter
DESCRIPTION: This example shows how to configure and add a custom OpenTelemetry Protocol (OTLP) exporter to the observability setup. It specifies an endpoint and compression method for sending trace data.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
from grpc import Compression
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from agent_framework.observability import setup_observability

exporter = OTLPSpanExporter(endpoint="your-otlp-endpoint", compression=Compression.Gzip)
setup_observability(exporters=[exporter])
```

--------------------------------

TITLE: Set Azure AI Foundry Environment Variable (PowerShell)
DESCRIPTION: Provides an example of how to set the AZURE_FOUNDRY_PROJECT_ENDPOINT environment variable using PowerShell. This variable is necessary for connecting to Azure AI Foundry services and is typically used when running samples or applications that integrate with this platform.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_FOUNDRY_PROJECT_ENDPOINT = "https://<your-project>-resource.services.ai.azure.com/api/projects/<your-project>"
```

--------------------------------

TITLE: Azure AI Foundry File Search Tool Call Response
DESCRIPTION: Represents the JSON response structure for a file search tool call in Azure AI Foundry Agent Service. It includes details about ranked search results, such as file ID, name, score, and content.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "file_search",
      "file_search": {
        "ranking_options": {
          "ranker": "{string}",
          "score_threshold": "{float}"
        },
        "results": [
          {
            "file_id": "{string}",
            "file_name": "{string}",
            "score": "{float}",
            "content": [
              {
                "text": "{string}",
                "type": "{string}"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: Azure AI Foundry OpenAPI Tool Call Response
DESCRIPTION: Represents the tool call response structure for an OpenAPI tool within the Azure AI Foundry Agent Service. This is used by the agent to identify and process results from an OpenAPI tool invocation.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "openapi",
      "openapi": {}
    }
  ]
}
```

--------------------------------

TITLE: Discouraged Direct Logger Initialization (Python)
DESCRIPTION: Shows a discouraged method for initializing a logger by directly naming it 'agent_framework'. While it might return a correctly configured logger if `get_logger` has been called, it bypasses the intended standard mechanism, risking inconsistencies in logging formats and handlers.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/design/python-package-setup.md

LANGUAGE: python
CODE:
```
import logging

logger = logging.getLogger("agent_framework")
```

--------------------------------

TITLE: Configure Observability with Custom Exporter
DESCRIPTION: Demonstrates how to set up observability by passing a custom OTLPSpanExporter to the `setup_observability()` function. This method bypasses the need for the `ENABLE_OTEL` environment variable and allows control over sensitive data inclusion via `ENABLE_SENSITIVE_DATA` or the `enable_sensitive_data` parameter.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from agent_framework.observability import setup_observability

exporter = OTLPSpanExporter(endpoint="another-otlp-endpoint")
setup_observability(exporters=[exporter])
```

--------------------------------

TITLE: Python Example: Train a Math Agent with Agent Framework Lab
DESCRIPTION: Demonstrates training a math agent using Agent Framework Lab and Agent-lightning. It includes agent definition with a calculator tool, training configuration, initialization of agent-framework for telemetry, and running the trainer.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: python
CODE:
```
from agent_framework.lab.lightning import init
from agentlightning import rollout, Trainer, LLM, Dataset
from agentlightning.algorithm.verl import VERL
from typing import Any
from agentlightning.tools.mcp import MCPStdioTool
from agentlightning.agents.chat import ChatAgent
from agentlightning.clients.openai import OpenAIChatClient

TaskType = Any

@rollout
async def math_agent(task: TaskType, llm: LLM) -> float:
    """A function that solves a math problem and returns the evaluation score."""
    async with (
        MCPStdioTool(name="calculator", command="uvx", args=["mcp-server-calculator"]) as mcp_server,
        ChatAgent(
            chat_client=OpenAIChatClient(
                model_id=llm.model,
                api_key="your-api-key",
                base_url=llm.endpoint,
            ),
            name="MathAgent",
            instructions="Solve the math problem and output answer after ###",
            temperature=llm.sampling_parameters.get("temperature", 0.0),
        ) as agent,
    ):
        result = await agent.run(task["question"], tools=mcp_server)
        # Your evaluation logic here...
        return evaluation_score

# Training configuration
config = {
    "data": {"train_batch_size": 8},
    "trainer": {"total_epochs": 2, "n_gpus_per_node": 1},
    # ... additional config
}

# Initialize agent-framework to send telemetry data to agent-lightning's observability backend
init()

trainer = Trainer(algorithm=VERL(config), n_workers=2)
# Both train_dataset and val_dataset are lists of TaskType
trainer.fit(math_agent, train_dataset, val_data=val_dataset)
```

--------------------------------

TITLE: Use Agent Framework Centralized Logger in Python
DESCRIPTION: Demonstrates the preferred method for obtaining a logger instance in the `agent_framework` project. It shows how to get a package-level logger and a subpackage-specific logger using `get_logger()` for centralized logging.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework import get_logger

# For main package
logger = get_logger()

# For subpackages
logger = get_logger('agent_framework.azure')
```

--------------------------------

TITLE: Integrate OpenAI Agents with Local MCP Servers (Python)
DESCRIPTION: Demonstrates integrating OpenAI agents with a locally running Model Context Protocol (MCP) server. This enables enhanced functionalities and seamless tool integration within a local environment. Requires OpenAI API key and model IDs, and a running local MCP server.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from openai_responses_client import OpenAIResponsesClient
from agent_framework.tools import FunctionTool

# Assume 'local_mcp_client' is initialized with connection details to the local MCP server
# e.g., local_mcp_client = LocalMCPClient(port=8000)

# Initialize the OpenAIResponsesClient
client = OpenAIResponsesClient(
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_chat_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID"),
    openai_responses_model_id=os.environ.get("OPENAI_RESPONSES_MODEL_ID"),
    local_mcp_client=local_mcp_client # Pass the initialized local MCP client
)

# Define a tool that interacts with the local MCP server
def process_local_request(request_id: str) -> str:
    # This function would internally call the local_mcp_client to process the request
    print(f"Processing local request: {request_id}")
    return f"Processed request {request_id} locally."

# Create an agent that uses tools connected to the local MCP server
agent = client.create_agent(tools=[FunctionTool.from_function(process_local_request)])

# Query the agent to use the local tool
response = agent.query("Process the request with ID abc-789.")
print(response.output)
```

--------------------------------

TITLE: Azure AI Foundry Bing Search Message Request
DESCRIPTION: Defines the JSON structure for making a Bing search request within the Azure AI Foundry Agent Service. It specifies search configurations like connection ID, count, market, language, and freshness.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "bing_grounding",
      "bing_grounding": {
        "search_configurations": [
          {
            "connection_id": "{string}",
            "count": "{number}", 
            "market": "{string}", 
            "set_lang": "{string}", 
            "freshness": "{string}"
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: OpenAI Assistants Agent with Thread Management
DESCRIPTION: Demonstrates thread management for OpenAI agents. It covers automatic thread creation for stateless conversations and explicit thread management for maintaining conversation context across multiple interactions.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent

# Example 1: Stateless conversation (automatic thread creation)
client_stateless = OpenAIAssistantsClient()
agent_stateless = ChatAgent(client=client_stateless)

response1 = agent_stateless.chat("What is the capital of France?")
print(f"Stateless response 1: {response1}")
response2 = agent_stateless.chat("And what is its population?") # New thread created automatically
print(f"Stateless response 2: {response2}")

# Example 2: Stateful conversation (explicit thread management)
client_stateful = OpenAIAssistantsClient()
agent_stateful = ChatAgent(client=client_stateful)

# Create a thread explicitly
thread_id = agent_stateful.create_thread()
print(f"Created thread with ID: {thread_id}")

# Interact within the explicit thread
response3 = agent_stateful.chat("Tell me about the Eiffel Tower.", thread_id=thread_id)
print(f"Stateful response 1: {response3}")

response4 = agent_stateful.chat("How tall is it?", thread_id=thread_id)
print(f"Stateful response 2: {response4}")

# Clean up the explicit thread if needed
# agent_stateful.delete_thread(thread_id)

```

--------------------------------

TITLE: Complete Google-Style Docstring Example in Python
DESCRIPTION: This example shows a comprehensive Google-style docstring, including a multi-line explanation, `Args`, `Returns`, and `Raises` sections. It details how to format each section with proper indentation for arguments and their descriptions.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same.

    Here is extra explanation of the logic involved.

    Args:
        arg1: The first string to compare.
        arg2: The second string to compare.

    Returns:
        True if the strings are the same, False otherwise.
    """
```

--------------------------------

TITLE: Import Core Agent Framework Components in Python
DESCRIPTION: Shows how to import core components like `ChatAgent` and `ai_function` directly from the top-level `agent_framework` package. This reflects the project's flat import structure for core functionalities.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework import ChatAgent, ai_function
```

--------------------------------

TITLE: Create and Run a Basic .NET Agent
DESCRIPTION: This snippet demonstrates how to create a basic AI agent using the Microsoft Agent Framework with Azure OpenAI. It requires setting environment variables for the Azure OpenAI endpoint and deployment name. The agent is initialized with a name and instructions, and then used to generate a response to a prompt.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/README.md

LANGUAGE: csharp
CODE:
```
using System;
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;

var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!;
var deploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME")!;

var agent = new AzureOpenAIClient(new Uri(endpoint), new AzureCliCredential())
    .GetOpenAIResponseClient(deploymentName)
    .CreateAIAgent(name: "HaikuBot", instructions: "You are an upbeat assistant that writes beautifully.");

Console.WriteLine(await agent.RunAsync("Write a haiku about Microsoft Agent Framework."));
```

--------------------------------

TITLE: Azure AI Foundry Bing Search Tool Call Response
DESCRIPTION: Illustrates the JSON structure for the tool call response from Bing Search within Azure AI Foundry. It includes a placeholder for future use, indicating a reserved field for 'bing_grounding'.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "function",
      "bing_grounding": {} // From documentation: Reserved for future use
    }
  ]
}
```

--------------------------------

TITLE: Import Agent Framework Specific Components in Python
DESCRIPTION: Demonstrates importing specific components from submodules within the `agent_framework` package, such as `VectorStoreModel` from `agent_framework.vector_data` and `ContentFilter` from `agent_framework.guardrails`. This structure is used for modular functionalities.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework.vector_data import VectorStoreModel
from agent_framework.guardrails import ContentFilter
```

--------------------------------

TITLE: Configure Detailed Logging
DESCRIPTION: Shows how to configure detailed logging by setting the root logger's level to `logging.NOTSET`. This ensures that all log messages, regardless of their severity, are exported as telemetry. Other loggers will inherit this setting.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: python
CODE:
```
import logging

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
```

--------------------------------

TITLE: Basic OpenAI Assistants Agent with ChatAgent
DESCRIPTION: Demonstrates the simplest way to create an agent using `ChatAgent` with `OpenAIAssistantsClient`. It covers both streaming and non-streaming responses, along with automatic assistant creation and cleanup.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent

# Example for basic usage (assuming you have API key configured)
client = OpenAIAssistantsClient()
agent = ChatAgent(client=client)

# Non-streaming response
response = agent.chat("Hello, who are you?")
print(f"Non-streaming response: {response}")

# Streaming response
print("Streaming response:")
for chunk in agent.chat_stream("Tell me a joke."):
    print(chunk, end="", flush=True)
print()

# Cleanup (if assistant was auto-created)
# agent.cleanup_assistant()

```

--------------------------------

TITLE: Integrate OpenAI Agents with Hosted MCP Servers (Python)
DESCRIPTION: Shows how to connect OpenAI agents with remote Model Context Protocol (MCP) servers. This example includes handling approval workflows and managing tools for these remote services. Requires OpenAI API key and model IDs, and MCP server details.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from openai_responses_client import OpenAIResponsesClient
from agent_framework.tools import FunctionTool

# Assume 'hosted_mcp_client' is initialized with connection details to the hosted MCP server
# e.g., hosted_mcp_client = HostedMCPClient(base_url='http://your-mcp-server.com', api_key='YOUR_MCP_API_KEY')

# Initialize the OpenAIResponsesClient
client = OpenAIResponsesClient(
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_chat_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID"),
    openai_responses_model_id=os.environ.get("OPENAI_RESPONSES_MODEL_ID"),
    hosted_mcp_client=hosted_mcp_client # Pass the initialized hosted MCP client
)

# Define a tool that might interact with the hosted MCP server
def get_remote_service_data(param: str) -> str:
    # This function would internally call the hosted_mcp_client to get data
    # For demonstration, we'll mock it.
    print(f"Querying remote service with: {param}")
    return f"Data for {param} from remote MCP"

# Create an agent that can use tools potentially interacting with the MCP server
agent = client.create_agent(tools=[FunctionTool.from_function(get_remote_service_data)])

# Query the agent
response = agent.query("Get data for user_123 from the remote service.")
print(response.output)
```

--------------------------------

TITLE: Basic OpenAI Responses Agent with ChatAgent
DESCRIPTION: Demonstrates the simplest way to create an agent using `ChatAgent` with `OpenAIResponsesClient`. It covers both streaming and non-streaming responses for structured response generation with OpenAI models.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.responses import OpenAIResponsesClient
from agent_framework.agents.chat_agent import ChatAgent

# Example for basic usage (assuming you have API key configured)
client = OpenAIResponsesClient()
agent = ChatAgent(client=client)

# Non-streaming response
response = agent.chat("Generate a structured response about the solar system.")
print(f"Non-streaming response: {response}")

# Streaming response
print("Streaming response:")
for chunk in agent.chat_stream("Describe the process of photosynthesis."):
    print(chunk, end="", flush=True)
print()

```

--------------------------------

TITLE: Set Azure OpenAI Deployment Name (Console)
DESCRIPTION: This command sets the Azure OpenAI deployment name as an environment variable. This specifies which model deployment to use. It's optional as a default is provided, but recommended for clarity.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/ModelContextProtocol/README.md

LANGUAGE: powershell
CODE:
```
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini
```

--------------------------------

TITLE: Correct Function Parameter Definition in Python
DESCRIPTION: This example demonstrates the preferred way to define function parameters by providing string-based overrides for enums like `ChatToolMode`. This approach avoids requiring the user to import additional modules and handles the conversion internally.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
def create_agent(name: str, tool_mode: Literal['auto', 'required', 'none'] | ChatToolMode) -> Agent:
    # Implementation here
    if isinstance(tool_mode, str):
        tool_mode = ChatToolMode(tool_mode)
```

--------------------------------

TITLE: OpenAI Chat Agent with Thread Management
DESCRIPTION: Demonstrates thread management for OpenAI chat agents. It covers automatic thread creation for stateless conversations and explicit thread management for maintaining conversation context across multiple interactions.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.chat import OpenAIChatClient
from agent_framework.agents.chat_agent import ChatAgent

# Example 1: Stateless conversation (automatic thread creation)
client_stateless = OpenAIChatClient()
agent_stateless = ChatAgent(client=client_stateless)

response1 = agent_stateless.chat("What is the capital of Spain?")
print(f"Stateless response 1: {response1}")
response2 = agent_stateless.chat("And what is its main river?") # New thread created automatically
print(f"Stateless response 2: {response2}")

# Example 2: Stateful conversation (explicit thread management)
client_stateful = OpenAIChatClient()
agent_stateful = ChatAgent(client=client_stateful)

# Create a thread explicitly
thread_id = agent_stateful.create_thread()
print(f"Created thread with ID: {thread_id}")

# Interact within the explicit thread
response3 = agent_stateful.chat("Tell me about the Sagrada Familia.", thread_id=thread_id)
print(f"Stateful response 1: {response3}")

response4 = agent_stateful.chat("When was it started?", thread_id=thread_id)
print(f"Stateful response 2: {response4}")

# Clean up the explicit thread if needed
# agent_stateful.delete_thread(thread_id)

```

--------------------------------

TITLE: Python: Google ADK Agent with MCP Toolset
DESCRIPTION: Shows how to initialize an agent using Google's ADK (Agent Development Kit) with a remote MCP Toolset. It demonstrates configuring connection parameters and optionally filtering tools.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: python
CODE:
```
async def get_agent_async():
  toolset = MCPToolset(
      tool_filter=['read_file', 'list_directory'] # Optional: filter specific tools
      connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )

  # Use in an agent
  root_agent = LlmAgent(
      model='model', # Adjust model name if needed based on availability
      name='agent_name',
      instruction='agent_instructions',
      tools=[toolset], # Provide the MCP tools to the ADK agent
  )
  return root_agent, toolset
```

--------------------------------

TITLE: Run Basic Chat Completion Sample (Python)
DESCRIPTION: Executes a basic chat completion scenario using both Semantic Kernel and Microsoft Agent Framework implementations. This script demonstrates the initial call to the SK implementation followed by the AF version, allowing for direct output comparison.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/semantic-kernel-migration/README.md

LANGUAGE: Python
CODE:
```
python samantic-kernel-migration/chat_completion/01_basic_chat_completion.py
```

--------------------------------

TITLE: Use Web Search Capabilities with OpenAI Agents (Python)
DESCRIPTION: Demonstrates how OpenAI agents can utilize web search to find and incorporate information from the internet into their responses. This enhances the agent's ability to provide up-to-date and relevant information. Requires OpenAI API key and model IDs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from openai_responses_client import OpenAIResponsesClient
from agent_framework.tools import WebSearchTool
import os

# Ensure the SEARCH_API_KEY environment variable is set if using a specific search provider
# os.environ["SEARCH_API_KEY"] = "YOUR_SEARCH_API_KEY"

# Initialize the OpenAIResponsesClient
client = OpenAIResponsesClient(
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_chat_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID"),
    openai_responses_model_id=os.environ.get("OPENAI_RESPONSES_MODEL_ID"),
)

# Create an agent with the WebSearchTool enabled
agent = client.create_agent(
    tools=[WebSearchTool()]
)

# Query the agent, asking a question that requires current information from the web
response = agent.query("What are the latest headlines about climate change?")
print(response.output)

# Example with a more specific search query
response_specific = agent.query("Find the current stock price of AAPL.")
print(response_specific.output)
```

--------------------------------

TITLE: Minimal Google-Style Docstring for Python Functions
DESCRIPTION: This snippet illustrates the most basic form of a Google-style docstring. It provides a single-line summary of the function's purpose, ending with a period, as per the documentation guidelines.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same."""
    ...
```

--------------------------------

TITLE: OpenAI Assistants Agent with Function Tools
DESCRIPTION: Demonstrates integrating function tools with OpenAI agents. It covers defining tools at both the agent level (during creation) and the query level (provided with specific queries).

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.base.tool import Tool

# Define a sample function tool
def get_current_weather(location: str, unit: str = "celsius") -> str:
    return f"It's sunny in {location} ({unit})Sea-level pressure: 1012 hPa"

# Define tool specifications for OpenAI
weather_tool = Tool(
    name="get_weather",
    func=get_current_weather,
    description="Get the current weather in a given location.",
    parameters=[
        {"name": "location", "type": "string", "description": "The city and state, e.g. San Francisco, CA"},
        {"name": "unit", "type": "string", "description": "The unit of temperature, 'celsius' or 'fahrenheit'.", "optional": True}
    ]
)

# Agent-level tools
client_agent_tools = OpenAIAssistantsClient(tools=[weather_tool])
agent_with_agent_tools = ChatAgent(client=client_agent_tools)

response_agent_tools = agent_with_agent_tools.chat("What's the weather like in Boston?")
print(f"Response with agent-level tools: {response_agent_tools}")

# Query-level tools
client_query_tools = OpenAIAssistantsClient()
agent_with_query_tools = ChatAgent(client=client_query_tools)

response_query_tools = agent_with_query_tools.chat("What's the weather in London?", tools=[weather_tool])
print(f"Response with query-level tools: {response_query_tools}")

```

--------------------------------

TITLE: Azure OpenAI Tool Call and Response for Knowledge Base Lookup
DESCRIPTION: This snippet demonstrates the structure of a tool call request to Azure OpenAI for a knowledge base lookup, including parameters like 'searchType' and 'vectorSearchConfiguration'. It also shows the corresponding response structure, detailing 'retrievedReferences' with content and metadata.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "toolCall": {
    "toolName": "knowledgeBase",
    "toolInput": {
      "vectorSearchConfiguration": {
        "vectorSearchType": "HYBRID",
        "vectorConfiguration": {
          "vectorConfigurationType": "VECTOR",
          "fields": [
            {
              "vectorStoreId": "{string}",
              "fields": [
                "{string}"
              ]
            }
          ]
        },
        "numberRecall": {
          "kind": "TOP_K",
          "value": "{number}"
        }
      },
      "searchType": "VECTOR",
      "numberOfResults": "{number}",
      "overrideSearchType": "{string}",
      "rerankingConfiguration": {
        "bedrockRerankingConfiguration": {
          "metadataConfiguration": {
            "selectionMode": "{string}",
            "selectiveModeConfiguration": {}
          },
          "modelConfiguration": {
            "additionalModelRequestFields": {
              "string": "{JSON string}"
            },
            "modelArn": "{string}"
          },
          "numberOfRerankedResults": "{number}"
        },
        "type": "{string}"
      }
    }
  }
}

```

LANGUAGE: json
CODE:
```
{
  "trace": {
    "orchestrationTrace": {
      "invocationInput": {
        "invocationType": "KNOWLEDGE_BASE",
        "knowledgeBaseLookupInput": {
          "knowledgeBaseId": "{string}",
          "text": "{string}"
        }
      },
      "observation": {
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseLookupOutput": {
          "retrievedReferences": [
            {
              "metadata": {},
              "content": {
                "byteContent": "{string}",
                "row": [
                  {
                    "columnName": "{string}",
                    "columnValue": "{string}",
                    "type": "{BLOB | BOOLEAN | DOUBLE | NULL | LONG | STRING}"
                  }
                ],
                "text": "{string}",
                "type": "{TEXT | IMAGE | ROW}"
              }
            }
          ],
          "metadata": {
            "clientRequestId": "{string}",
            "endTime": "{timestamp}",
            "operationTotalTimeMs": "{long}",
            "startTime": "{timestamp}",
            "totalTimeMs": "{long}",
            "usage": {
              "inputTokens": "{integer}",
              "outputTokens": "{integer}"
            }
          }
        }
      }
    }
  }
}

```

--------------------------------

TITLE: OpenAI Chat Agent with Function Tools
DESCRIPTION: Demonstrates integrating function tools with OpenAI chat agents. It covers defining tools at both the agent level (during creation) and the query level (provided with specific queries).

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.chat import OpenAIChatClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.base.tool import Tool

# Define a sample function tool
def add_numbers(a: int, b: int) -> int:
    return a + b

# Define tool specifications for OpenAI
add_tool = Tool(
    name="add",
    func=add_numbers,
    description="Adds two integers together.",
    parameters=[
        {"name": "a", "type": "integer", "description": "The first integer."},
        {"name": "b", "type": "integer", "description": "The second integer."}
    ]
)

# Agent-level tools
client_agent_tools = OpenAIChatClient(tools=[add_tool])
agent_with_agent_tools = ChatAgent(client=client_agent_tools)

response_agent_tools = agent_with_agent_tools.chat("What is 5 + 3?")
print(f"Response with agent-level tools: {response_agent_tools}")

# Query-level tools
client_query_tools = OpenAIChatClient()
agent_with_query_tools = ChatAgent(client=client_query_tools)

response_query_tools = agent_with_query_tools.chat("Calculate 10 + 7.", tools=[add_tool])
print(f"Response with query-level tools: {response_query_tools}")

```

--------------------------------

TITLE: OpenAI Responses Agent with Explicit Settings
DESCRIPTION: Illustrates initializing an agent with a specific OpenAI Responses client, explicitly configuring settings such as the API key and model ID. This allows for precise control over client initialization.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.responses import OpenAIResponsesClient
from agent_framework.agents.chat_agent import ChatAgent

# Replace with your actual API key and desired model ID
api_key = "sk-YOUR_API_KEY"
model_id = "gpt-4-turbo"

client = OpenAIResponsesClient(api_key=api_key, model_id=model_id)
agent = ChatAgent(client=client)

response = agent.chat("Summarize the key points of quantum entanglement.")
print(f"Response with explicit settings: {response}")

```

--------------------------------

TITLE: OpenAI Responses Agent with File Search
DESCRIPTION: Demonstrates using file search capabilities with OpenAI agents. This enables the agent to search through uploaded files to provide answers based on the provided documentation.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.responses import OpenAIResponsesClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.file_search.file_search import FileSearchTool

# Assuming you have files uploaded to your OpenAI assistant or configured for file search

client = OpenAIResponsesClient(enable_file_search=True) # Or configure FileSearchTool explicitly
agent = ChatAgent(client=client)

# Example query that might involve searching through files
response = agent.chat("Based on the uploaded project proposal, what are the estimated timelines?")
print(f"Response using file search: {response}")

# To explicitly use FileSearchTool if not implicitly enabled:
# file_search_tool = FileSearchTool()
# client = OpenAIResponsesClient(tools=[file_search_tool])
# agent = ChatAgent(client=client)
# response = agent.chat("Find information about 'budget allocation' in the provided reports.")
# print(f"Response using explicit file search tool: {response}")

```

--------------------------------

TITLE: Basic OpenAI Chat Agent with ChatAgent
DESCRIPTION: Shows the simplest way to create an agent using `ChatAgent` with `OpenAIChatClient`. It demonstrates both streaming and non-streaming responses for chat-based interactions with OpenAI models.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.chat import OpenAIChatClient
from agent_framework.agents.chat_agent import ChatAgent

# Example for basic usage (assuming you have API key configured)
client = OpenAIChatClient()
agent = ChatAgent(client=client)

# Non-streaming response
response = agent.chat("Hello, how can you help me?")
print(f"Non-streaming response: {response}")

# Streaming response
print("Streaming response:")
for chunk in agent.chat_stream("Tell me a short story."):
    print(chunk, end="", flush=True)
print()

```

--------------------------------

TITLE: Lazy Loading and Error Handling for Subpackages
DESCRIPTION: Illustrates the concept of lazy loading within vendor namespaces. When a subpackage or its dependencies are not installed, a clear error message should be raised to guide the user on which extra to install.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: python
CODE:
```
# Example of lazy loading and error raising (conceptual)

try:
    from agent_framework.azure.purview import PurviewMiddleware
except ImportError:
    raise ImportError("The 'azure-purview' extra is not installed. Install with: pip install agent-framework[azure-purview]")
```

--------------------------------

TITLE: OpenAI Assistants Agent with File Search
DESCRIPTION: Demonstrates using file search capabilities with OpenAI agents. This allows the agent to search through uploaded files to answer user questions.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.file_search.file_search import FileSearchTool

# Assuming you have files uploaded to your OpenAI assistant or configured for file search
# This example assumes the FileSearchTool is implicitly enabled or configured with the client

client = OpenAIAssistantsClient(enable_file_search=True) # Or configure FileSearchTool explicitly
agent = ChatAgent(client=client)

# Example query that might require file search
response = agent.chat("Based on the provided documents, what are the key findings?")
print(f"Response using file search: {response}")

# To explicitly use FileSearchTool if not implicitly enabled:
# file_search_tool = FileSearchTool()
# client = OpenAIAssistantsClient(tools=[file_search_tool])
# agent = ChatAgent(client=client)
# response = agent.chat("Search for 'project roadmap' in the documents.")
# print(f"Response using explicit file search tool: {response}")

```

--------------------------------

TITLE: Install Agent Framework Lab from Source
DESCRIPTION: This command sequence clones the agent-framework repository, navigates to the lab package directory, and installs it in editable mode using pip. This method is suitable for development or when the latest unreleased features are needed.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/README.md

LANGUAGE: bash
CODE:
```
git clone https://github.com/microsoft/agent-framework.git
cd agent-framework/python/packages/lab
pip install -e .
```

--------------------------------

TITLE: Incorrect Function Parameter Definition in Python
DESCRIPTION: This example illustrates an incorrect way to define function parameters, specifically for `tool_mode`, as it requires the user to import an additional `ChatToolMode` module. The guideline suggests avoiding additional imports for basic function usage.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
def create_agent(name: str, tool_mode: ChatToolMode) -> Agent:
    # Implementation here
```

--------------------------------

TITLE: Creating Chat Messages with Attributes in Python
DESCRIPTION: This snippet demonstrates the preferred method of configuring objects using attributes, specifically for `ChatMessage` instances. It highlights avoiding inheritance when parameters are mostly similar by directly instantiating with specific attributes.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework import ChatMessage

user_msg = ChatMessage(role="user", content="Hello, world!")
asst_msg = ChatMessage(role="assistant", content="Hello, world!")
```

--------------------------------

TITLE: Manually Run Console Application with Telemetry
DESCRIPTION: Navigate to the console application's directory, set the OpenTelemetry exporter endpoint to direct telemetry to the locally running Aspire Dashboard, and then execute the .NET application. This enables real-time telemetry visualization.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentOpenTelemetry/README.md

LANGUAGE: powershell
CODE:
```
cd dotnet/demos/AgentOpenTelemetry
$env:OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
dotnet run
```

--------------------------------

TITLE: Haystack Pipeline with Custom Message Collector
DESCRIPTION: This Python code defines a custom `MessageCollector` component for Haystack's pipeline architecture. This component intercepts and stores `ChatMessage` objects flowing through the pipeline, useful for observation or debugging. It's integrated into a pipeline that also includes a conditional router and tool invoker.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
from haystack import Pipeline
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.routers import ConditionalRouter
from haystack.components.tools import ToolInvoker
from haystack.tools import ComponentTool
from haystack.components.websearch import SerperDevWebSearch
from haystack.dataclasses import ChatMessage
from typing import Any, Dict, List
from haystack import component
from haystack.core.component.types import Variadic

# Custom component to collect/observe messages (for interception/observation)
@component()
class MessageCollector:
    def __init__(self):
        self._messages = []
    @component.output_types(messages=List[ChatMessage])
    def run(self, messages: Variadic[List[ChatMessage]]) -> Dict[str, Any]:
        self._messages.extend([msg for inner in messages for msg in inner])
        return {"messages": self._messages}
    def clear(self):
        self._messages = []

# Define a tool
web_tool = ComponentTool(component=SerperDevWebSearch(top_k=3))

# Define routes for filtering (e.g., check for tool calls)
routes = [
    {
        "condition": "{{replies[0].tool_calls | length > 0}}",
        "output": "{{replies}}",
        "output_name": "there_are_tool_calls",
        "output_type": List[ChatMessage],
    },
    {
        "condition": "{{replies[0].tool_calls | length == 0}}",
        "output": "{{replies}}",
        "output_name": "final_replies",
        "output_type": List[ChatMessage],
    },
]

# Build the pipeline
pipeline = Pipeline()
pipeline.add_component("generator", OpenAIChatGenerator(model="gpt-4o-mini"))
pipeline.add_component("router", ConditionalRouter(routes=routes))
pipeline.add_component("tool_invoker", ToolInvoker(tools=[web_tool]))
pipeline.add_component("message_collector", MessageCollector())

```

--------------------------------

TITLE: Create, Retrieve, and Run Agent with Foundry SDK and Agent Framework (C#)
DESCRIPTION: This snippet demonstrates how to create a persistent agent using the Foundry SDK, retrieve it as an AIAgent, run it using the Agent Framework SDK, and then clean up the agent. It requires Azure AI endpoint and credentials.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/specs/001-foundry-sdk-alignment.md

LANGUAGE: csharp
CODE:
```
// Get a client to create server side agents with.
var persistentAgentsClient = new PersistentAgentsClient(
    TestConfiguration.AzureAI.Endpoint, new AzureCliCredential());

// Create a persistent agent.
var persistentAgentMetadata = await persistentAgentsClient.Administration.CreateAgentAsync(
    model: TestConfiguration.AzureAI.DeploymentName!,
    name: JokerName,
    instructions: JokerInstructions);

// Get the persistent agent we created in the previous step and expose it as an Agent Framework agent.
AIAgent agent = await persistentAgentsClient.GetAIAgentAsync(persistentAgent.Value.Id);

// Respond to user input.
var input = "Tell me a joke about a pirate.";
Console.WriteLine(input);
Console.WriteLine(await agent.RunAsync(input));

// Delete the persistent agent.
await persistentAgentsClient.Administration.DeleteAgentAsync(agent.Id);
```

--------------------------------

TITLE: OpenAI Assistants Agent with Explicit Settings
DESCRIPTION: Illustrates initializing an agent with a specific OpenAI Assistants client, explicitly configuring settings such as the API key and model ID. This provides more control over the client's configuration.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.assistants import OpenAIAssistantsClient
from agent_framework.agents.chat_agent import ChatAgent

# Replace with your actual API key and desired model ID
api_key = "sk-YOUR_API_KEY"
model_id = "gpt-4o"

client = OpenAIAssistantsClient(api_key=api_key, model_id=model_id)
agent = ChatAgent(client=client)

response = agent.chat("Can you explain the concept of recursion?")
print(f"Response with explicit settings: {response}")

```

--------------------------------

TITLE: OpenAI Responses Agent with Image Analysis
DESCRIPTION: Demonstrates using vision capabilities with agents to analyze images. This allows the agent to interpret and respond based on image content.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.responses import OpenAIResponsesClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.vision.vision_tool import VisionTool

# Example: Assuming you have an image URL or path
image_source = "https://example.com/path/to/your/image.jpg"

# Initialize the vision tool and the client
vision_tool = VisionTool()
client = OpenAIResponsesClient(tools=[vision_tool])
agent = ChatAgent(client=client)

# Ask the agent to analyze the image
response = agent.chat(f"Analyze the content of this image: {image_source}")
print(f"Image analysis response: {response}")

```

--------------------------------

TITLE: Run Demo with PowerShell Quick Start Script
DESCRIPTION: Execute this PowerShell script to automatically set up and run the entire demo. It handles prerequisite checks, application building, Aspire Dashboard startup via Docker, and launches the interactive console application.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentOpenTelemetry/README.md

LANGUAGE: powershell
CODE:
```
.\start-demo.ps1
```

--------------------------------

TITLE: Integrate Custom Conversation Workflows in Python
DESCRIPTION: This code shows how to build and integrate custom conversation workflows using WorkflowBuilder and AgentExecutor. It defines the flow of interaction between agents, including setting start points and defining transitions with conditions. Dependencies include agent_framework.WorkflowBuilder, agent_framework.AgentExecutor, and agent_framework.lab.tau2.TaskRunner.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/tau2/README.md

LANGUAGE: python
CODE:
```
from agent_framework import WorkflowBuilder, AgentExecutor
from agent_framework.lab.tau2 import TaskRunner

class WorkflowTaskRunner(TaskRunner):
    def build_conversation_workflow(self, assistant_agent, user_simulator_agent):
        # Build a custom workflow
        builder = WorkflowBuilder()

        # Create agent executors
        assistant_executor = AgentExecutor(assistant_agent, id="assistant_agent")
        user_executor = AgentExecutor(user_simulator_agent, id="user_simulator")

        # Add workflow edges and conditions
        builder.set_start_executor(assistant_executor)
        builder.add_edge(assistant_executor, user_executor)
        builder.add_edge(user_executor, assistant_executor, condition=self.should_not_stop)

        return builder.build()
```

--------------------------------

TITLE: OpenAI Chat Agent with Explicit Settings
DESCRIPTION: Illustrates initializing an agent with a specific OpenAI Chat client, explicitly configuring settings such as the API key and model ID. This provides fine-grained control over the client's parameters.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.chat import OpenAIChatClient
from agent_framework.agents.chat_agent import ChatAgent

# Replace with your actual API key and desired model ID
api_key = "sk-YOUR_API_KEY"
model_id = "gpt-3.5-turbo"

client = OpenAIChatClient(api_key=api_key, model_id=model_id)
agent = ChatAgent(client=client)

response = agent.chat("Explain the difference between synchronous and asynchronous programming.")
print(f"Response with explicit settings: {response}")

```

--------------------------------

TITLE: OpenAI Responses Agent with Reasoning Capabilities
DESCRIPTION: Demonstrates how agents can provide detailed reasoning for their responses. This feature helps in understanding the thought process behind the agent's answers.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.responses import OpenAIResponsesClient
from agent_framework.agents.chat_agent import ChatAgent

# Initialize the client and agent
client = OpenAIResponsesClient()
agent = ChatAgent(client=client)

# Ask a question and request reasoning
response = agent.chat("Given that A > B and B > C, what is the relationship between A and C? Explain your reasoning.")
print(f"Response with reasoning: {response}")

```

--------------------------------

TITLE: Manually Start Aspire Dashboard via Docker
DESCRIPTION: This command starts the .NET Aspire Dashboard in a detached Docker container, mapping host ports for the web UI and OpenTelemetry collector endpoint. It configures the dashboard for anonymous access during development.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentOpenTelemetry/README.md

LANGUAGE: bash
CODE:
```
docker run -d --name aspire-dashboard -p 4318:18888 -p 4317:18889 -e DOTNET_DASHBOARD_UNSECURED_ALLOW_ANONYMOUS=true mcr.microsoft.com/dotnet/aspire-dashboard:9.0
```

--------------------------------

TITLE: Run GAIA Evaluation Script
DESCRIPTION: Executes a Python evaluation script using the `uv` command. This command initiates the GAIA benchmark process, which may download data and save results.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/gaia/README.md

LANGUAGE: bash
CODE:
```
uv run python run_gaia.py
```

--------------------------------

TITLE: Configure Application with OTLP Endpoint Environment Variable
DESCRIPTION: This example shows how to set the OTLP endpoint for an application when running it via the command line. It enables OpenTelemetry and specifies the local endpoint for telemetry data transmission.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/observability/README.md

LANGUAGE: bash
CODE:
```
ENABLE_OTEL=true OTLP_ENDPOINT=http://localhost:4317 python 01-zero_code.py
```

--------------------------------

TITLE: LlamaIndex Callback Manager for Query Observation
DESCRIPTION: This Python example shows how to set up a callback manager in LlamaIndex to observe query execution. It uses `LlamaDebugHandler` to capture events and provides a `CallbackManager` instance that can be assigned to components like `VectorStoreIndex` or query engines. This is primarily for debugging and tracing query operations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

debug_handler = LlamaDebugHandler()  # Concrete handler subclassing BaseCallbackHandler
callback_manager = CallbackManager([debug_handler])

# Assign to components, e.g., an index or query engine
# index = VectorStoreIndex.from_documents(documents, callback_manager=callback_manager)
# query_engine = index.as_query_engine()
# response = query_engine.query("What is this about?")
```

--------------------------------

TITLE: Implement Custom Assistant and User Agents in Python
DESCRIPTION: This snippet demonstrates how to create a custom TaskRunner to override the default behavior of assistant and user simulator agents. It allows for custom system prompts, tools, and other configurations for enhanced agent interaction. Dependencies include agent_framework.lab.tau2.TaskRunner and agent_framework.ChatAgent.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/tau2/README.md

LANGUAGE: python
CODE:
```
from agent_framework.lab.tau2 import TaskRunner
from agent_framework import ChatAgent

class CustomTaskRunner(TaskRunner):
    def assistant_agent(self, assistant_chat_client):
        # Override to customize the assistant agent
        return ChatAgent(
            chat_client=assistant_chat_client,
            instructions="Your custom system prompt here",
            # Add custom tools, temperature, etc.
        )

    def user_simulator(self, user_chat_client, task):
        # Override to customize the user simulator
        return ChatAgent(
            chat_client=user_chat_client,
            instructions="Custom user simulator prompt",
        )
```

--------------------------------

TITLE: CrewAI Event Listener for Crew Kickoff
DESCRIPTION: This Python snippet demonstrates how to create a custom event listener in CrewAI to react to the 'CrewKickoffStartedEvent'. It utilizes the event bus to register a callback function that prints a message when a crew starts. This is useful for logging or triggering actions based on workflow events.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: python
CODE:
```
from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    BaseEventListener,
    crewai_event_bus
)

class MyCustomListener(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print(f"Crew '{event.crew_name}' started!")

my_listener = MyCustomListener()  # Automatically registers on init

# Use in a crew
# crew = Crew(agents=[...], tasks=[...])
```

--------------------------------

TITLE: Configure OpenAI API Keys in .env file
DESCRIPTION: This snippet shows the content of an `.env` or `openai.env` file used to store OpenAI API credentials and model configurations. It allows Agent Framework to load these settings from the environment, especially when using VSCode's Python extension.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: env
CODE:
```
OPENAI_API_KEY=""
OPENAI_CHAT_MODEL_ID="gpt-4o-mini"
```

--------------------------------

TITLE: OpenAI Chat Agent with Web Search
DESCRIPTION: Shows how to integrate web search capabilities with OpenAI chat agents. This allows the agent to retrieve and utilize information from the internet to formulate responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.chat import OpenAIChatClient
from agent_framework.agents.chat_agent import ChatAgent
from agent_framework.tools.web_search.web_search import WebSearchTool

# Initialize the web search tool
web_search_tool = WebSearchTool()

# Initialize the client and agent, providing the web search tool
client = OpenAIChatClient(tools=[web_search_tool])
agent = ChatAgent(client=client)

# Ask a question that requires up-to-date information from the web
response = agent.chat("What are the latest headlines in technology news today?")
print(f"Response using web search: {response}")

```

--------------------------------

TITLE: Automated Agent Framework Setup with uv and Poe
DESCRIPTION: This single command provides an alternative, automated way to set up the Agent Framework development environment using `uv` and `poe`. It reinstalls the virtual environment, packages, dependencies, and pre-commit hooks, allowing for easy Python version switching.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: bash
CODE:
```
uv run poe setup -p 3.13
```

--------------------------------

TITLE: OpenAI Chat Agent with Local MCP Server
DESCRIPTION: Shows how to integrate OpenAI agents with local Model Context Protocol (MCP) servers. This integration allows for enhanced functionality and tool usage within a local environment.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/agents/openai/README.md

LANGUAGE: python
CODE:
```
from agent_framework.tools.openai.chat import OpenAIChatClient
from agent_framework.agents.chat_agent import ChatAgent

# Assume a local MCP server is running and accessible at this URL
mcp_server_url = "http://localhost:8000/v1"

# Initialize the client pointing to the local MCP server
# You might need to configure authentication or other parameters depending on your MCP setup
client = OpenAIChatClient(base_url=mcp_server_url, api_key="dummy-key") # API key might be ignored or required by server
agent = ChatAgent(client=client)

response = agent.chat("Process this data using the local model.")
print(f"Response from local MCP server: {response}")

```

--------------------------------

TITLE: Run Single Task with τ²-bench
DESCRIPTION: This Python code snippet demonstrates how to run a single customer service task using the τ²-bench framework. It initializes the TaskRunner, sets up OpenAI chat clients for both the assistant and user simulator, retrieves a task, and executes the conversation. Finally, it evaluates and prints the reward for the completed task. Ensure you have the necessary OpenAI API key and model IDs configured.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/tau2/README.md

LANGUAGE: python
CODE:
```
import asyncio
from agent_framework.openai import OpenAIChatClient
from agent_framework.lab.tau2 import TaskRunner
from tau2.domains.airline.environment import get_tasks

async def run_single_task():
    # Initialize the task runner
    runner = TaskRunner(max_steps=50)

    # Set up your LLM clients
    assistant_client = OpenAIChatClient(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_id="gpt-4o"
    )
    user_client = OpenAIChatClient(
        base_url="https://api.openai.com/v1",
        api_key="your-api-key",
        model_id="gpt-4o-mini"
    )

    # Get a task and run it
    tasks = get_tasks()
    task = tasks[0]  # Run the first task

    conversation = await runner.run(task, assistant_client, user_client)
    reward = runner.evaluate(task, conversation, runner.termination_reason)

    print(f"Task completed with reward: {reward}")

# Run the example
asyncio.run(run_single_task())
```

--------------------------------

TITLE: Stable Import Example: Google Chat Client
DESCRIPTION: Demonstrates the intended stable import path for subpackages, ensuring that imports remain consistent even if the internal package structure changes. This promotes a reliable developer experience.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: python
CODE:
```
from agent_framework.google import GoogleChatClient
```

--------------------------------

TITLE: Google - Remote MCP Tool Integration
DESCRIPTION: Python example for integrating remote MCP tools, such as file operations, into an ADK agent.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Google - Remote MCP Tool Integration

### Description
This section provides a Python code example demonstrating how to configure and use remote MCP tools within the Google ADK agent framework.

### Method
N/A (This is a code snippet)

### Endpoint
N/A

### Parameters
N/A

### Request Example
```python
async def get_agent_async():
    toolset = MCPToolset(
        tool_filter=['read_file', 'list_directory'] # Optional: filter specific tools
        connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
    )

    # Use in an agent
    root_agent = LlmAgent(
        model='model', # Adjust model name if needed based on availability
        name='agent_name',
        instruction='agent_instructions',
        tools=[toolset], # Provide the MCP tools to the ADK agent
    )
    return root_agent, toolset
```

### Response
#### Success Response (200)
N/A

#### Response Example
N/A
```

--------------------------------

TITLE: Configure Agent Framework Google Optional Dependency in pyproject.toml
DESCRIPTION: This TOML snippet demonstrates how to declare an optional dependency for Agent Framework's Google connectors within the `pyproject.toml` file. This allows developers to install the core framework and optionally include Google-specific components and their dependencies using `pip install agent-framework[google]`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/design/python-package-setup.md

LANGUAGE: toml
CODE:
```
[project.optional-dependencies]
google = [
    "agent-framework-google == 1.0.0"
]
```

--------------------------------

TITLE: Azure AI Foundry Agent Service - Bing Search
DESCRIPTION: This endpoint allows agents to perform web searches using Bing. It defines the structure for sending search configurations and the expected response format for tool calls.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Azure AI Foundry Agent Service - Bing Search

### Description
This API allows agents to perform web searches using Bing. It defines the structure for sending search configurations and the expected response format for tool calls.

### Method
POST

### Endpoint
/search

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools to use, including `bing_grounding`.
  - **type** (string) - Required - Must be `bing_grounding`.
  - **bing_grounding** (object) - Required - Configuration for Bing search.
    - **search_configurations** (array) - Required - List of search configurations.
      - **connection_id** (string) - Required - The ID of the Bing connection.
      - **count** (number) - Optional - The number of search results to return.
      - **market** (string) - Optional - The market to search in (e.g., "en-US").
      - **set_lang** (string) - Optional - The language to set for the search.
      - **freshness** (string) - Optional - The freshness of the search results (e.g., "Day", "Week", "Month").

### Request Example
```json
{
  "tools": [
    {
      "type": "bing_grounding",
      "bing_grounding": {
        "search_configurations": [
          {
            "connection_id": "{string}",
            "count": 5,
            "market": "en-US",
            "set_lang": "en-US",
            "freshness": "Day"
          }
        ]
      }
    }
  ]
}
```

### Response
#### Success Response (200)
- **tool_calls** (array) - Contains information about the tool calls made.
  - **id** (string) - The ID of the tool call.
  - **type** (string) - The type of tool call, expected to be `function`.
  - **bing_grounding** (object) - Reserved for future use.

#### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "function",
      "bing_grounding": {}
    }
  ]
}
```
```

--------------------------------

TITLE: Apply and Remove Environment State Patches in Python
DESCRIPTION: This snippet illustrates how to enable and disable compatibility patches for τ²-bench integration using `patch_env_set_state` and `unpatch_env_set_state`. These functions are crucial for ensuring proper environment setup and cleanup during agent framework operations. Dependencies include agent_framework.lab.tau2.patch_env_set_state and agent_framework.lab.tau2.unpatch_env_set_state.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/tau2/README.md

LANGUAGE: python
CODE:
```
from agent_framework.lab.tau2 import patch_env_set_state, unpatch_env_set_state

# Enable compatibility patches for τ²-bench integration
patch_env_set_state()

# Disable patches when done
unpatch_env_set_state()
```

--------------------------------

TITLE: Configure Environment Variables for OpenAI
DESCRIPTION: This code snippet shows how to set environment variables required for configuring OpenAI API access. It includes setting the base URL for OpenAI API calls and the API key. It also provides an example for configuring custom OpenAI endpoints. These are typically set in a shell environment before running the Python scripts.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/tau2/README.md

LANGUAGE: bash
CODE:
```
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_API_KEY="your-api-key"

# Optional: for custom endpoints
export OPENAI_BASE_URL="https://your-custom-endpoint.com/v1"
```

--------------------------------

TITLE: Manually Set Up Agent Framework Environment with uv
DESCRIPTION: These commands, executed after `uv` is installed, manually configure the Agent Framework development environment. They install multiple Python versions, create a virtual environment, synchronize development dependencies, install Poe tasks, and set up pre-commit hooks.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: bash
CODE:
```
# Install Python 3.10, 3.11, 3.12, and 3.13
uv python install 3.10 3.11 3.12 3.13
# Create a virtual environment with Python 3.10 (you can change this to 3.11, 3.12 or 3.13)
$PYTHON_VERSION = "3.10"
uv venv --python $PYTHON_VERSION
# Install AF and all dependencies
uv sync --dev
# Install all the tools and dependencies
uv run poe install
# Install pre-commit hooks
uv run poe pre-commit-install
```

--------------------------------

TITLE: Instantiate Agent Framework Messages (Avoid This Pattern)
DESCRIPTION: This example shows a non-preferred way to instantiate `UserMessage` and `AssistantMessage` from the `agent_framework`. While functional, the text implies this pattern is considered unnecessary inheritance or an anti-pattern within the project. It demonstrates basic object creation.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: python
CODE:
```
from agent_framework import UserMessage, AssistantMessage

user_msg = UserMessage(content="Hello, world!")
asst_msg = AssistantMessage(content="Hello, world!")
```

--------------------------------

TITLE: DELETE /v1/threads/{thread_id}
DESCRIPTION: No description

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md



--------------------------------

TITLE: Bash Example: Execute Math Agent Training Script
DESCRIPTION: Runs the Python script 'train_math_agent.py' to initiate the training of a math agent. This script utilizes the Agent Framework Lab and Agent-lightning for the training process.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
# Run the training script
python train_math_agent.py
```

--------------------------------

TITLE: POST /v1/entities/add
DESCRIPTION: Adds a new entity to the DevUI from a specified URL. This is used for dynamically loading sample entities or remote configurations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## POST /v1/entities/add

### Description
Adds a new entity (agent or workflow) to the DevUI from a specified URL. This endpoint is primarily used for dynamically loading sample entities or remote configurations into the running application.

### Method
POST

### Endpoint
/v1/entities/add

### Parameters
#### Path Parameters
(None)

#### Query Parameters
(None)

#### Request Body
- **url** (string) - Required - The URL pointing to the entity's configuration or definition.

### Request Example
{
  "url": "https://example.com/my_agent_config.json"
}

### Response
#### Success Response (200)
- **message** (string) - A confirmation message indicating the entity was added.
- **entity_id** (string) - The ID of the newly added entity.

#### Response Example
{
  "message": "Entity added successfully",
  "entity_id": "new_sample_agent"
}
```

--------------------------------

TITLE: Install Microsoft Agent Framework DevUI (pip)
DESCRIPTION: This command installs the DevUI component of the Microsoft Agent Framework using pip. The `--pre` flag is used to include pre-release versions, ensuring access to the latest features.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: bash
CODE:
```
pip install agent-framework-devui --pre
```

--------------------------------

TITLE: Run τ²-bench Benchmark Script
DESCRIPTION: This section provides examples of how to execute the τ²-bench benchmark using the provided Python script. It shows commands for running with default models, specifying custom assistant and user models, debugging a specific task by its ID, and limiting the maximum conversation steps. These commands are executed from the terminal.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/tau2/README.md

LANGUAGE: bash
CODE:
```
# Run with default models (gpt-4.1 for both agent and user)
python samples/run_benchmark.py

# Use custom models
python samples/run_benchmark.py --assistant gpt-4o --user gpt-4o-mini

# Debug a specific task
python samples/run_benchmark.py --debug-task-id task_001 --assistant gpt-4o

# Limit conversation length
python samples/run_benchmark.py --max-steps 20
```

--------------------------------

TITLE: Integrate .NET function tools with AIAgent using Description attributes
DESCRIPTION: This C# example illustrates how to create and register function tools for an `AIAgent` using `Microsoft.Agents.AI` and `Azure.AI.OpenAI`. The `GetWeather` function is marked with `Description` attributes, allowing the agent to understand its purpose and parameters. It shows both non-streaming and streaming execution of agent queries that utilize the defined function.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: csharp
CODE:
```
using System.ComponentModel;
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using OpenAI;

var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
var deploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? "gpt-4o-mini";

[Description("Get the weather for a given location.")]
static string GetWeather([Description("The location to get the weather for.")] string location)
    => $"The weather in {location} is cloudy with a high of 15°C.";

// Create agent with function tool
AIAgent agent = new AzureOpenAIClient(
    new Uri(endpoint),
    new AzureCliCredential())
    .GetChatClient(deploymentName)
    .CreateAIAgent(
        instructions: "You are a helpful assistant",
        tools: [AIFunctionFactory.Create(GetWeather)]);

// Non-streaming with function call
Console.WriteLine(await agent.RunAsync("What is the weather like in Amsterdam?"));

// Streaming with function call
await foreach (var update in agent.RunStreamingAsync("What is the weather like in Paris?"))
{
    Console.WriteLine(update);
}
```

--------------------------------

TITLE: Build Frontend for Production (Yarn)
DESCRIPTION: Builds the frontend application for production. The resulting static files are typically copied to the backend for serving.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
yarn build
```

--------------------------------

TITLE: Set Up Frontend Environment (Yarn/Bash)
DESCRIPTION: Navigates to the `frontend` directory, installs JavaScript dependencies using `yarn install`, and configures environment files (`.env.local` and `.env.production`) to specify the backend API URL. This prepares the frontend for development or building.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
cd frontend
yarn install

# Create .env.local with backend URL
echo 'VITE_API_BASE_URL=http://localhost:8000' > .env.local

# Create .env.production (empty for relative URLs)
echo '' > .env.production
```

--------------------------------

TITLE: POST /v1/responses
DESCRIPTION: Executes an agent or workflow using the standard OpenAI API format. This endpoint supports both streaming and synchronous execution, requiring the `entity_id` in `extra_body`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## POST /v1/responses

### Description
Executes an agent or workflow using the standard OpenAI API chat completions format. This endpoint supports both streaming and synchronous execution, requiring the `entity_id` to be specified in the `extra_body` field to identify the target entity.

### Method
POST

### Endpoint
/v1/responses

### Parameters
#### Path Parameters
(None)

#### Query Parameters
(None)

#### Request Body
- **model** (string) - Required - Placeholder, typically "agent-framework".
- **input** (string) - Required - The user's input message or prompt for the agent/workflow.
- **extra_body** (object) - Required - Additional parameters.
    - **entity_id** (string) - Required - The unique identifier of the agent or workflow to execute.

### Request Example
{
  "model": "agent-framework",
  "input": "Hello world",
  "extra_body": {"entity_id": "weather_agent"}
}

### Response
#### Success Response (200)
- **id** (string) - A unique identifier for the response.
- **object** (string) - The type of object, e.g., "chat.completion".
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the completion.
- **choices** (array of objects) - List of completion choices.
    - **index** (integer) - The index of the choice.
    - **message** (object) - The message from the agent/workflow.
        - **role** (string) - The role of the message, e.g., "assistant".
        - **content** (string) - The content of the message.
    - **finish_reason** (string) - The reason the completion finished.

#### Response Example
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "agent-framework",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I am the WeatherAgent. How can I help you?"
      },
      "finish_reason": "stop"
    }
  ]
}
```

--------------------------------

TITLE: Set Environment Variables and Run Tau2 Agent Training (Bash)
DESCRIPTION: This snippet shows how to set necessary environment variables for data directory, API keys, and Weights & Biases tracking, followed by commands to start a Ray cluster and execute the Tau2 agent training script.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
# Set required environment variables
export TAU2_DATA_DIR="/path/to/tau2/data"

# Used for user simulator and LLM judge
export OPENAI_BASE_URL="your-endpoint"
export OPENAI_API_KEY="your-key"

# Used for tracking on Weights & Biases
export WANDB_API_KEY="your-key"

# Run the ray cluster
ray start --head --dashboard-host=0.0.0.0

# Train the tau2 agent
cd samples
python samples/train_tau2_agent.py

# Debug mode
python samples/train_tau2_agent.py --debug
```

--------------------------------

TITLE: GET /v1/entities
DESCRIPTION: Lists all discovered agents and workflows available in the DevUI. This endpoint provides an overview of all entities currently registered.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## GET /v1/entities

### Description
Lists all discovered agents and workflows currently available in the DevUI. This endpoint provides an overview of all entities registered, including those discovered via directory and in-memory.

### Method
GET

### Endpoint
/v1/entities

### Parameters
#### Path Parameters
(None)

#### Query Parameters
(None)

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **entities** (array of objects) - A list of discovered agents and workflows, each with basic identification information.

#### Response Example
{
  "entities": [
    {
      "id": "weather_agent",
      "name": "WeatherAgent",
      "type": "Agent"
    },
    {
      "id": "my_workflow",
      "name": "MyWorkflow",
      "type": "Workflow"
    }
  ]
}
```

--------------------------------

TITLE: GET /health
DESCRIPTION: Performs a simple health check to determine if the DevUI API server is operational. This endpoint is useful for monitoring the service status.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## GET /health

### Description
Performs a simple health check to determine if the DevUI API server is operational. This endpoint is useful for monitoring the service status and ensuring the server is responsive.

### Method
GET

### Endpoint
/health

### Parameters
#### Path Parameters
(None)

#### Query Parameters
(None)

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **status** (string) - Indicates the health status, typically "OK".

#### Response Example
{
  "status": "OK"
}
```

--------------------------------

TITLE: Install Agent Framework with GAIA dependencies
DESCRIPTION: Installs the agent-framework-lab package with GAIA extra dependencies from source. Requires cloning the repository and using pip for installation.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/gaia/README.md

LANGUAGE: bash
CODE:
```
git clone https://github.com/microsoft/agent-framework.git
cd agent-framework/python/packages/lab
pip install -e ".[gaia]"
```

--------------------------------

TITLE: Interact with Agent via OpenAI-Compatible API (cURL)
DESCRIPTION: This cURL command demonstrates how to interact with an agent or workflow running in DevUI using an OpenAI-compatible API format. It sends a POST request to the `/v1/responses` endpoint, specifying the `entity_id` in the `extra_body` to target a specific agent.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: bash
CODE:
```
curl -X POST http://localhost:8080/v1/responses \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "model": "agent-framework",
  "input": "Hello world",
  "extra_body": {"entity_id": "weather_agent"}
}

```

--------------------------------

TITLE: GET /v1/threads
DESCRIPTION: Lists all conversation threads, optionally filtered by `agent_id`. This endpoint helps retrieve existing threads associated with agents.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## GET /v1/threads

### Description
Lists all conversation threads managed by the DevUI, optionally filtered by a specific `agent_id`. This endpoint helps retrieve existing threads associated with agents for further interaction or review.

### Method
GET

### Endpoint
/v1/threads

### Parameters
#### Path Parameters
(None)

#### Query Parameters
- **agent_id** (string) - Optional - Filter threads by the ID of the associated agent.

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **threads** (array of objects) - A list of thread objects, each containing thread metadata.

#### Response Example
{
  "threads": [
    {
      "id": "thread_abc123",
      "agent_id": "weather_agent",
      "created_at": "2023-10-27T10:00:00Z"
    }
  ]
}
```

--------------------------------

TITLE: Build and Serve Agent Framework Documentation
DESCRIPTION: Outlines the command-line commands for managing project documentation. It includes building the documentation, serving it locally with auto-reload, and checking for warnings using `uv run poe`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: bash
CODE:
```
# Build documentation
uv run poe docs-build

# Serve documentation locally with auto-reload
uv run poe docs-serve

# Check documentation for warnings
uv run poe docs-check
```

--------------------------------

TITLE: POST /v1/threads
DESCRIPTION: Creates a new conversation thread for an agent. This endpoint is optional and allows for managing conversational context separately.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## POST /v1/threads

### Description
Creates a new conversation thread for an agent. This endpoint is optional and provides a way to manage conversational context and state for interactions with an agent.

### Method
POST

### Endpoint
/v1/threads

### Parameters
#### Path Parameters
(None)

#### Query Parameters
(None)

#### Request Body
- **agent_id** (string) - Optional - The ID of the agent for which to create the thread.

### Request Example
{
  "agent_id": "weather_agent"
}

### Response
#### Success Response (200)
- **thread_id** (string) - The unique identifier of the newly created thread.

#### Response Example
{
  "thread_id": "thread_abc123"
}
```

--------------------------------

TITLE: Launch DevUI from CLI with Directory Discovery (Bash)
DESCRIPTION: This CLI command launches the DevUI server, enabling it to discover agents and workflows defined within a specified directory (e.g., `./agents`). It starts the web UI and API server, accessible at `http://localhost:8080`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: bash
CODE:
```
devui ./agents --port 8080
```

--------------------------------

TITLE: Set OpenAI API Key Environment Variable
DESCRIPTION: Sets the OpenAI API key as an environment variable, which is required for enabling hybrid search with OpenAI embeddings in the Redis context provider.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/context_providers/redis/README.md

LANGUAGE: bash
CODE:
```
export OPENAI_API_KEY="<your key>"
```

--------------------------------

TITLE: Google Vertex AI Generative AI Message Request
DESCRIPTION: Shows the JSON request format for Google's Vertex AI Generative AI, including content and tool definitions for Google Search integration. The `tools` array specifies the use of `googleSearch`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "{string}"
        }
      ]
    }
  ],
  "tools": [
    {
      "googleSearch": {}
    }
  ]
}
```

--------------------------------

TITLE: Google Vertex AI - Function Calling
DESCRIPTION: Documentation for function calling in Google's Vertex AI Generative AI, detailing message request and tool call response formats.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Google Vertex AI - Function Calling

### Description
This section outlines the implementation of function calling for Google's Vertex AI Generative AI, including request and response structures.

### Method
Not specified (details provided for request/response bodies)

### Endpoint
Not specified (related to REST API for Vertex AI Generative AI)

### Parameters
#### Request Body (tools)
- **tools** (array) - Required - A list of tools available to the model.
  - **functionDeclarations** (array) - Required - A list of function declarations.
    - **name** (string) - Required - The name of the function.
    - **description** (string) - Optional - A description of the function.
    - **parameters** (object) - Required - The parameters the function expects, represented as a JSON Schema object.

### Request Example
```json
{
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "{string}",
          "description": "{string}",
          "parameters": "{JSON Schema object}"
        }
      ]
    }
  ]
}
```

### Response
#### Tool Call Response (content.parts)
- **content** (object) - The model's response content.
  - **role** (string) - The role of the participant, typically "model".
  - **parts** (array) - Contains the parts of the response.
    - **functionCall** (object) - Details of the function call.
      - **name** (string) - The name of the function to call.
      - **args** (object) - The arguments to pass to the function.
        - **{argument_name}** (any) - The name and value of a function argument.

#### Response Example
```json
{
  "content": {
    "role": "model",
    "parts": [
      {
        "functionCall": {
          "name": "{string}",
          "args": {
            "{argument_name}": {}
          }
        }
      }
    ]
  }
}
```
```

--------------------------------

TITLE: Install Agent Framework Lab with Lightning Dependencies
DESCRIPTION: Installs the agent-framework lab package with specific dependencies for Lightning, enabling RL training capabilities. This command clones the repository and installs the package in editable mode.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
git clone https://github.com/microsoft/agent-framework.git
cd agent-framework/python/packages/lab
pip install -e ".[lightning]"
```

--------------------------------

TITLE: Run Frontend in Development Mode (Yarn)
DESCRIPTION: Starts the frontend development server. This allows for live development and testing of the user interface.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
yarn dev
```

--------------------------------

TITLE: Create Environment File (Bash)
DESCRIPTION: Copies the example environment file `.env.example` to `.env`. This creates a new configuration file that needs to be edited with actual API keys.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
cp .env.example .env
```

--------------------------------

TITLE: Function Calling: Google Vertex AI (JSON)
DESCRIPTION: Defines the JSON structure for function calling within Google's Vertex AI platform. This includes the 'tools' format for requests and the 'content' part of the response containing 'functionCall'.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "{string}",
          "description": "{string}",
          "parameters": "{JSON Schema object}"
        }
      ]
    }
  ]
}
```

LANGUAGE: json
CODE:
```
{
  "content": {
    "role": "model",
    "parts": [
      {
        "functionCall": {
          "name": "{string}",
          "args": {
            "{argument_name}": {}
          }
        }
      }
    ]
  }
}
```

--------------------------------

TITLE: Clone Agent Framework Repository (Bash)
DESCRIPTION: Clones the `agent-framework` repository from GitHub and navigates into its directory. This is the initial step to obtain the source code for the project.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
git clone https://github.com/microsoft/agent-framework.git
cd agent-framework
```

--------------------------------

TITLE: Google Vertex AI: Code Execution Tool Response Structure
DESCRIPTION: Illustrates the JSON format for a tool call response from Google Vertex AI, detailing the `executableCode` and `codeExecutionResult` parts. This response includes the language and code executed, along with the outcome and output.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "content": {
    "role": "model",
    "parts": [
      {
        "executableCode": {
          "language": "{string}",
          "code": "{string}"
        }
      },
      {
        "codeExecutionResult": {
          "outcome": "{string}",
          "output": "{string}"
        }
      }
    ]
  }
}
```

--------------------------------

TITLE: GET /v1/entities/{entity_id}/info
DESCRIPTION: Retrieves detailed information about a specific agent or workflow. Use this endpoint to get comprehensive details about a particular entity.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## GET /v1/entities/{entity_id}/info

### Description
Retrieves detailed information about a specific agent or workflow by its unique ID. This endpoint provides comprehensive details about the entity, such as its configuration, tools, and capabilities.

### Method
GET

### Endpoint
/v1/entities/{entity_id}/info

### Parameters
#### Path Parameters
- **entity_id** (string) - Required - The unique identifier of the agent or workflow.

#### Query Parameters
(None)

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **id** (string) - The unique identifier of the entity.
- **name** (string) - The human-readable name of the entity.
- **type** (string) - The type of entity (e.g., "Agent", "Workflow").
- **description** (string) - A description of the entity.
- **tools** (array) - List of tools available to the entity.

#### Response Example
{
  "id": "weather_agent",
  "name": "WeatherAgent",
  "type": "Agent",
  "description": "An agent that can fetch weather information.",
  "tools": [
    {
      "name": "get_weather",
      "description": "Get weather for a location.",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string"
          }
        },
        "required": ["location"]
      }
    }
  ]
}
```

--------------------------------

TITLE: Google Vertex AI Code Execution
DESCRIPTION: This section details the request and response format for using the code execution tool with Google Vertex AI.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Google Vertex AI Code Execution

### Description
This endpoint allows for code execution within the Google Vertex AI platform, enabling programmatic tasks and data processing.

### Method
POST

### Endpoint
/vertex-ai/code-execution

### Parameters
#### Request Body
- **contents** (object) - Required - The main content of the message, including role and parts.
  - **role** (string) - Required - The role of the message sender (e.g., "model", "user").
  - **parts** (object) - Required - The content of the message.
    - **text** (string) - Required - The text content of the message.
- **tools** (array) - Required - A list of tools to be used.
  - **codeExecution** (object) - Required - Specifies the code execution tool.

### Request Example
```json
{
  "contents": {
    "role": "user",
    "parts": {
      "text": "Execute this Python code: print(\"Hello, World!\")"
    }
  },
  "tools": [
    {
      "codeExecution": {}
    }
  ]
}
```

### Response
#### Success Response (200)
- **content** (object) - Required - The response content from the model.
  - **role** (string) - Required - The role of the message sender (e.g., "model").
  - **parts** (array) - Required - An array of message parts.
    - **executableCode** (object) - The code that was executed.
      - **language** (string) - Required - The programming language of the code.
      - **code** (string) - Required - The code snippet.
    - **codeExecutionResult** (object) - The result of the code execution.
      - **outcome** (string) - Required - The outcome of the execution (e.g., "SUCCESS", "ERROR").
      - **output** (string) - The output produced by the code execution.

#### Response Example
```json
{
  "content": {
    "role": "model",
    "parts": [
      {
        "executableCode": {
          "language": "python",
          "code": "print(\"Hello, World!\")"
        }
      },
      {
        "codeExecutionResult": {
          "outcome": "SUCCESS",
          "output": "Hello, World!\n"
        }
      }
    ]
  }
}
```
```

--------------------------------

TITLE: GET /v1/threads/{thread_id}
DESCRIPTION: Retrieves detailed information about a specific conversation thread. This includes metadata about the thread and its association.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## GET /v1/threads/{thread_id}

### Description
Retrieves detailed information about a specific conversation thread using its unique `thread_id`. This includes metadata about the thread, its associated agent, and creation timestamp.

### Method
GET

### Endpoint
/v1/threads/{thread_id}

### Parameters
#### Path Parameters
- **thread_id** (string) - Required - The unique identifier of the conversation thread.

#### Query Parameters
(None)

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **id** (string) - The unique identifier of the thread.
- **agent_id** (string) - The ID of the agent associated with this thread.
- **created_at** (string) - Timestamp of when the thread was created.

#### Response Example
{
  "id": "thread_abc123",
  "agent_id": "weather_agent",
  "created_at": "2023-10-27T10:00:00Z"
}
```

--------------------------------

TITLE: Google Vertex AI: Code Execution Request Structure
DESCRIPTION: Defines the JSON structure for a message request to Google Vertex AI's generative models when utilizing the code execution tool. It specifies the content and the activation of the code execution tool.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "contents": {
    "role": "{string}",
    "parts": {
      "text": "{string}"
    }
  },
  "tools": [
    {
      "codeExecution": {}
    }
  ]
}
```

--------------------------------

TITLE: Run Agent Framework Tests with uv and pytest
DESCRIPTION: Provides command-line examples for executing tests in the `agent-framework` project using `uv run poe` and `pytest`. It covers running all tests with coverage, a specific test file, and tests with verbose output.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: bash
CODE:
```
# Run all tests with coverage
uv run poe test

# Run specific test file
uv run pytest tests/test_agents.py

# Run with verbose output
uv run pytest -v
```

--------------------------------

TITLE: DELETE /v1/entities/{entity_id}
DESCRIPTION: Removes a specific remote entity from the DevUI. This allows for de-registering entities that were added dynamically.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: APIDOC
CODE:
```
## DELETE /v1/entities/{entity_id}

### Description
Removes a specific remote entity (agent or workflow) from the DevUI based on its unique ID. This endpoint is used to de-register entities that were dynamically added or are no longer needed.

### Method
DELETE

### Endpoint
/v1/entities/{entity_id}

### Parameters
#### Path Parameters
- **entity_id** (string) - Required - The unique identifier of the entity to be removed.

#### Query Parameters
(None)

#### Request Body
(None)

### Request Example
(None)

### Response
#### Success Response (200)
- **message** (string) - A confirmation message indicating the entity was removed.

#### Response Example
{
  "message": "Entity 'my_sample_agent' removed successfully"
}
```

--------------------------------

TITLE: Test DevUI API with cURL (Bash)
DESCRIPTION: Sends a POST request to the DevUI's API endpoint (`/v1/responses`) using `curl`. This demonstrates how to programmatically interact with the DevUI to query specific agents, like the 'weather_agent', and receive responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
curl -X POST http://localhost:8080/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agent-framework",
    "input": "What is the weather in Seattle?",
    "extra_body": {"entity_id": "weather_agent"}
  }'
```

--------------------------------

TITLE: Configure NuGet.Config for GitHub Microsoft Packages
DESCRIPTION: This XML configuration file manually sets up the NuGet package sources and mappings to include packages from the Microsoft GitHub registry, specifically for nightly builds. It also includes credentials for authentication.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/FAQS.md

LANGUAGE: xml
CODE:
```
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" protocolVersion="3" />
    <add key="github" value="https://nuget.pkg.github.com/microsoft/index.json" />
  </packageSources>

  <packageSourceMapping>
    <packageSource key="nuget.org">
      <package pattern="*" />
    </packageSource>
    <packageSource key="github">
      <package pattern="*nightly"/>
    </packageSource>
  </packageSourceMapping>

  <packageSourceCredentials>
    <github>
        <add key="Username" value="<Your GitHub Id>" />
        <add key="ClearTextPassword" value="<Your Personal Access Token>" />
      </github>
  </packageSourceCredentials>
</configuration>
```

--------------------------------

TITLE: OpenAI Assistant API Code Interpreter Request and Response
DESCRIPTION: Illustrates the JSON format for requesting the code interpreter tool within the OpenAI Assistant API and the subsequent tool call response. The request specifies tool usage and file IDs, while the response details code execution input and log outputs. .NET support is confirmed.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "tool_resources": {
    "code_interpreter": {
      "file_ids": ["{string}"]
    }
  }
}
```

LANGUAGE: json
CODE:
```
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "code",
      "code": {
        "input": "{string}",
        "outputs": [
          {
            "type": "logs",
            "logs": "{string}"
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: Add GitHub Microsoft NuGet Source via CLI
DESCRIPTION: This command adds the Microsoft GitHub Packages source to your NuGet configuration, allowing you to download nightly builds. It requires your GitHub username and personal access token, storing the password in clear text.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/FAQS.md

LANGUAGE: powershell
CODE:
```
dotnet nuget add source --username GITHUBUSERNAME --password GITHUBPERSONALACCESSTOKEN --store-password-in-clear-text --name GitHubMicrosoft "https://nuget.pkg.github.com/microsoft/index.json"
```

--------------------------------

TITLE: Set Hugging Face Token for GAIA
DESCRIPTION: Sets the Hugging Face token as an environment variable. This token is required to access the GAIA benchmark data from Hugging Face.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/gaia/README.md

LANGUAGE: bash
CODE:
```
export HF_TOKEN="hf*..." # must have access to gaia-benchmark/GAIA
```

--------------------------------

TITLE: Launch DevUI with Directory-Based Discovery (Bash)
DESCRIPTION: Navigates to the `packages/devui/samples` directory and runs the `devui` command. This launches the UI, discovering all example agents and workflows, accessible at `http://localhost:8080`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
cd packages/devui/samples
devui
```

--------------------------------

TITLE: Render DOT Output with Graphviz
DESCRIPTION: Pipes the output of the workflow visualization sample to the Graphviz 'dot' command to render a PNG image of the workflow. This requires Graphviz to be installed on the system.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/Workflows/Visualization/README.md

LANGUAGE: bash
CODE:
```
dotnet run | tail -n +20 | dot -Tpng -o workflow.png
```

--------------------------------

TITLE: Install Agent Framework Redis Extra
DESCRIPTION: Installs the necessary package for the Agent Framework's Redis integration, enabling persistent and searchable memory for agents.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/context_providers/redis/README.md

LANGUAGE: bash
CODE:
```
pip install "agent-framework-redis"
```

--------------------------------

TITLE: OpenAI Responses API Code Interpreter Request and Response
DESCRIPTION: Details the JSON structure for enabling the code interpreter tool with container auto-detection in the OpenAI Responses API message request and the array-based tool call response format. The response includes status, container ID, and results such as logs and files. .NET support is currently in development.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "code_interpreter",
      "container": { "type": "auto" }
    }
  ]
}
```

LANGUAGE: json
CODE:
```
[
  {
    "id": "{string}",
    "code": "{string}",
    "type": "code_interpreter_call",
    "status": "{string}",
    "container_id": "{string}",
    "results": [
      {
        "type": "logs",
        "logs": "{string}"
      },
      {
        "type": "files",
        "files": [
          {
            "file_id": "{string}",
            "mime_type": "{string}"
          }
        ]
      }
    ]
  }
]
```

--------------------------------

TITLE: View GAIA Evaluation Results
DESCRIPTION: Launches the GAIA result viewer using `uv`. This command allows users to inspect the results of a completed GAIA evaluation, with an option for detailed output.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/gaia/README.md

LANGUAGE: bash
CODE:
```
uv run gaia_viewer "gaia_results_<timestamp>.jsonl" --detailed
```

--------------------------------

TITLE: Microsoft Fabric Data Agent Tool
DESCRIPTION: Defines the API request structure for the Microsoft Fabric data agent tool, specifying connection details for data operations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Microsoft Fabric Data Agent Tool

### Description
This tool allows agents to interact with Microsoft Fabric data sources. It is defined using the `fabric_dataagent` tool type and requires specifying connection details.

### Method
POST

### Endpoint
Not specified (Tool usage within an agent message)

### Parameters
#### Request Body
- **tools** (array) - Required - A list of available tools for the agent.
  - **type** (string) - Required - The type of tool, e.g., `fabric_dataagent`.
  - **fabric_dataagent** (object) - Configuration for the Fabric data agent.
    - **connections** (array) - Required - A list of connection configurations.
      - **connection_id** (string) - Required - The identifier for the Fabric connection.

### Request Example
```json
{
  "tools": [
    {
      "type": "fabric_dataagent",
      "fabric_dataagent": {
        "connections": [
          {
            "connection_id": "{string}"
          }
        ]
      }
    }
  ]
}
```

### Response
#### Success Response (200)
Tool Call Response: Not specified in the documentation.
```

--------------------------------

TITLE: Bash Example: Run Ray Cluster for Agent Training
DESCRIPTION: Starts a Ray cluster in head mode, which is necessary for distributed training of agents. This command is typically run before executing the training script.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
# Run the ray cluster (see the troubleshooting section for more details)
ray start --head --dashboard-host=0.0.0.0
```

--------------------------------

TITLE: Add Environment Helper to .csproj
DESCRIPTION: This XML snippet demonstrates how to add the `SampleHelpers.SampleEnvironment` class to a project's ItemGroup in the .csproj file. This enables the enhanced `GetEnvironmentVariable` method, which prompts the user for input if an environment variable is not found. No external dependencies are required beyond the Agent Framework.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/src/Shared/Demos/README.md

LANGUAGE: xml
CODE:
```
<ItemGroup>
  <Using Include="SampleHelpers.SampleEnvironment" Alias="Environment" />
</ItemGroup>

<ItemGroup>
  <Compile Include="$(MSBuildThisFileDirectory)\..\src\Shared\Demos\*.cs" LinkBase="" Visible="false" />
</ItemGroup>
```

--------------------------------

TITLE: Tool Call Response - Amazon Bedrock Agents
DESCRIPTION: Represents the response structure from Amazon Bedrock Agents for tool calls, including invocation details and parameters for executing actions.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "returnControl": {
    "invocationId": "{string}",
    "invocationInputs": [
      {
        "functionInvocationInput": {
          "actionGroup": "{string}",
          "actionInvocationType": "RESULT",
          "agentId": "{string}",
          "function": "{string}",
          "parameters": [
            {
              "name": "{string}",
              "type": "string",
              "value": "{string}"
            }
          ]
        }
      }
    ]
  }
}
```

--------------------------------

TITLE: Install Agent Framework Copilot Studio Package (Bash)
DESCRIPTION: This command installs the `agent-framework-copilotstudio` package using pip. The `--pre` flag is used to install pre-release versions of the package, which is necessary for accessing the latest features and integrations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/copilotstudio/README.md

LANGUAGE: bash
CODE:
```
pip install agent-framework-copilotstudio --pre
```

--------------------------------

TITLE: Build DevUI Frontend and Environment Setup (Bash)
DESCRIPTION: This snippet outlines the steps to set up, develop, and build the DevUI frontend using Yarn. It includes commands for installing dependencies, configuring API base URLs for development and production, and running the development server or building the project.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/frontend/README.md

LANGUAGE: bash
CODE:
```
cd frontend
yarn install

# Create .env.local with backend URL
echo 'VITE_API_BASE_URL=http://localhost:8000' > .env.local

# Create .env.production (empty for relative URLs)
echo '' > .env.production

# Development
yarn dev

# Build (copies to backend)
yarn build
```

--------------------------------

TITLE: Create Amazon Bedrock Agent Action Group with OpenAPI
DESCRIPTION: Defines an action group for an Amazon Bedrock Agent, specifying an OpenAPI specification as the payload. This allows the agent to expose functionality defined in an OpenAPI spec.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "apiSchema": {
    "payload": "{JSON or YAML OpenAPI specification string}"
  }
}
```

--------------------------------

TITLE: Install Optional Dependencies for Agent Framework Lab Lightning
DESCRIPTION: Installs optional dependencies for the agent-framework lab package with Lightning. The 'math' extra is for math-related training, and 'tau2' is for tau2 benchmarking. These installations are also in editable mode.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
# For math-related training
pip install -e ".[lightning,math]"

# For tau2 benchmarking
pip install -e ".[lightning,tau2]"
```

--------------------------------

TITLE: Troubleshooting Ray Connection Issues (Bash)
DESCRIPTION: This code block provides commands to stop existing Ray processes and then restart Ray with debugging enabled, which can help resolve connection issues during RL training with VERL.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
# Stop existing Ray processes
ray stop

# Start Ray with debugging enabled
env RAY_DEBUG=legacy HYDRA_FULL_ERROR=1 VLLM_USE_V1=1 ray start --head --dashboard-host=0.0.0.0
```

--------------------------------

TITLE: Install uv dependency manager
DESCRIPTION: These commands provide instructions for installing the `uv` dependency management tool across various operating systems. Choose the appropriate command based on your environment: Windows (non-WSL), WSL/Linux/MacOS via cURL, or MacOS via Homebrew.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: powershell
CODE:
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

LANGUAGE: bash
CODE:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

LANGUAGE: bash
CODE:
```
brew install uv
```

--------------------------------

TITLE: OpenAPI Spec Tool - Amazon Bedrock Agents
DESCRIPTION: Details on how Amazon Bedrock Agents use OpenAPI specifications for action groups.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Amazon Bedrock Agents - OpenAPI Spec Tool

### Description
This section outlines the request syntax for creating an action group with an OpenAPI specification in Amazon Bedrock Agents.

### Method
Not applicable (Configuration)

### Endpoint
Not applicable (Configuration)

### Parameters
#### Request Body
- **apiSchema** (object) - Required - Defines the schema for the API.
  - **payload** (string) - Required - The OpenAPI specification as a JSON or YAML string.

### Request Example
```json
{
  "apiSchema": {
    "payload": "{JSON or YAML OpenAPI specification string}"
  }
}
```

### Response
#### Success Response (200)
- **invocationInputs** (array) - Details for invoking the API.
  - **apiInvocationInput** (object) - Input details for the API invocation.
    - **actionGroup** (string) - The name of the action group.
    - **apiPath** (string) - The path of the API endpoint.
    - **httpMethod** (string) - The HTTP method for the API call.
    - **parameters** (array) - An array of parameters for the API call.
      - **name** (string) - The name of the parameter.
      - **type** (string) - The type of the parameter.
      - **value** (string) - The value of the parameter.

#### Response Example
```json
{
  "invocationInputs": [
    {
      "apiInvocationInput": {
        "actionGroup": "{string}",
        "apiPath": "{string}",
        "httpMethod": "{string}",
        "parameters": [
          {
            "name": "{string}",
            "type": "{string}",
            "value": "{string}"
          }
        ]
      }
    }
  ]
}
```
```

--------------------------------

TITLE: C# RunStreaming with Helper Methods for Primary Content
DESCRIPTION: Shows how to use only the `RunStreamingAsync` method and leverage extension methods to process the stream for primary content or full messages. This approach offers a single API for both streaming and non-streaming use cases, though it may be more complex for inexperienced users.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
// User can get the primary content through an extension method on the async enumerable stream.
var responses = agent.RunStreamingAsync("Do Something");
// E.g. an extension method that builds the primary content text.
Console.WriteLine(await responses.AggregateFinalResult());
// Or an extention method that builds complete messages from the updates.
Console.WriteLine(await responses.BuildMessage().Text);

// Callers can also iterate through all updates if needed
await foreach (var update in responses)
{
    Console.WriteLine(update.Contents.FirstOrDefault()?.GetType().Name);
}
```

--------------------------------

TITLE: Set Environment Variables for A2A Client
DESCRIPTION: PowerShell commands to configure essential environment variables for the A2A client. These include specifying the OpenAI model and API key, and providing a delimited list of agent URLs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/A2AClientServer/A2AClient/README.md

LANGUAGE: powershell
CODE:
```
cd dotnet/samples/A2AClientServer/A2AClient

$env:OPENAI_MODEL="gpt-4o-mini"
$env:OPENAI_API_KEY="<Your OPENAI api key>"
$env:AGENT_URLS="http://localhost:5000/policy;http://localhost:5000/invoice;http://localhost:5000/logistics"
```

--------------------------------

TITLE: Subpackage Naming Convention Example
DESCRIPTION: Provides examples of the recommended naming convention for subpackages, following the pattern '<vendor/folder>-<feature/brand>' or a simplified name for less complex vendors.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-python-subpackages.md

LANGUAGE: plaintext
CODE:
```
google-gemini
azure-purview
microsoft-copilotstudio
mem0
redis
```

--------------------------------

TITLE: Function Calling: Amazon Bedrock Agents (JSON)
DESCRIPTION: Shows the JSON syntax for creating an agent action group with Amazon Bedrock, including the function schema definition. It also presents the structure for tool call invocation inputs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "functionSchema": {
    "name": "{string}",
    "description": "{string}",
    "parameters": {
      "type": "{string | number | integer | boolean | array}",
      "description": "{string}",
      "required": "{boolean}"
    }
  }
}
```

LANGUAGE: json
CODE:
```
{
  "invocationInputs": [
    {
      "functionInvocationInput": {
        "actionGroup": "{string}",
        "function": "{string}",
        "parameters": [
          {
            "name": "{string}",
            "type": "{string | number | integer | boolean | array}",
            "value": {}
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: Configure A2A Agent URLs for Client (PowerShell)
DESCRIPTION: This PowerShell command sets an environment variable to specify the URLs of remote agents that the A2A client should connect to. Multiple agent URLs can be provided as a space-delimited string, allowing the client to interact with several services.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/A2AClientServer/README.md

LANGUAGE: powershell
CODE:
```
$env:A2A_AGENT_URLS="http://localhost:5000/;http://localhost:5001/;http://localhost:5002/"
```

--------------------------------

TITLE: Google Vertex AI Generative AI Tool Call Response
DESCRIPTION: Details the JSON response from Google Vertex AI after a tool call, including grounding metadata. This metadata contains web search queries, search entry points, grounding chunks with URIs and titles, and grounding supports with text segments and confidence scores.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "content": {
    "role": "model",
    "parts": [
      {
        "text": "{string}"
      }
    ]
  },
  "groundingMetadata": {
    "webSearchQueries": [
      "{string}"
    ],
    "searchEntryPoint": {
      "renderedContent": "{string}"
    },
    "groundingChunks": [
      {
        "web": {
          "uri": "{string}",
          "title": "{string}",
          "domain": "{string}"
        }
      }
    ],
    "groundingSupports": [
      {
        "segment": {
          "startIndex": "{number}",
          "endIndex": "{number}",
          "text": "{string}"
        },
        "groundingChunkIndices": [
          "{number}"
        ],
        "confidenceScores": [
          "{number}"
        ]
      }
    ],
    "retrievalMetadata": {}
  }
}
```

--------------------------------

TITLE: Non-Streaming Agent Invocation: Semantic Kernel vs. Agent Framework
DESCRIPTION: Demonstrates the difference in non-streaming agent invocation. Semantic Kernel uses `InvokeAsync` returning an `IAsyncEnumerable` of messages, while the Agent Framework uses `RunAsync` returning a single `AgentRunResponse` object containing all messages.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: csharp
CODE:
```
await foreach (AgentResponseItem<ChatMessageContent> result in agent.InvokeAsync(userInput, thread, agentOptions))
{
    Console.WriteLine(result.Message);
}
```

LANGUAGE: csharp
CODE:
```
AgentRunResponse agentResponse = await agent.RunAsync(userInput, thread);
```

--------------------------------

TITLE: Amazon Bedrock Agents Code Interpreter Action Group and Response
DESCRIPTION: Shows the JSON for enabling the CodeInterpreter action group in Amazon Bedrock Agents and the structure of a tool call response, including invocation input and observation details. The response contains execution results, potential errors, and metadata. .NET support is lacking specific SDK features.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "actionGroupName": "{string}",
  "parentActionGroupSignature": "AMAZON.CodeInterpreter",
  "actionGroupState": "ENABLED"
}
```

LANGUAGE: json
CODE:
```
{
  "trace": {
    "orchestrationTrace": {
      "invocationInput": {
        "invocationType": "ACTION_GROUP_CODE_INTERPRETER",
        "codeInterpreterInvocationInput": {
          "code": "{string}",
          "files": ["{string}"]
        }
      },
      "observation": {
        "codeInterpreterInvocationOutput": {
          "executionError": "{string}",
          "executionOutput": "{string}",
          "executionTimeout": "{boolean}",
          "files": ["{string}"],
          "metadata": {
            "clientRequestId": "{string}",
            "endTime": "{timestamp}",
            "operationTotalTimeMs": "{long}",
            "startTime": "{timestamp}",
            "totalTimeMs": "{long}",
            "usage": {
              "inputTokens": "{integer}",
              "outputTokens": "{integer}"
            }
          }
        }
      }
    }
  }
}
```

--------------------------------

TITLE: Run DevUI in In-Memory Mode (Bash)
DESCRIPTION: Navigates to the `packages/devui/samples` directory and executes `in_memory_mode.py`. This starts the DevUI with predefined agents for quick testing, automatically opening a browser to `http://localhost:8090`.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/dev.md

LANGUAGE: bash
CODE:
```
cd packages/devui/samples
python in_memory_mode.py
```

--------------------------------

TITLE: Amazon Bedrock Agents - Code Interpreter Integration
DESCRIPTION: This section details how to enable and interact with the Code Interpreter functionality within Amazon Bedrock Agents, including agent action group creation and tool call response structure.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Amazon Bedrock Agents - Code Interpreter Integration

### Description
This describes the process of enabling and using the Code Interpreter functionality with Amazon Bedrock Agents. It covers the request to create an action group for the code interpreter and the structure of the tool call responses.

### Method
POST (for CreateAgentActionGroup)

### Endpoint
`/agents/{agentId}/actionGroups` (implied endpoint for action group creation)

### Parameters
#### Request Body (CreateAgentActionGroup)
- **actionGroupName** (string) - Required - The name for the action group.
- **parentActionGroupSignature** (string) - Required - Must be 'AMAZON.CodeInterpreter'.
- **actionGroupState** (string) - Required - State of the action group, e.g., 'ENABLED'.

### Response
#### Success Response (200 OK) (Tool Call Response)
- **trace** (object) - Contains trace information about the orchestration.
  - **orchestrationTrace** (object) - Details of the orchestration.
    - **invocationInput** (object) - The input used for invocation.
      - **invocationType** (string) - Type of invocation, 'ACTION_GROUP_CODE_INTERPRETER'.
      - **codeInterpreterInvocationInput** (object) - Input specific to the code interpreter.
        - **code** (string) - The code to be executed.
        - **files** (array of strings) - File IDs to be used in execution.
    - **observation** (object) - The observation from the tool execution.
      - **codeInterpreterInvocationOutput** (object) - Output from the code interpreter.
        - **executionError** (string) - (Optional) Any error during execution.
        - **executionOutput** (string) - (Optional) The standard output of the execution.
        - **executionTimeout** (boolean) - (Optional) Indicates if execution timed out.
        - **files** (array of strings) - (Optional) File IDs generated during execution.
        - **metadata** (object) - Metadata about the execution.
          - **clientRequestId** (string) - Unique ID for the client request.
          - **endTime** (timestamp) - End time of the operation.
          - **operationTotalTimeMs** (long) - Total time for the operation in milliseconds.
          - **startTime** (timestamp) - Start time of the operation.
          - **totalTimeMs** (long) - Total time spent in milliseconds.
          - **usage** (object) - Token usage details.
            - **inputTokens** (integer) - Number of input tokens.
            - **outputTokens** (integer) - Number of output tokens.

### Request Example (CreateAgentActionGroup)
```json
{
  "actionGroupName": "{string}",
  "parentActionGroupSignature": "AMAZON.CodeInterpreter",
  "actionGroupState": "ENABLED"
}
```

### Response Example (Tool Call Response)
```json
{
  "trace": {
    "orchestrationTrace": {
      "invocationInput": {
        "invocationType": "ACTION_GROUP_CODE_INTERPRETER",
        "codeInterpreterInvocationInput": {
          "code": "{string}",
          "files": ["{string}"]
        }
      },
      "observation": {
        "codeInterpreterInvocationOutput": {
          "executionError": "{string}",
          "executionOutput": "{string}",
          "executionTimeout": {boolean},
          "files": ["{string}"],
          "metadata": {
            "clientRequestId": "{string}",
            "endTime": "{timestamp}",
            "operationTotalTimeMs": {long},
            "startTime": "{timestamp}",
            "totalTimeMs": {long},
            "usage": {
              "inputTokens": {integer},
              "outputTokens": {integer}
            }
          }
        }
      }
    }
  }
}
```
```

--------------------------------

TITLE: Manage Persistent Agent Conversations by Serializing Threads (.NET)
DESCRIPTION: This C# example illustrates how to achieve conversation persistence by serializing and deserializing `AgentThread` objects. It demonstrates how to save the state of a conversation thread to a file (or any storage) as JSON and then restore it to continue an interaction with the agent. This method allows agents to remember context across application lifecycles.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/context7.md

LANGUAGE: csharp
CODE:
```
using System.Text.Json;
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;
using OpenAI;

var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
var deploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? "gpt-4o-mini";

// Create agent
AIAgent agent = new AzureOpenAIClient(
    new Uri(endpoint),
    new AzureCliCredential())
    .GetChatClient(deploymentName)
    .CreateAIAgent(
        instructions: "You are good at telling jokes.",
        name: "Joker");

// Start conversation with thread
AgentThread thread = agent.GetNewThread();
Console.WriteLine(await agent.RunAsync("Tell me a joke about a pirate.", thread));

// Serialize thread to JSON
JsonElement serializedThread = thread.Serialize();
string tempFilePath = Path.GetTempFileName();
await File.WriteAllTextAsync(tempFilePath, JsonSerializer.Serialize(serializedThread));

// Load and deserialize thread
JsonElement reloadedSerializedThread = JsonSerializer.Deserialize<JsonElement>(
    await File.ReadAllTextAsync(tempFilePath)
);
AgentThread resumedThread = agent.DeserializeThread(reloadedSerializedThread);

// Continue conversation with restored context
Console.WriteLine(await agent.RunAsync(
    "Now tell the same joke in the voice of a pirate, and add some emojis.",
    resumedThread
));
```

--------------------------------

TITLE: Run Agent Middleware Sample (PowerShell)
DESCRIPTION: This snippet demonstrates how to navigate to the Agent Middleware sample directory and execute the sample using the .NET CLI. It assumes the .NET SDK is installed.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/Agents/Agent_Step14_Middleware/README.md

LANGUAGE: powershell
CODE:
```
cd dotnet/samples/GettingStarted/Agents/Agent_Step14_Middleware
dotnet run
```

--------------------------------

TITLE: C# Agent and Response Type Definitions
DESCRIPTION: Defines abstract base classes for `Agent`, `AgentRunResponse`, and `AgentRunResponseUpdate`. This demonstrates a design where custom response types extend existing Microsoft.SemanticKernel types, providing familiarity for users already employing MEAI but limiting independent evolution of agent response types.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
class Agent
{
    public abstract Task<AgentRunResponse> RunAsync(
        IReadOnlyCollection<ChatMessage> messages,
        AgentThread? thread = null,
        AgentRunOptions? options = null,
        CancellationToken cancellationToken = default);

    public abstract IAsyncEnumerable<AgentRunResponseUpdate> RunStreamingAsync(
        IReadOnlyCollection<ChatMessage> messages,
        AgentThread? thread = null,
        AgentRunOptions? options = null,
        CancellationToken cancellationToken = default);
}

class AgentRunResponse : ChatResponse
{
}

public class AgentRunResponseUpdate : ChatResponseUpdate
{
}
```

--------------------------------

TITLE: OpenAI Responses API - Function Calling
DESCRIPTION: Documentation for function calling using the OpenAI Responses API mode, detailing request and response structures.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## OpenAI Responses API - Function Calling

### Description
This section covers function calling within the OpenAI Responses API mode, outlining the request and tool call response formats.

### Method
Not specified (details provided for request/response bodies)

### Endpoint
Not specified

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools available to the model.
  - **type** (string) - Required - Must be "function".
  - **description** (string) - Required - A natural language description of what the function does.
  - **name** (string) - Required - The name of the function.
  - **parameters** (object) - Required - The parameters the function expects, represented as a JSON Schema object.

### Request Example
```json
{
  "tools": [
    {
      "type": "function",
      "description": "{string}",
      "name": "{string}",
      "parameters": "{JSON Schema object}"
    }
  ]
}
```

### Response
#### Tool Call Response
- **id** (string) - The ID of the tool call.
- **call_id** (string) - The identifier for the call.
- **type** (string) - Must be "function_call".
- **name** (string) - The name of the function to call.
- **arguments** (object) - The arguments to pass to the function, in JSON format.

#### Response Example
```json
[
  {
    "id": "{string}",
    "call_id": "{string}",
    "type": "function_call",
    "name": "{string}",
    "arguments": "{JSON object}"
  }
]
```
```

--------------------------------

TITLE: Amazon Bedrock Agent Tool Call Response
DESCRIPTION: Illustrates the structure of a tool call response from an Amazon Bedrock Agent. This response contains invocation inputs, including action group details, API path, HTTP method, and parameters.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "invocationInputs": [
    {
      "apiInvocationInput": {
        "actionGroup": "{string}",
        "apiPath": "{string}",
        "httpMethod": "{string}",
        "parameters": [
          {
            "name": "{string}",
            "type": "{string}",
            "value": "{string}"
          }
        ]
      }
    }
  ]
}
```

--------------------------------

TITLE: Run Ollama Docker Container (GPU)
DESCRIPTION: This command initiates an Ollama Docker container, enabling GPU acceleration. It requires NVIDIA drivers and Docker with GPU support configured. It maps a local volume for data and exposes the Ollama port.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_Ollama/README.md

LANGUAGE: powershell
CODE:
```
docker run -d --gpus=all -v "c:\temp\ollama:/root/.ollama" -p 11434:11434 --name ollama ollama/ollama
```

--------------------------------

TITLE: Agent Framework Project Directory Structure
DESCRIPTION: Illustrates the hierarchical directory and file structure of the `agent_framework` project. It categorizes components into Tiers (0, 1, 2) to show core, general, and vendor-specific modules, highlighting the organized package layout.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: plaintext
CODE:
```
agent_framework/
├── __init__.py              # Tier 0: Core components
├── _agents.py              # Agent implementations
├── _tools.py               # Tool definitions
├── _models.py              # Type definitions
├── _logging.py             # Logging utilities
├── context_providers.py    # Tier 1: Context providers
├── guardrails.py          # Tier 1: Guardrails and filters
├── vector_data.py         # Tier 1: Vector stores
├── workflows.py           # Tier 1: Multi-agent orchestration
└── azure/                 # Tier 2: Azure connectors (lazy loaded)
    └── __init__.py        # Imports from agent-framework-azure
```

--------------------------------

TITLE: Sample Output from A2A Client Interaction (Console)
DESCRIPTION: This console output demonstrates a typical interaction with the A2A client, showing agent initialization, user input, and the agent's processed response. It illustrates how the client integrates information from various remote agents to provide a comprehensive answer.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/A2AClientServer/README.md

LANGUAGE: console
CODE:
```
A2AClient> dotnet run
info: HostClientAgent[0]
      Initializing Agent Framework agent with model: gpt-4o-mini

User (:q or quit to exit): Customer is disputing transaction TICKET-XYZ987 as they claim the received fewer t-shirts than ordered.

Agent:

Agent:

Agent: The transaction details for **TICKET-XYZ987** are as follows:

- **Invoice ID:** INV789
- **Company Name:** Contoso
- **Invoice Date:** September 4, 2025
- **Products:**
  - **T-Shirts:** 150 units at $10.00 each
  - **Hats:** 200 units at $15.00 each
  - **Glasses:** 300 units at $5.00 each

To proceed with the dispute regarding the quantity of t-shirts delivered, please specify the exact quantity issue \u2013 how many t-shirts were actually received compared to the ordered amount.
```

--------------------------------

TITLE: AWS Bedrock - Knowledge Base Lookup
DESCRIPTION: This section describes the API for performing knowledge base lookups using AWS Bedrock, outlining the request structure for invocation and the response format detailing retrieved references.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /knowledgeBases/{knowledgeBaseId}/retrieve

### Description
This endpoint retrieves information from a specified knowledge base using AWS Bedrock.

### Method
POST

### Endpoint
`/knowledgeBases/{knowledgeBaseId}/retrieve`

### Parameters
#### Path Parameters
- **knowledgeBaseId** (string) - Required - The ID of the knowledge base to query.

#### Request Body
- **text** (string) - Required - The text query to perform against the knowledge base.
- **retrievalConfiguration** (object) - Optional - Configuration for retrieval.
  - **vectorSearchConfiguration** (object) - Configuration for vector search.
    - **numberOfResults** (number) - Optional - The number of results to return.
  - **rerankingConfiguration** (object) - Optional - Configuration for reranking results.
    - **bedrockRerankingConfiguration** (object) - Bedrock-specific reranking configuration.
      - **modelConfiguration** (object) - Configuration for the reranking model.
        - **modelArn** (string) - Required - The ARN of the reranking model.
      - **numberOfRerankedResults** (number) - Optional - The number of results to rerank.

### Request Example
```json
{
  "text": "What are the main features of the product?",
  "retrievalConfiguration": {
    "vectorSearchConfiguration": {
      "numberOfResults": 5
    },
    "rerankingConfiguration": {
      "bedrockRerankingConfiguration": {
        "modelConfiguration": {
          "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/cohere-rerank-english-v1:0"
        },
        "numberOfRerankedResults": 3
      }
    }
  }
}
```

### Response
#### Success Response (200)
- **retrievedReferences** (array) - A list of retrieved references.
  - **content** (object) - The content of the reference.
    - **text** (string) - The text content.
    - **type** (string) - The type of content (e.g., TEXT, IMAGE, ROW).
    - **row** (array) - If type is ROW, details about the row.
      - **columnName** (string) - The name of the column.
      - **columnValue** (string) - The value of the column.
      - **type** (string) - The data type of the column value.
  - **metadata** (object) - Metadata associated with the reference.

#### Response Example
```json
{
  "retrievedReferences": [
    {
      "content": {
        "type": "TEXT",
        "text": "The product features include A, B, and C."
      },
      "metadata": {
        "source": "document.pdf",
        "page": 5
      }
    }
  ]
}
```
```

--------------------------------

TITLE: Run Agent with Specific Output Type (C#)
DESCRIPTION: Demonstrates how to run an agent and expect the result to be deserialized into a specific type, like an array of Movie objects. This approach assumes the agent supports requesting a schema at invocation time.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
class Movie
{
    public string Title { get; set; }
    public string DirectorFullName { get; set; }
    public int ReleaseYear { get; set; }
}

AgentRunResponse<Movie[]> response = agent.RunAsync<Movie[]>("What are the top 3 children's movies of the 80s.");
Movie[] movies = response.Result
```

--------------------------------

TITLE: Injecting Provider-Specific Tools with RawRepresentationFactory
DESCRIPTION: This C# code snippet demonstrates how to use `ChatOptions.RawRepresentationFactory` to inject provider-specific tools into the AI chat options. This approach leverages existing functionality and is flexible for integrating tools from any AI provider without modifying the base `AITool` class, but requires a separate registration mechanism and can reduce abstraction.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: csharp
CODE:
```
ChatOptions options = new() {
    RawRepresentationFactory = _ => new ResponseCreationOptions() {
        Tools = { ... }, // backend-specific tools
    },
};
```

--------------------------------

TITLE: RunAsync with Primary Content and Streaming Primary Content
DESCRIPTION: Demonstrates how to retrieve the primary content from a non-streaming 'RunAsync' call and how to stream primary content using 'RunStreamingAsync'. It assumes that 'TextContent', 'DataContent', and 'UriContent' are designated as primary content, and secondary content does not use 'TextContent'. The 'ChatResponse.Text' property aggregates all 'TextContent' from messages.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
var response = await agent.RunAsync("Do Something");
Console.WriteLine(response.Text);

// Callers can still get access to all updates too.
foreach (var update in response.Messages)
{
    Console.WriteLine(update.Contents.FirstOrDefault()?.GetType().Name);
}

// For streaming, it's possible to output the primary content by also using the Text property on each update.
await foreach (var update in agent.RunStreamingAsync("Do Something"))
{
    Console.Writeline(update.Text)
}
```

--------------------------------

TITLE: Create and Orchestrate AI Agents with C#
DESCRIPTION: This C# code snippet demonstrates how to use the Foundry SDK to create AI agents (Analyst, Copywriter, Editor) and then orchestrate them sequentially using the Agent Framework SDK. It includes agent definition, input processing, orchestration execution, and agent cleanup.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/specs/001-foundry-sdk-alignment.md

LANGUAGE: csharp
CODE:
```
var persistentAgentsClient = new PersistentAgentsClient(
    TestConfiguration.AzureAI.Endpoint, new AzureCliCredential());
var model = TestConfiguration.OpenAI.ChatModelId;

AIAgent analystAgent =
    await persistentAgentsClient.CreateAIAgentAsync(
        model,
        name: "Analyst",
        instructions:
        """
        You are a marketing analyst. Given a product description, identify:
        - Key features
        - Target audience
        - Unique selling points
        """,
        description: "An agent that extracts key concepts from a product description.");
AIAgent writerAgent =
    await persistentAgentsClient.CreateAIAgentAsync(
        model,
        name: "copywriter",
        instructions:
        """
        You are a marketing copywriter. Given a block of text describing features, audience, and USPs,
        compose a compelling marketing copy (like a newsletter section) that highlights these points.
        Output should be short (around 150 words), output just the copy as a single text block.
        """,
        description: "An agent that writes a marketing copy based on the extracted concepts.");
AIAgent editorAgent =
    await persistentAgentsClient.CreateAIAgentAsync(
        model,
        name: "editor",
        instructions:
        """
        You are an editor. Given the draft copy, correct grammar, improve clarity, ensure consistent tone,
        give format and make it polished. Output the final improved copy as a single text block.
        """,
        description: "An agent that formats and proofreads the marketing copy.");

SequentialOrchestration orchestration =
    new(analystAgent, writerAgent, editorAgent)
    {
        LoggerFactory = this.LoggerFactory,
    };

string input = "An eco-friendly stainless steel water bottle that keeps drinks cold for 24 hours";
Console.WriteLine($"\n# INPUT: {input}\n");
AgentRunResponse result = await orchestration.RunAsync(input);
Console.WriteLine($"\n# RESULT: {result}");

await persistentAgentsClient.Administration.DeleteAgentAsync(analystAgent.Id);
await persistentAgentsClient.Administration.DeleteAgentAsync(writerAgent.Id);
await persistentAgentsClient.Administration.DeleteAgentAsync(editorAgent.Id);
```

--------------------------------

TITLE: C# Run Streaming with Primary and Secondary Updates
DESCRIPTION: Demonstrates running an agent and accessing both the primary text content and all intermediate secondary updates. Useful for non-streaming scenarios where clear separation of content and updates is desired. This pattern aligns with SDKs like AutoGen and OpenAI.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
// Since text contains the primary content, it's a good getting started experience.
var response = await agent.RunAsync("Do Something");
Console.WriteLine(response.Text);

// Callers can still get access to all updates too.
foreach (var update in response.Updates)
{
    Console.WriteLine(update.Contents.FirstOrDefault()?.GetType().Name);
}
```

--------------------------------

TITLE: OpenAI Image Generation Tool Definition (JSON)
DESCRIPTION: Defines an image generation tool for OpenAI's API. The message request specifies the tool type, and the tool call response includes details about the generated image, such as its ID, base64 result, and status.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "image_generation"
    }
  ]
}
```

LANGUAGE: json
CODE:
```
{
  "output": [
    {
      "type": "image_generation_call",
      "id": "{string}",
      "result": "{Base64 string}",
      "status": "{string}"
    }
  ]
}
```

--------------------------------

TITLE: CreateAgentActionGroup Request - Amazon Bedrock Agents
DESCRIPTION: Specifies the request format for creating an action group in Amazon Bedrock Agents, with a focus on enabling computer use capabilities.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "actionGroupName": "{string}",
  "parentActionGroupSignature": "ANTHROPIC.Computer",
  "actionGroupState": "ENABLED"
}
```

--------------------------------

TITLE: Function Calling: OpenAI Responses API (JSON)
DESCRIPTION: Details the JSON format for function calling using the OpenAI Responses API. This format differs slightly, particularly in the 'type' field for tool calls and the inclusion of 'call_id'.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "function",
      "description": "{string}",
      "name": "{string}",
      "parameters": "{JSON Schema object}"
    }
  ]
}
```

LANGUAGE: json
CODE:
```
[
  {
    "id": "{string}",
    "call_id": "{string}",
    "type": "function_call",
    "name": "{string}",
    "arguments": "{JSON object}"
  }
]
```

--------------------------------

TITLE: Streaming Agent Invocation: Semantic Kernel vs. Agent Framework
DESCRIPTION: Illustrates agent invocation with streaming enabled. Semantic Kernel's `InvokeStreamingAsync` yields `StreamingChatMessageContent`, whereas the Agent Framework's `RunStreamingAsync` returns `AgentRunResponseUpdate` objects, providing more detailed agent-specific information per update.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: csharp
CODE:
```
await foreach (StreamingChatMessageContent update in agent.InvokeStreamingAsync(userInput, thread))
{
    Console.Write(update);
}
```

LANGUAGE: csharp
CODE:
```
await foreach (AgentRunResponseUpdate update in agent.RunStreamingAsync(userInput, thread))
{
    Console.Write(update); // Update is ToString() friendly
}
```

--------------------------------

TITLE: RunAsync with Optional Secondary Content Inclusion
DESCRIPTION: Illustrates how to optionally include secondary content in the response messages for the 'RunAsync' method. By default, the response contains only primary content. An option can be used to include updates, allowing access to all messages.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
// By default the response only has the primary content, so text
// contains the primary content, and it's a good starting experience.
var response = await agent.RunAsync("Do Something");
Console.WriteLine(response.Text);

// we can also optionally include updates via an option.
var response = await agent.RunAsync("Do Something", options: new() { IncludeUpdates = true });
// Callers can now access all updates.
foreach (var update in response.Messages)
{
    Console.WriteLine(update.Contents.FirstOrDefault()?.GetType().Name);
}
```

--------------------------------

TITLE: Set OpenAI API Key Environment Variable (PowerShell)
DESCRIPTION: Shows how to set the OPENAI_API_KEY environment variable using PowerShell. This key is essential for authenticating requests to the OpenAI API, including services like OpenAI Assistants. It's a common prerequisite for running OpenAI-related samples.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: powershell
CODE:
```
$env:OPENAI_API_KEY = "sk-..."
```

--------------------------------

TITLE: Google Vertex AI Grounding Message Request and Response
DESCRIPTION: This snippet shows the JSON structure for sending a message request to Google Vertex AI that includes retrieval capabilities via Vertex AI Search. It also details the response, including grounding metadata such as retrieval queries and supported segments.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "{string}"
        }
      ]
    }
  ],
  "tools": [
    {
      "retrieval": {
        "vertexAiSearch": {
          "datastore": "{string}"
        }
      }
    }
  ]
}

```

LANGUAGE: json
CODE:
```
{
  "content": {
    "role": "model",
    "parts": [
      {
        "text": "{string}"
      }
    ]
  },
  "groundingMetadata": {
    "retrievalQueries": [
      "{string}"
    ],
    "groundingChunks": [
      {
        "retrievedContext": {
          "uri": "{string}",
          "title": "{string}"
        }
      }
    ],
    "groundingSupport": [
      {
        "segment": {
          "startIndex": "{number}",
          "endIndex": "{number}"
        },
        "segment_text": "{string}",
        "supportChunkIndices": ["{number}"],
        "confidenceScore": ["{number}"]
      }
    ]
  }
}

```

--------------------------------

TITLE: Clone ONNX Model Repository
DESCRIPTION: This command clones the ONNX model repository from Hugging Face using git. Ensure you have git installed and configured.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_ONNX/README.md

LANGUAGE: powershell
CODE:
```
git clone https://huggingface.co/microsoft/Phi-4-mini-instruct-onnx
```

--------------------------------

TITLE: Google Vertex AI - Grounding
DESCRIPTION: This section outlines the API for grounding responses using Google Vertex AI Search, detailing the message request format and the structure of the tool call response including grounding metadata.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /models/{model}:generateContent

### Description
This endpoint generates content using a specified model in Google Vertex AI, with support for grounding via Vertex AI Search.

### Method
POST

### Endpoint
`/models/{model}:generateContent`

### Parameters
#### Path Parameters
- **model** (string) - Required - The name of the model to use (e.g., "gemini-pro").

#### Request Body
- **contents** (array) - Required - An array of content objects representing the conversation.
  - **role** (string) - Required - The role of the author ('user' or 'model').
  - **parts** (array) - Required - An array of content parts.
    - **text** (string) - Required - The text content.
- **tools** (array) - Optional - A list of tools to enable.
  - **retrieval** (object) - Configuration for retrieval tool.
    - **vertexAiSearch** (object) - Configuration for Vertex AI Search.
      - **datastore** (string) - Required - The ID of the Vertex AI Search datastore.

### Request Example
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Explain the concept of grounding in AI."
        }
      ]
    }
  ],
  "tools": [
    {
      "retrieval": {
        "vertexAiSearch": {
          "datastore": "my-vertex-ai-datastore-id"
        }
      }
    }
  ]
}
```

### Response
#### Success Response (200)
- **content** (object) - The generated content.
  - **role** (string) - The role of the author ('model').
  - **parts** (array) - An array of content parts.
    - **text** (string) - The generated text.
- **groundingMetadata** (object) - Metadata related to grounding.
  - **groundingChunks** (array) - Chunks of retrieved content used for grounding.
    - **retrievedContext** (object) - Context of the retrieved chunk.
      - **uri** (string) - The URI of the source document.
      - **title** (string) - The title of the source document.
  - **groundingSupport** (array) - Support segments used for grounding.
    - **segment_text** (string) - The text of the grounded segment.
    - **startIndex** (number) - The start index of the segment.
    - **endIndex** (number) - The end index of the segment.

#### Response Example
```json
{
  "content": {
    "role": "model",
    "parts": [
      {
        "text": "Grounding in AI refers to the process of connecting a model's output to specific external information sources to ensure factual accuracy and reduce hallucinations."
      }
    ]
  },
  "groundingMetadata": {
    "groundingChunks": [
      {
        "retrievedContext": {
          "uri": "gs://my-bucket/documents/grounding_paper.pdf",
          "title": "Understanding Grounding in AI Models"
        }
      }
    ],
    "groundingSupport": [
      {
        "segment_text": "...connecting a model's output to specific external information sources...",
        "startIndex": 500,
        "endIndex": 550
      }
    ]
  }
}
```
```

--------------------------------

TITLE: Computer Use Tool Request - OpenAI
DESCRIPTION: Defines the structure for requesting computer use capabilities from OpenAI's API. It specifies the tool type and environment details for interaction.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "computer_use_preview",
      "display_width": "{number}",
      "display_height": "{number}",
      "environment": "{browser | mac | windows | ubuntu}"
    }
  ]
}
```

--------------------------------

TITLE: Create and Run Agent with Conversation State using Foundry SDK and Agent Framework (C#)
DESCRIPTION: This snippet illustrates creating an AIAgent using the Foundry SDK, managing conversation state with an AgentThread, and running the agent within that thread using the Agent Framework SDK. It includes cleanup for both the agent and the thread.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/specs/001-foundry-sdk-alignment.md

LANGUAGE: csharp
CODE:
```
// Get a client to create server side agents with.
var persistentAgentsClient = new PersistentAgentsClient(
    TestConfiguration.AzureAI.Endpoint, new AzureCliCredential());

// Create an Agent Framework agent.
AIAgent agent = await persistentAgentsClient.CreateAIAgentAsync(
    model: TestConfiguration.AzureAI.DeploymentName!,
    name: JokerName,
    instructions: JokerInstructions);

// Start a new thread for the agent conversation.
AgentThread thread = agent.GetNewThread();

// Respond to user input.
await RunAgentAsync("Tell me a joke about a pirate.");
await RunAgentAsync("Now add some emojis to the joke.");

// Local function to run agent and display the conversation messages for the thread.
async Task RunAgentAsync(string input)
{
    Console.WriteLine(
        $"""
User: {input}
Assistant:
{await agent.RunAsync(input, thread)}

""");
}

// Cleanup
await persistentAgentsClient.Threads.DeleteThreadAsync(thread.ConversationId);
await persistentAgentsClient.Administration.DeleteAgentAsync(agent.Id);
```

--------------------------------

TITLE: OpenAI Assistant API - Function Calling
DESCRIPTION: Documentation for function calling within the OpenAI Assistant API, detailing the structure of message requests and tool call responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## OpenAI Assistant API - Function Calling

### Description
This section outlines the structure for defining tools and handling tool calls when using the OpenAI Assistant API.

### Method
Not specified (details provided for request/response bodies)

### Endpoint
Not specified

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools available to the assistant.
  - **type** (string) - Required - Must be "function".
  - **function** (object) - Required - Describes the function.
    - **description** (string) - Optional - A natural language description of the function's purpose.
    - **name** (string) - Required - The name of the function.
    - **parameters** (object) - Required - The parameters the function expects, represented as a JSON Schema object.

### Request Example
```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "description": "{string}",
        "name": "{string}",
        "parameters": "{JSON Schema object}"
      }
    }
  ]
}
```

### Response
#### Tool Call Response
- **tool_calls** (array) - Contains the tool calls made by the assistant.
  - **id** (string) - The ID of the tool call.
  - **type** (string) - Must be "function".
  - **function** (object) - Details of the function call.
    - **name** (string) - The name of the function to call.
    - **arguments** (object) - The arguments to pass to the function, in JSON format.

#### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "function",
      "function": {
        "name": "{string}",
        "arguments": "{JSON object}"
      }
    }
  ]
}
```
```

--------------------------------

TITLE: OpenAI Responses API - File Search Tool
DESCRIPTION: This endpoint describes the file search tool integration within the OpenAI Responses API, returning structured results for file search operations.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /responses/file_search

### Description
This endpoint utilizes the file search tool within the OpenAI Responses API. It takes vector store IDs and returns structured search results.

### Method
POST

### Endpoint
/responses/file_search

### Parameters
#### Request Body
- **tools** (array) - Required - List of tools to use, must include `{"type": "file_search"}`.
- **tool_resources** (object) - Required - Resources for the tools.
  - **file_search** (object) - Required - Configuration for file search.
    - **vector_store_ids** (array) - Required - IDs of the vector stores to use.

### Request Example
```json
{
  "tools": [
    {
      "type": "file_search"
    }
  ],
  "tool_resources": {
    "file_search": {
      "vector_store_ids": ["string"]
    }
  }
}
```

### Response
#### Success Response (200)
- **output** (array) - A list of file search call results.
  - **id** (string) - Unique identifier for the search call.
  - **queries** (array) - The queries that were performed.
  - **status** (string) - The status of the search call (e.g., "in_progress", "completed", "failed").
  - **type** (string) - The type of the call, expected to be "file_search_call".
  - **results** (array) - List of search results.
    - **attributes** (object) - Additional attributes for the result.
    - **file_id** (string) - ID of the file.
    - **filename** (string) - Name of the file.
    - **score** (float) - Relevance score of the result.
    - **text** (string) - The extracted text content.

#### Response Example
```json
{
  "output": [
    {
      "id": "{string}",
      "queries": ["{string}"],
      "status": "completed",
      "type": "file_search_call",
      "results": [
        {
          "attributes": {},
          "file_id": "{string}",
          "filename": "{string}",
          "score": "{float}",
          "text": "{string}"
        }
      ]
    }
  ]
}
```
```

--------------------------------

TITLE: Anthropic Text Editor Tool Definition (JSON)
DESCRIPTION: Defines a text editor tool for Anthropic's API, specifying its type and a name for string replacement-based edits. It includes a sample tool call response with command and path inputs.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "text_editor_20250429",
      "name": "str_replace_based_edit_tool"
    }
  ]
}
```

LANGUAGE: json
CODE:
```
{
  "role": "assistant",
  "content": [
    {
      "type": "tool_use",
      "id": "{string}",
      "name": "str_replace_based_edit_tool",
      "input": {
        "command": "{string}",
        "path": "{string}"
      }
    }
  ]
}
```

--------------------------------

TITLE: Configure Type-Aware ESLint for TypeScript (JavaScript)
DESCRIPTION: This configuration snippet demonstrates how to enhance an ESLint setup with type-aware linting rules for TypeScript files using `@typescript-eslint/eslint-plugin`. It shows different levels of strictness (recommendedTypeChecked, strictTypeChecked, stylisticTypeChecked) and specifies `parserOptions` for project-wide type checking.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/frontend/README.md

LANGUAGE: js
CODE:
```
export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      ...tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      ...tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

--------------------------------

TITLE: Create and Run Agent Directly with Foundry SDK and Agent Framework (C#)
DESCRIPTION: This example shows how to directly create an AIAgent using the Foundry SDK, run it with the Agent Framework SDK, and then clean up the agent. This method bypasses the explicit creation of a persistent agent first.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/specs/001-foundry-sdk-alignment.md

LANGUAGE: csharp
CODE:
```
// Get a client to create server side agents with.
var persistentAgentsClient = new PersistentAgentsClient(
    TestConfiguration.AzureAI.Endpoint, new AzureCliCredential());

// Create a persistent agent and expose it as an Agent Framework agent.
AIAgent agent = await persistentAgentsClient.CreateAIAgentAsync(
    model: TestConfiguration.AzureAI.DeploymentName!,
    name: JokerName,
    instructions: JokerInstructions);

// Respond to user input.
var input = "Tell me a joke about a pirate.";
Console.WriteLine(input);
Console.WriteLine(await agent.RunAsync(input));

// Delete the persistent agent.
await persistentAgentsClient.Administration.DeleteAgentAsync(agent.Id);
```

--------------------------------

TITLE: Agent-Level Filtering with Middleware in C#
DESCRIPTION: Configures an AI agent to use middleware for function invocation filtering. It applies two middleware components: one to log streaming status and arguments, and another to log the city name from arguments. This demonstrates agent-level filtering using the .Use() pattern.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0007-agent-filtering-middleware.md

LANGUAGE: csharp
CODE:
```
var agent = persistentAgentsClient.CreateAIAgent(model)
    .AsBuilder()
    .Use((functionInvocationContext, next, ct) =>
    {
        Console.WriteLine($"IsStreaming: {functionInvocationContext!.IsStreaming}");
        return next(functionInvocationContext.Arguments, ct);
    })
    .Use((functionInvocationContext, next, ct) =>
    {
        Console.WriteLine($"City Name: {(functionInvocationContext!.Arguments.TryGetValue("location", out var location) ? location : "not provided")}");
        return next(functionInvocationContext.Arguments, ct);
    })
    .Build();
```

--------------------------------

TITLE: Update C# Namespaces for Agent Framework
DESCRIPTION: This snippet shows the updated namespace declarations required when migrating from Semantic Kernel to Agent Framework. Agent Framework uses `Microsoft.Agents.AI` and `Microsoft.Extensions.AI` for core AI message and content types.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: csharp
CODE:
```
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
```

LANGUAGE: csharp
CODE:
```
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;
```

--------------------------------

TITLE: Send Message to Agent using HTTP REST Client
DESCRIPTION: This HTTP POST request sends a JSON RPC message to an agent, typically used for initiating a conversation or submitting a task. The request body includes the message ID, sender role, and the content of the message, formatted as application/json.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/A2AClientServer/README.md

LANGUAGE: http
CODE:
```
POST {{hostInvoice}}
Content-Type: application/json

{
    "id": "1",
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
        "id": "12345",
        "message": {
            "kind": "message",
            "role": "user",
            "messageId": "msg_1",
            "parts": [
                {
                    "kind": "text",
                    "text": "Show me all invoices for Contoso?"
                }
            ]
        }
    }
}
```

--------------------------------

TITLE: Enable OpenTelemetry Tracing in DevUI (Bash)
DESCRIPTION: This command starts the DevUI server with OpenTelemetry tracing enabled for the framework. This allows users to view detailed traces for various operations performed by agents and workflows within the DevUI.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/devui/README.md

LANGUAGE: bash
CODE:
```
devui ./agents --tracing framework
```

--------------------------------

TITLE: Amazon Bedrock Agents - Create Agent Action Group
DESCRIPTION: Details the request syntax for creating an agent action group with the computer use capability in Amazon Bedrock.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /agents/{agentId}/actionGroups (Amazon Bedrock)

### Description
This endpoint is used to create or update an action group for an agent in Amazon Bedrock, specifying capabilities like computer use.

### Method
POST

### Endpoint
/agents/{agentId}/actionGroups

### Parameters
#### Path Parameters
- **agentId** (string) - Required - The unique identifier of the agent.

#### Request Body
- **actionGroupName** (string) - Required - The name of the action group.
- **parentActionGroupSignature** (string) - Required - The signature of the parent action group. For computer use, this is typically `"ANTHROPIC.Computer"`.
- **actionGroupState** (string) - Required - The state of the action group (e.g., `"ENABLED"`, `"DISABLED"`).

### Request Example
```json
{
  "actionGroupName": "ComputerActions",
  "parentActionGroupSignature": "ANTHROPIC.Computer",
  "actionGroupState": "ENABLED"
}
```

### Response
#### Success Response (200)
- **returnControl** (object) - Contains information for controlling the agent's interaction flow.
  - **invocationId** (string) - The unique identifier for this invocation.
  - **invocationInputs** (array) - A list of inputs for the function invocation.
    - **functionInvocationInput** (object) - Details of the function call.
      - **actionGroup** (string) - The name of the action group being invoked.
      - **actionInvocationType** (string) - The type of action invocation (e.g., `"RESULT"`).
      - **agentId** (string) - The ID of the agent.
      - **function** (string) - The name of the function to invoke.
      - **parameters** (array) - Parameters for the function call.
        - **name** (string) - The name of the parameter.
        - **type** (string) - The data type of the parameter.
        - **value** (string) - The value of the parameter.

#### Response Example
```json
{
  "returnControl": {
    "invocationId": "inv-123",
    "invocationInputs": [
      {
        "functionInvocationInput": {
          "actionGroup": "ComputerActions",
          "actionInvocationType": "RESULT",
          "agentId": "agent-abc",
          "function": "performAction",
          "parameters": [
            {
              "name": "actionType",
              "type": "string",
              "value": "click"
            },
            {
              "name": "elementSelector",
              "type": "string",
              "value": ".submit-button"
            }
          ]
        }
      }
    ]
  }
}
```
```

--------------------------------

TITLE: Create and Run an A2A AI Agent in C#
DESCRIPTION: This C# code snippet demonstrates how to create an A2A client, obtain an AI agent from it, and then run the agent with a specific prompt. It utilizes the A2A and Microsoft.Agents.AI libraries. The output of the agent's run is printed to the console.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_A2A/README.md

LANGUAGE: csharp
CODE:
```
using A2A;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.A2A;

// Create an A2AClient pointing to your `echo` A2A agent endpoint
A2AClient a2aClient = new(new Uri("https://your-a2a-agent-host/echo"));

// Create an AIAgent from the A2AClient
AIAgent agent = a2aClient.GetAIAgent();

// Run the agent
AgentRunResponse response = await agent.RunAsync("Tell me a joke about a pirate.");
Console.WriteLine(response);
```

--------------------------------

TITLE: Enable Agent Framework Debug Mode (PowerShell)
DESCRIPTION: Explains how to set the AF_SHOW_ALL_DEMO_SETTING_VALUES environment variable to 'Y' using PowerShell. This optional variable is used to enable a debug mode within the Agent Framework, which can be helpful for troubleshooting and understanding sample execution.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/SemanticKernelMigration/README.md

LANGUAGE: powershell
CODE:
```
$env:AF_SHOW_ALL_DEMO_SETTING_VALUES = "Y"
```

--------------------------------

TITLE: Set ONNX Model Path Environment Variable
DESCRIPTION: This command sets the ONNX_MODEL_PATH environment variable. Replace the example path with the actual path to your downloaded ONNX model. This is crucial for the agent framework to locate the model.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/GettingStarted/AgentProviders/Agent_With_ONNX/README.md

LANGUAGE: powershell
CODE:
```
$env:ONNX_MODEL_PATH="C:\repos\Phi-4-mini-instruct-onnx\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4" # Replace with your model path
```

--------------------------------

TITLE: Agent Long Running Process Support - Option 1
DESCRIPTION: Introduces an AgentRunContent class that inherits from AIContent and includes an AgentRunId property, designed for handling long-running agent processes. Additionally, it defines a static property `LongRunning` for the ChatFinishReason enumeration, indicating that a process is ongoing.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
public class AgentRunContent : AIContent
{
    public string AgentRunId { get; set; }
}

// Add a new long running chat finish reason.
public class ChatFinishReason
{
    public static ChatFinishReason LongRunning { get; } = new ChatFinishReason("long_running");
}
```

--------------------------------

TITLE: Parse Structured Output from Agent Response (C#)
DESCRIPTION: Shows how to extract a structured output from an agent's response if the agent has a built-in schema or if the schema was configured at construction time. This method attempts to parse the response into the specified type.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0001-agent-run-response.md

LANGUAGE: csharp
CODE:
```
AgentRunResponse response = agent.RunAsync("What are the top 3 children's movies of the 80s.");
Movie[] movies = response.TryParseStructuredOutput<Movie[]>();
```

--------------------------------

TITLE: Anthropic Code Execution Tool
DESCRIPTION: This section outlines the request and response format for using the code execution tool with Anthropic's models.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## Anthropic Code Execution Tool

### Description
This endpoint enables code execution through Anthropic's tools, allowing models to run code and return results.

### Method
POST

### Endpoint
/anthropic/tools/code-execution

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools to be used by the model.
  - **name** (string) - Required - The name of the tool, "code_execution".
  - **type** (string) - Required - The type of the tool, "code_execution_20250522".

### Request Example
```json
{
  "tools": [
    {
      "name": "code_execution",
      "type": "code_execution_20250522"
    }
  ]
}
```

### Response
#### Success Response (200)
- **role** (string) - Required - The role of the message sender (e.g., "assistant").
- **container** (object) - Information about the execution container.
  - **id** (string) - Required - The ID of the container.
  - **expires_at** (timestamp) - Required - The expiration time of the container.
- **content** (array) - Required - An array of content objects.
  - **type** (string) - Required - The type of content (e.g., "server_tool_use", "code_execution_tool_result").
  - **id** (string) - Required - The ID of the tool use.
  - **name** (string) - Required - The name of the tool used.
  - **input** (object) - The input provided to the tool.
    - **code** (string) - Required - The code to be executed.
  - **tool_use_id** (string) - Required - The ID of the tool use.
  - **content** (object) - The result of the code execution.
    - **type** (string) - Required - The type of the result (e.g., "code_execution_result").
    - **stdout** (string) - The standard output from the execution.
    - **stderr** (string) - The standard error from the execution.
    - **return_code** (integer) - The return code of the execution.

#### Response Example
```json
{
  "role": "assistant",
  "container": {
    "id": "cont-abcdef123456",
    "expires_at": "2024-01-01T12:00:00Z"
  },
  "content": [
    {
      "type": "server_tool_use",
      "id": "tu_xyz789",
      "name": "code_execution",
      "input": {
        "code": "print(\"Hello from Anthropic!\")"
      }
    },
    {
      "type": "code_execution_tool_result",
      "tool_use_id": "tu_xyz789",
      "content": {
        "type": "code_execution_result",
        "stdout": "Hello from Anthropic!\n",
        "stderr": null,
        "return_code": 0
      }
    }
  ]
}
```
```

--------------------------------

TITLE: OpenAI Image Generation Tool
DESCRIPTION: Details the API request and response structure for the OpenAI image generation tool, enabling agents to create images.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## OpenAI Image Generation Tool

### Description
This tool integrates with OpenAI's API to generate images based on agent prompts. It uses the `image_generation` tool type and provides a structured response containing the generated image data.

### Method
POST

### Endpoint
Not specified (Tool usage within an agent message)

### Parameters
#### Request Body
- **tools** (array) - Required - A list of available tools for the agent.
  - **type** (string) - Required - The type of tool, e.g., `image_generation`.

### Request Example
```json
{
  "tools": [
    {
      "type": "image_generation"
    }
  ]
}
```

### Response
#### Success Response (200)
- **output** (array) - A list of image generation results.
  - **type** (string) - The type of output, e.g., `image_generation_call`.
  - **id** (string) - A unique identifier for the image generation task.
  - **result** (string) - The generated image data, typically as a Base64 encoded string.
  - **status** (string) - The status of the image generation (e.g., 'succeeded', 'failed').

#### Response Example
```json
{
  "output": [
    {
      "type": "image_generation_call",
      "id": "{string}",
      "result": "{Base64 string}",
      "status": "{string}"
    }
  ]
}
```
```

--------------------------------

TITLE: OpenAI Responses API Web Search Message Request
DESCRIPTION: Defines the JSON message request for the OpenAI Responses API, enabling web search previews. It includes a list of tools and user input for the search query.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "web_search_preview"
    }
  ],
  "input": "{string}"
}
```

--------------------------------

TITLE: OpenAI ChatCompletion API - Function Calling
DESCRIPTION: Documentation for function calling with the OpenAI ChatCompletion API, specifying request and response formats.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## OpenAI ChatCompletion API - Function Calling

### Description
This section describes how to use function calling with the OpenAI ChatCompletion API, including request and response formats.

### Method
Not specified (details provided for request/response bodies)

### Endpoint
Not specified

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools available to the model.
  - **type** (string) - Required - Must be "function".
  - **function** (object) - Required - Describes the function.
    - **description** (string) - Optional - A natural language description of the function's purpose.
    - **name** (string) - Required - The name of the function.
    - **parameters** (object) - Required - The parameters the function expects, represented as a JSON Schema object.

### Request Example
```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "description": "{string}",
        "name": "{string}",
        "parameters": "{JSON Schema object}"
      }
    }
  ]
}
```

### Response
#### Tool Call Response
- **tool_calls** (array) - Contains the tool calls made by the model.
  - **id** (string) - The ID of the tool call.
  - **type** (string) - Must be "function".
  - **function** (object) - Details of the function call.
    - **name** (string) - The name of the function to call.
    - **arguments** (object) - The arguments to pass to the function, in JSON format.

#### Response Example
```json
[
  {
    "id": "{string}",
    "type": "function",
    "function": {
      "name": "{string}",
      "arguments": "{JSON object}"
    }
  }
]
```
```

--------------------------------

TITLE: Run Agent Training in Debug Mode (Bash)
DESCRIPTION: This command demonstrates how to run the training script in debug mode, which is useful for validating agent behavior, checking tool integration, and ensuring proper result extraction before full training.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/packages/lab/lightning/README.md

LANGUAGE: bash
CODE:
```
# Use debug mode to validate agent behavior
python your_training_script.py --debug
```

--------------------------------

TITLE: JSON: OpenAI Message Request for Remote MCP Tools
DESCRIPTION: Illustrates the JSON structure for an OpenAI message request that includes the configuration for remote MCP (Message Communication Protocol) servers. This allows agents to interact with external services.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: json
CODE:
```
{
  "tools": [
    {
      "type": "mcp",
      "server_label": "{string}",
      "server_url": "{string}",
      "require_approval": "{string}"
    }
  ]
}
```

--------------------------------

TITLE: OpenAI Responses API - Computer Use
DESCRIPTION: Details the request and response format for using the computer_use_preview tool with OpenAI's API.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## POST /v1/chat/completions (OpenAI)

### Description
This endpoint allows agents to interact with computer environments using the `computer_use_preview` tool. It defines the parameters for the tool and the structure of the response, including action details and status.

### Method
POST

### Endpoint
/v1/chat/completions

### Parameters
#### Request Body
- **tools** (array) - Required - A list of tools the agent can use. For computer use, this includes `type: "computer_use_preview"` with optional `display_width` and `display_height`, and `environment`.
  - **type** (string) - Required - Must be `"computer_use_preview"`.
  - **display_width** (number) - Optional - The width of the display in pixels.
  - **display_height** (number) - Optional - The height of the display in pixels.
  - **environment** (string) - Optional - The target environment (e.g., `"browser"`, `"mac"`, `"windows"`, `"ubuntu"`).

### Request Example
```json
{
  "tools": [
    {
      "type": "computer_use_preview",
      "display_width": 1920,
      "display_height": 1080,
      "environment": "browser"
    }
  ]
}
```

### Response
#### Success Response (200)
- **output** (array) - Contains details of the tool call result, including reasoning and executed computer actions.
  - **type** (string) - Type of the output item (e.g., `"reasoning"`, `"computer_call"`).
  - **id** (string) - Unique identifier for the output item.
  - **summary** (array) - For reasoning output, contains a summary text.
  - **call_id** (string) - For computer_call, the unique ID of the action call.
  - **action** (object) - Describes the computer action performed (e.g., `click`, `keypress`, `type`, `wait`).
  - **pending_safety_checks** (array) - List of pending safety checks.
  - **status** (string) - Status of the computer action (e.g., `"in_progress"`, `"completed"`, `"incomplete"`).

#### Response Example
```json
{
  "output": [
    {
      "type": "reasoning",
      "id": "reasoning-123",
      "summary": [
        {
          "type": "summary_text",
          "text": "The agent decided to click on the login button."
        }
      ]
    },
    {
      "type": "computer_call",
      "id": "call-456",
      "call_id": "action-abc",
      "action": {
        "type": "click",
        "element_selector": "#login-button"
      },
      "pending_safety_checks": [],
      "status": "completed"
    }
  ]
}
```
```

--------------------------------

TITLE: OpenAI Responses API - Code Interpreter
DESCRIPTION: This section outlines the Code Interpreter tool as used with the OpenAI Responses API, detailing the request body for tool specification and the structure of tool call responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## OpenAI Responses API - Code Interpreter

### Description
This describes the integration of the code interpreter tool within the OpenAI Responses API. It includes the request body format for enabling the tool and the structure of the tool call responses.

### Method
POST (implied, as part of a message request to the OpenAI API)

### Endpoint
Not explicitly defined, assumed to be part of the OpenAI API endpoint for message creation.

### Parameters
#### Request Body
- **tools** (array) - Required - Specifies the tools to be used, including 'code_interpreter'.
  - **type** (string) - Required - Must be 'code_interpreter'.
  - **container** (object) - Optional - Configuration for the execution container.
    - **type** (string) - Required - The type of container, e.g., 'auto'.

### Response
#### Success Response (200 OK)
- This response is an array of tool call results.
  - **id** (string) - Unique identifier for the tool call.
  - **code** (string) - The code that was executed.
  - **type** (string) - Type of the tool call result, 'code_interpreter_call'.
  - **status** (string) - The status of the execution (e.g., 'succeeded', 'failed').
  - **container_id** (string) - Identifier for the container that executed the code.
  - **results** (array of objects) - The outcomes of the code execution.
    - **type** (string) - Type of the result ('logs' or 'files').
    - **logs** (string) - (if type is 'logs') The execution logs.
    - **files** (array of objects) - (if type is 'files') Information about generated files.
      - **file_id** (string) - The ID of the generated file.
      - **mime_type** (string) - The MIME type of the file.

### Request Example
```json
{
  "tools": [
    {
      "type": "code_interpreter",
      "container": { "type": "auto" }
    }
  ]
}
```

### Response Example
```json
[
  {
    "id": "{string}",
    "code": "{string}",
    "type": "code_interpreter_call",
    "status": "{string}",
    "container_id": "{string}",
    "results": [
      {
        "type": "logs",
        "logs": "{string}"
      },
      {
        "type": "files",
        "files": [
          {
            "file_id": "{string}",
            "mime_type": "{string}"
          }
        ]
      }
    ]
  }
]
```
```

--------------------------------

TITLE: OpenAI Assistant API - Code Interpreter
DESCRIPTION: This section details the Code Interpreter tool as used with the OpenAI Assistant API, covering request structure for tool usage and the format of tool call responses.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0002-agent-tools.md

LANGUAGE: APIDOC
CODE:
```
## OpenAI Assistant API - Code Interpreter

### Description
This describes the integration of the code interpreter tool within the OpenAI Assistant API. It outlines the message request structure for enabling the tool and the format of the tool call responses.

### Method
POST (implied, as part of a larger assistant API request)

### Endpoint
Not explicitly defined, assumed to be part of the OpenAI Assistant API endpoint.

### Parameters
#### Request Body
- **tools** (array) - Required - Specifies the tools to be used, including 'code_interpreter'.
  - **type** (string) - Required - Must be 'code_interpreter'.
- **tool_resources** (object) - Optional - Resources for the tools.
  - **code_interpreter** (object) - Optional - Configuration for the code interpreter.
    - **file_ids** (array of strings) - Optional - A list of file IDs to be used by the code interpreter.

### Response
#### Success Response (200 OK)
- **tool_calls** (array) - Contains the results of the tool execution.
  - **id** (string) - Unique identifier for the tool call.
  - **type** (string) - Type of the tool call, should be 'code'.
  - **code** (object) - Details of the code execution.
    - **input** (string) - The code executed.
    - **outputs** (array of objects) - The results of the code execution.
      - **type** (string) - Type of the output, should be 'logs'.
      - **logs** (string) - The execution logs.

### Request Example
```json
{
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "tool_resources": {
    "code_interpreter": {
      "file_ids": ["{string}"]
    }
  }
}
```

### Response Example
```json
{
  "tool_calls": [
    {
      "id": "{string}",
      "type": "code",
      "code": {
        "input": "{string}",
        "outputs": [
          {
            "type": "logs",
            "logs": "{string}"
          }
        ]
      }
    }
  ]
}
```
```

--------------------------------

TITLE: Running Tests for a Specific Package in Bash
DESCRIPTION: This command demonstrates how to execute tests for a single package, such as `agent_framework`, using `uv run poe`. The `--directory` flag is used to specify the package's location within the project structure.

SOURCE: https://github.com/microsoft/agent-framework/blob/main/python/DEV_SETUP.md

LANGUAGE: bash
CODE:
```
uv run poe --directory packages/core test
```