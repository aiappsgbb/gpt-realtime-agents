---
description: "Generate research plan matching current 4-section template (scope snapshot, topics/search terms, resolved libraries, refined search terms)"
---

The raw user request (if provided) appears below and MUST anchor the plan.

User input:

$ARGUMENTS

# Ultra-Minimal Research Plan Instructions

Goal: Produce a concise plan (using `research-plan-template.md`) containing ONLY the sections that exist in the template, in order:
1. Scope Snapshot table
2. Topics (initial search terms checklist that focus on getting the major libraries correct)
3. Resolved Library Names (context libraries for potential later retrieval)
4. Refined Search Terms (more specific intent-focused phrases)
5. Open Notes (draft preparatory notes for a future final answer; synthesize gaps & intended synthesis approach)

Do NOT introduce additional sections (no placeholder findings/output targets/checklist/response outline unless the template is updated). Keep phrasing concise and implementation-focused.

## Required Actions (Exact)
1. Scope Snapshot: Replace example descriptions with concrete scope elements; no blank Description cells. Use <PLACEHOLDER> only when unknown and non-blocking; otherwise clarify.
2. Topics (accurate and targeted search terms): Provide a minimal checklist (≤3-5) of accurate and targeted phrases derived from Scope items. Each bullet should map back to at least one Scope element; no duplicates.
3. Resolved Library Names: List only libraries genuinely relevant to the scope. Use generic names unless user specified exact ones. Skip any you cannot justify from Scope.
4. Refined Search Terms: For each topic, add 1–2 specific intent phrases (total refined terms ≤2x terms). No commands, URLs, or invocation syntax.
5. Open Notes: Summarize (a) key unanswered points, (b) planned synthesis structure, (c) any assumptions. Bullet form, concise (≤12 words per bullet). No final answer content yet.

## Prohibitions
- Do NOT add sections not present in the template.
- Do NOT name commands, shell tools, or cite repository file paths.
- Do NOT fabricate concrete configuration values (SKUs, tiers) — use <SKU>, <TIER> if needed.
- Do NOT perform or summarize real documentation retrieval.
- Do NOT provide the final answer inside Open Notes; it is preparation only.

## Save & Format
Save as `.github/scratchpad/research-plan-[TIMESTAMP].md` (UTC compact). If another exists same day, append `-v2`, `-v3`, etc. Output must be ONLY the filled template plus final Status line.

## Readiness Criteria
Ready only if:
- Scope Snapshot has no blank Description cells
- Topics list covers each distinct scope concern (≤10) with no near-duplicates
- Resolved Library Names: every entry aligns with at least one Topic; none are gratuitous
- Refined Search Terms: each topic represented by ≥1 refined phrase; no command syntax, URLs, or library name repetition unless adding distinct intent
- Open Notes present with at least 3 bullets (or fewer if trivially small scope) and contains no conclusive final answer text

Return only the filled template content (no extra commentary).

## Section-by-Section Fill Instructions
1. Scope Snapshot
	- Replace placeholder descriptions with concrete concise scope statements (≤12 words each).
	- Remove rows you do not need; add only if a distinct scope element is missing.
	- No commands, tool names, or file paths.

2. Topics (Accurate and Targeted Search Terms)
	- Each bullet: Accurate and targeted conceptual phrase ("minimal auth flow", "container deployment basics").
	- Tie directly to one or more scope items; do not duplicate meaning.
	- Keep list lean (≤3-5). Come up with **MOST** essential topics only. Focus on getting the libraries correct because they are the key to a healthy research phase.
	- Make sure to cover the essentials first, do NOT go broad. Stick to what is directly related to the user ask.

3. Resolved Library Names
	- List candidate libraries or SDK domains (generic if exact undecided: "auth library", "http client").
	- Omit any not clearly justified by scope.
    - To fill in this section, you **MUST** perform the MANDATORY TOOL CALL: `upstash/context7/resolve-library-id` to resolve the library names.
	- Make sure to get the most relevant libraries; avoid gratuitous entries. Only include libraries you can justify from the scope/topics (revisit the user ask AGAIN). For example if the user requests something like the following: "I want to build a chatbot using Azure OpenAI and deploy it to Azure App Service with CI/CD from GitHub Actions", you might choose libraries like "Azure OpenAI SDK", "Azure App Service SDK", "GitHub Actions SDK", "Azure Identity SDK" but NOT something unrelated like "Azure Cosmos DB SDK" unless the user specifically mentioned a database.
	- The most common libraries that we work with are listed below:
		* **Microsoft Agent Framework SDK – microsoft.agentframework:** Framework for building multimodal, agentic applications across Microsoft 365 and custom apps.
		* **Azure OpenAI Service SDK – azure.ai.openai:** Python SDK for integrating OpenAI models hosted in Azure for text, chat, and image generation.
		* **Azure AI Foundry SDK – azure.ai.foundry:** Unified SDK for orchestrating AI models, agents, and workflows across Azure AI services.
		* **Azure AI Document Intelligence SDK – azure.ai.documentintelligence:** Extracts and structures data from PDFs and scanned documents using Azure AI.
		* **Azure AI Search SDK – azure.search.documents:** Enables intelligent search and retrieval for RAG and cognitive search applications.
		* **Azure AI Language SDK – azure.ai.language:** Provides NLP capabilities such as summarization, key phrase extraction, and entity recognition.
		* **Azure AI Vision SDK – azure.ai.vision:** Handles image recognition, OCR, and video analysis.
		* **Azure AI Speech SDK – azure.cognitiveservices.speech:** Converts speech to text, synthesizes voice, and performs real-time speech translation.
		* **Azure AI Translator SDK – azure.ai.translation:** Provides real-time translation and language detection.
		* **Azure AI Content Safety SDK – azure.ai.contentsafety:** Detects and filters unsafe text and images in generative outputs.
		* **Azure AI Content Understanding SDK – azure.ai.contentunderstanding:** Enables semantic extraction and comprehension of unstructured content.
		* **Azure Machine Learning SDK v2 – azure.ai.ml:** Full ML lifecycle SDK for training, deploying, and managing AI models in Azure ML.
		* **Semantic Kernel – semantic_kernel:** Framework for composing AI models, tools, and memory into intelligent agent workflows.
		* **Bot Framework SDK – botbuilder:** SDK for building conversational bots and assistants integrated with Teams or web.
		* **SynapseML – synapse.ml:** Scalable ML and AI library integrating Spark, Azure ML, and Cognitive Services.
		* **DeepSpeed – deepspeed:** Library for distributed training and optimization of large language models.
		* **ONNX Runtime – onnxruntime:** High-performance inference engine for cross-platform model execution.
		* **Olive – olive-ai:** Toolkit for model optimization, quantization, and deployment on edge or cloud.
		* **Responsible AI Toolbox – raiutils:** Tools for evaluating, explaining, and monitoring responsible AI systems.
		* **Fairlearn – fairlearn:** Library for assessing and mitigating fairness and bias in ML models.
		* **InterpretML – interpret:** Framework for explainable machine learning and model interpretability.
		* **Error Analysis – erroranalysis:** Identifies root causes of model errors and performance issues.
		* **Azure Container Apps CLI Extension – azure.cli.command_modules.containerapp:** CLI for deploying and scaling containerized AI inference apps.
		* **Azure Kubernetes Service CLI – azure.cli.command_modules.aks:** Manages AKS clusters for running AI workloads.
		* **Azure Container Registry CLI – azure.cli.command_modules.acr:** Manages container images for AI and web services.
		* **Azure Functions Core Tools – azure.functions:** Enables development of event-driven serverless functions using Python.
		* **Azure App Service CLI – azure.cli.command_modules.webapp:** Deploys and manages AI-enabled web applications.
		* **Azure Batch SDK – azure.batch:** Runs large-scale batch inference or parallel training jobs.
		* **Azure Cosmos DB SDK – azure.cosmos:** Multi-model NoSQL SDK for storing and querying vector and JSON data for AI apps.
		* **Azure PostgreSQL SDK – azure.mgmt.rdbms.postgresql:** Manages PostgreSQL databases for structured and vectorized AI data.
		* **Azure SQL Database SDK – azure.mgmt.sql:** Manages SQL databases used for structured AI application data.
		* **Azure Cache for Redis SDK – azure.mgmt.redis:** Provides high-performance caching for AI workloads and chat memory.
		* **Azure Logic Apps SDK – azure.mgmt.logic:** Automates workflows connecting AI models with external services.
		* **Azure Data Factory SDK – azure.mgmt.datafactory:** Manages ETL pipelines feeding AI and ML data flows.
		* **Azure Durable Functions – azure.durable_functions:** Orchestrates long-running and stateful AI agent workflows.
		* **Azure Blob Storage SDK – azure.storage.blob:** Manages unstructured data storage for models, embeddings, and datasets.
		* **Azure Data Lake SDK – azure.storage.filedatalake:** Provides hierarchical file storage for AI data processing pipelines.
		* **Azure Queue Storage SDK – azure.storage.queue:** Handles asynchronous message passing between AI components.
		* **Azure Service Bus SDK – azure.servicebus:** Reliable enterprise messaging between AI services and orchestrators.
		* **Azure Event Hubs SDK – azure.eventhub:** Streams telemetry and event data for real-time AI processing.
		* **Azure Event Grid SDK – azure.eventgrid:** Publishes and subscribes to events for AI automation and triggers.
		* **Azure SignalR Service SDK – azure.signalr:** Adds real-time communication and live updates to AI-powered applications.
		* **Azure CLI – azure.cli:** Command-line tool for managing all Azure resources and services.
		* **Azure Developer CLI – azd:** Developer-first CLI for provisioning, deploying, and debugging full-stack AI apps.
		* **Azure PowerShell – azure.mgmt.resource:** Automation scripts for managing Azure AI infrastructure.
		* **Azure Resource Manager SDK – azure.mgmt.resource:** Manages provisioning and lifecycle of Azure resources via API.
		* **Azure Bicep – bicep:** DSL for Infrastructure-as-Code deployments of AI and data solutions.
		* **Azure Front Door SDK – azure.mgmt.frontdoor:** Configures global load balancing and routing for AI web apps.
		* **Azure API Management SDK – azure.mgmt.apimanagement:** Secures and exposes AI model APIs with usage policies.
		* **Azure Load Balancer SDK – azure.mgmt.network:** Distributes inference and API requests across compute nodes.
		* **Azure Virtual Network SDK – azure.mgmt.network:** Manages private networking for secure AI deployments.
		* **Azure Application Gateway SDK – azure.mgmt.applicationgateway:** Provides WAF and SSL termination for web-based AI endpoints.
		* **Azure Monitor OpenTelemetry Exporter – azure.monitor.opentelemetry.exporter:** Sends telemetry data from OpenTelemetry to Azure Monitor.
		* **OpenTelemetry API – opentelemetry:** Provides standard interfaces for distributed tracing and metrics in Python.
		* **OpenTelemetry SDK – opentelemetry.sdk:** Core implementation for tracing, metrics, and logging instrumentation.
		* **OpenTelemetry FastAPI Instrumentation – opentelemetry.instrumentation.fastapi:** Automatically instruments FastAPI apps for tracing.
		* **OpenTelemetry HTTPX Instrumentation – opentelemetry.instrumentation.httpx:** Instruments HTTPX requests for observability and performance tracking.
		* **Azure Identity – azure.identity:** Provides credential classes for authenticating with Azure SDKs.
		* **Streamlit – streamlit:** Rapidly builds and deploys interactive AI and data-driven web apps in Python.
		* **Pydantic – pydantic:** Defines and validates structured data models for AI and API schemas.
		* **Pydantic Settings – pydantic_settings:** Simplifies environment-based configuration for AI and data apps.
		* **Python Dotenv – dotenv:** Loads environment variables from `.env` files for AI and backend apps.
		* **HTTPX – httpx:** Async HTTP client used for calling AI APIs and external endpoints.
		* **Pandas – pandas:** Core library for data manipulation and preprocessing in AI pipelines.
		* **NumPy – numpy:** Fundamental package for scientific and numerical computing.
		* **Scikit-learn – sklearn:** Machine learning library for feature engineering, modeling, and evaluation.
		* **Plotly – plotly:** Interactive data visualization library for analytics dashboards.
		* **Altair – altair:** Declarative charting library for Python, great for AI results visualization.
		* **Matplotlib – matplotlib:** Core 2D plotting library for visualizing data distributions and results.
		* **Seaborn – seaborn:** High-level interface for statistical and aesthetic data visualization.
		* **Pillow – PIL:** Image processing library for manipulating and transforming images in AI workflows.

4. Refined Search Terms
	- Each row MUST be a tuple: (Resolved Library ID from Section 3, Specific Keyphrase) exactly as shown in Table 4 format.
	- Use the resolved library identifier string (e.g., "/microsoft/azure-identity") not an alias.
	- Keyphrase: actionable, implementation-focused (verb or objective + target) ≤10 words (e.g., "authenticate with managed identity", "stream chat response tokens").
	- Each topic must map to ≥1 tuple; total tuples ≤2x number of topics unless justified by distinct scope facets.
	- Avoid duplication: do not repeat the same keyphrase across different libraries unless behavior differs materially.
	- No CLI commands, no URLs, no raw code; placeholders allowed for undecided nouns (<COMPONENT>, <FORMAT>).
	- If a required library for a keyphrase is undecided, resolve it first (or mark <PENDING_LIBRARY> only if resolution blocking—then plan is not Ready).

5. Open Notes
	- Provide a bullet list (3–8 bullets) covering:
		- Pending clarifications or unknowns
		- Outline of how final answer would be structured
		- Key assumptions (each clearly labeled Assumption: ...)
	- No direct solutions or final narrative—only preparatory scaffolding.

Validation (apply before returning)
	- No blank scope descriptions.
	- Accurate and targeted topics cover all scope aspects without redundancy.
	- Each topic represented in refined terms.
	- Refined terms total count ≤2x search term count.
	- Open Notes bullets present (≥3 unless scope trivially 1–2 items) and contain no final answer prose.
	- No forbidden concrete values (SKUs, tiers) unless user supplied.
	- No extraneous sections added.

Output: ONLY the filled template content.

External Response Rule: After writing the file, the agent MUST respond externally ONLY with: "I have completed the plan, please refer to the file <filename>." No other summary or answer.