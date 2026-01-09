---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'git_branch', 'runCommands']
description: 'Create a new ASP.NET Core Web API application using .NET 9 following best practices and a simplified structure.'
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
- Review research collection findings for .NET API patterns, libraries, and configurations
- Use consolidated environment variables from collection template
- Reference code snippets from findings for implementation
- Validate against research gaps identified in collection phase

---
# Create New ASP.NET Core Web API Application

- Create a new ASP.NET Core Web API application using .NET 9 under the src folder with a simplified structure.
- Ensure you create a new branch for this work with naming feature/add-${input:appName:my-dotnet-app}
- Make sure to use all the provided tools to actually create folders and files with the required content.

**Application Name**: ${input:appName:my-dotnet-app}

## Directory Structure

Create the following directory structure:

```text
src/
├── ${input:appName}/
│   ├── ${input:appName}.csproj
│   ├── README.md
│   ├── global.json
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── appsettings.json
│   ├── appsettings.Development.json
│   ├── Program.cs
│   ├── Controllers/
│   │   └── HealthController.cs
│   ├── Services/
│   │   ├── IHealthService.cs
│   │   └── HealthService.cs
│   ├── Models/
│   │   ├── HealthResponse.cs
│   │   └── ApiResponse.cs
│   ├── Configuration/
│   │   ├── AppSettings.cs
│   │   └── AzureSettings.cs
│   ├── Extensions/
│   │   ├── ServiceCollectionExtensions.cs
│   │   └── ApplicationBuilderExtensions.cs
│   ├── Middleware/
│   │   ├── ExceptionHandlingMiddleware.cs
│   │   └── RequestLoggingMiddleware.cs
│   └── Utils/
│       ├── AzureCredentialHelper.cs
│       └── LoggingHelper.cs
```

## File Requirements

### 1. ${input:appName}.csproj

Generate a `.csproj` file with:

- Project metadata targeting .NET 9.0
- Enable latest C# language features and nullable reference types
- Package references with safe version pinning (no major version upgrades):
  - Microsoft.AspNetCore.OpenApi>=9.0.0,<10.0.0
  - Swashbuckle.AspNetCore>=7.0.0,<8.0.0
  - Serilog.AspNetCore>=8.0.0,<9.0.0 (structured logging)
  - Serilog.Sinks.Console>=6.0.0,<7.0.0, Serilog.Sinks.File>=6.0.0,<7.0.0
- Azure integration packages:
  - Azure.Identity>=1.12.0,<2.0.0
  - Azure.Monitor.OpenTelemetry.AspNetCore>=1.2.0,<2.0.0
- OpenTelemetry packages:
  - OpenTelemetry.Extensions.Hosting>=1.9.0,<2.0.0
  - OpenTelemetry.Instrumentation.AspNetCore>=1.9.0,<2.0.0
  - OpenTelemetry.Instrumentation.Http>=1.9.0,<2.0.0
- Development packages: Microsoft.AspNetCore.Mvc.Testing>=9.0.0,<10.0.0, xunit>=2.9.0,<3.0.0, xunit.runner.visualstudio>=2.8.0,<3.0.0

Example .csproj:
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <LangVersion>latest</LangVersion>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <DockerDefaultTargetOS>Linux</DockerDefaultTargetOS>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="9.0.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="7.0.0" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="Azure.Identity" Version="1.12.0" />
    <PackageReference Include="Azure.Monitor.OpenTelemetry.AspNetCore" Version="1.2.0" />
  </ItemGroup>

</Project>
```

### 2. global.json

Create a `global.json` file specifying .NET 9.0 SDK:

```json
{
  "sdk": {
    "version": "9.0.100",
    "rollForward": "latestMinor"
  }
}
```

### 3. Program.cs

Generate a `Program.cs` file using .NET 9 features with:

- Minimal API setup with top-level statements
- Configuration management with strongly-typed settings
- Dependency injection container configuration
- Serilog structured logging integration
- OpenTelemetry tracing configuration
- Exception handling middleware
- Health check endpoints
- Swagger/OpenAPI documentation
- CORS configuration
- Azure Monitor integration
- Production-ready settings

Example Program.cs structure:
```csharp
using Serilog;
using Azure.Monitor.OpenTelemetry.AspNetCore;
using MyDotNetApp.Configuration;
using MyDotNetApp.Extensions;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

// Configure strongly-typed settings
builder.Services.Configure<AppSettings>(builder.Configuration);
builder.Services.Configure<AzureSettings>(builder.Configuration.GetSection("Azure"));

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Add custom services
builder.Services.AddApplicationServices();

// Add Azure Monitor OpenTelemetry
builder.Services.AddOpenTelemetry()
    .UseAzureMonitor();

// Add health checks
builder.Services.AddHealthChecks();

var app = builder.Build();

// Configure the HTTP request pipeline
app.UseExceptionHandling();
app.UseRequestLogging();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors();
app.UseAuthorization();

app.MapControllers();
app.MapHealthChecks("/health");

app.Run();
```

### 4. Dockerfile

Create a multi-stage Dockerfile optimized for ASP.NET Core with:

- Multi-stage build for smaller production images
- .NET 9.0 runtime and SDK images (use Azure Linux base)
- Proper layer caching
- Non-root user for security
- Health check configuration
- Production-ready settings

```dockerfile
# Dockerfile structure for ASP.NET Core
FROM mcr.microsoft.com/dotnet/aspnet:9.0-azurelinux3.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

# Install CA certificates
RUN tdnf install -y ca-certificates && \
    update-ca-trust enable && \
    update-ca-trust extract && \
    tdnf clean all

FROM mcr.microsoft.com/dotnet/sdk:9.0-azurelinux3.0 AS build
WORKDIR /src
COPY ["${input:appName}.csproj", "."]
RUN dotnet restore "${input:appName}.csproj"
COPY . .
WORKDIR "/src"
RUN dotnet build "${input:appName}.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "${input:appName}.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

ENTRYPOINT ["dotnet", "${input:appName}.dll"]
```

### 5. .dockerignore

Create a `.dockerignore` file to exclude:

- Development files (.git, .vs, .vscode, etc.)
- Build artifacts (bin/, obj/, etc.)
- Test files and documentation
- IDE configuration files
- OS-specific files
- Package files (*.nupkg)

### 6. Configuration/AppSettings.cs

Create a strongly-typed configuration class using .NET 9 features:

```csharp
namespace MyDotNetApp.Configuration;

public record AppSettings
{
    public string ApplicationName { get; init; } = string.Empty;
    public string Version { get; init; } = "1.0.0";
    public LoggingSettings Logging { get; init; } = new();
    public AzureSettings Azure { get; init; } = new();
}

public record LoggingSettings
{
    public string LogLevel { get; init; } = "Information";
    public bool EnableConsoleLogging { get; init; } = true;
    public bool EnableFileLogging { get; init; } = false;
    public string LogFilePath { get; init; } = "logs/app.log";
}

public record AzureSettings
{
    public string? ClientId { get; init; }
    public string? TenantId { get; init; }
    public string? KeyVaultEndpoint { get; init; }
    public string? ApplicationInsightsConnectionString { get; init; }
}
```

### 7. Utils/AzureCredentialHelper.cs

Create an Azure credential helper using best practices:

```csharp
using Azure.Identity;

namespace MyDotNetApp.Utils;

public static class AzureCredentialHelper
{
    /// <summary>
    /// Get Azure credential using best practice chain.
    /// This works for both local development (azd) and production (Container Apps).
    /// </summary>
    /// <returns>
    /// ChainedTokenCredential that tries Azure Developer CLI first, then Managed Identity.
    /// </returns>
    public static ChainedTokenCredential GetAzureCredential()
    {
        return new ChainedTokenCredential(
            new AzureDeveloperCliCredential(), // tries Azure Developer CLI (azd) for local development
            new ManagedIdentityCredential()    // fallback to managed identity for production
        );
    }

    /// <summary>
    /// Get Azure credential with specific client ID for managed identity.
    /// Use when AZURE_CLIENT_ID environment variable is set.
    /// </summary>
    /// <param name="clientId">The client ID of the managed identity</param>
    /// <returns>ChainedTokenCredential with specified client ID</returns>
    public static ChainedTokenCredential GetAzureCredential(string clientId)
    {
        return new ChainedTokenCredential(
            new AzureDeveloperCliCredential(),
            new ManagedIdentityCredential(clientId)
        );
    }
}
```

**Important**: Always ensure `AZURE_CLIENT_ID` environment variable is set in Azure Container Apps to specify which managed identity to use for authentication.

**CRITICAL**: Follow [Azure Best Practices](../azure-bestpractices.md) - NEVER use API keys for Azure services. All authentication must use Entra ID with managed identities.

### 8. Extensions/ServiceCollectionExtensions.cs

Create service registration extensions:

```csharp
using MyDotNetApp.Services;

namespace MyDotNetApp.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        // Register application services
        services.AddScoped<IHealthService, HealthService>();
        
        // Add HTTP client with Azure authentication
        services.AddHttpClient();
        
        // Add Azure credential helper
        services.AddSingleton(_ => AzureCredentialHelper.GetAzureCredential());
        
        return services;
    }
}
```

### 9. Middleware/ExceptionHandlingMiddleware.cs

Create global exception handling middleware:

```csharp
using System.Net;
using System.Text.Json;
using MyDotNetApp.Models;

namespace MyDotNetApp.Middleware;

public class ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await next(context);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        var response = new ApiResponse<object>
        {
            Success = false,
            Message = "An error occurred while processing your request",
            Data = null
        };

        context.Response.ContentType = "application/json";
        context.Response.StatusCode = exception switch
        {
            ArgumentException => (int)HttpStatusCode.BadRequest,
            UnauthorizedAccessException => (int)HttpStatusCode.Unauthorized,
            NotImplementedException => (int)HttpStatusCode.NotImplemented,
            _ => (int)HttpStatusCode.InternalServerError
        };

        var jsonResponse = JsonSerializer.Serialize(response, new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        });

        await context.Response.WriteAsync(jsonResponse);
    }
}
```

### 10. Controllers/HealthController.cs

Create a health check controller:

```csharp
using Microsoft.AspNetCore.Mvc;
using MyDotNetApp.Models;
using MyDotNetApp.Services;

namespace MyDotNetApp.Controllers;

[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class HealthController(IHealthService healthService, ILogger<HealthController> logger) : ControllerBase
{
    /// <summary>
    /// Get application health status
    /// </summary>
    /// <returns>Health status information</returns>
    [HttpGet]
    [ProducesResponseType<ApiResponse<HealthResponse>>(StatusCodes.Status200OK)]
    public async Task<ActionResult<ApiResponse<HealthResponse>>> GetHealth()
    {
        logger.LogInformation("Health check requested");
        
        var healthResponse = await healthService.GetHealthAsync();
        
        return Ok(new ApiResponse<HealthResponse>
        {
            Success = true,
            Message = "Health check