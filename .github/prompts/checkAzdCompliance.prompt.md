---
mode: 'agent'
model: Auto (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'runCommands', 'mcp']
description: 'Validate Azure Developer CLI (azd) compliance - focus on what breaks deployments'
---
Validate Azure Developer CLI (azd) configuration to catch issues that would break `azd provision` or `azd deploy`.

**Philosophy**: Only flag issues that will cause failures or runtime problems. Skip style preferences.

**Use MCP tools** to validate against current azd schema and best practices when uncertain.

---

## 🚨 Critical Checks (Will Break azd)

### 1. azure.yaml Structure

These issues will cause `azd` commands to fail:

| Check | Why It Matters |
|-------|----------------|
| `name` field exists | azd refuses to run without it |
| `infra.path` points to existing directory | `azd provision` fails immediately |
| Service `project` paths exist | `azd deploy` can't find source code |
| Service `host` matches infrastructure | Deploys to wrong/nonexistent resource |

**Quick validation**:
```powershell
azd config list  # Should not error
```

### 2. Parameter Mismatch (Most Common Failure)

Every parameter in `main.bicep` that lacks a default MUST have a mapping in `main.parameters.json`:

```bicep
// main.bicep
param environmentName string      // No default = MUST be in parameters.json
param location string             // No default = MUST be in parameters.json  
param principalId string = ''     // Has default = optional in parameters.json
```

**Check**: Compare parameter declarations in main.bicep against main.parameters.json entries.

**Required azd variables** (these are auto-populated by azd):
- `${AZURE_ENV_NAME}` → environmentName
- `${AZURE_LOCATION}` → location

### 3. Service-to-Resource Binding

If azure.yaml defines services, verify the infrastructure creates matching resources:

| azure.yaml `host` | Required Bicep Resource |
|-------------------|------------------------|
| `containerapp` | Container App with matching name pattern |
| `function` | Function App |
| `appservice` | App Service |

**The binding**: azd matches services to resources using naming conventions or explicit `resourceName` in azure.yaml.

### 4. Required azd Tags

azd uses specific tags for resource discovery and management:

**Resource Group** must have:
```bicep
var tags = {
  'azd-env-name': environmentName  // Required - azd uses this to find resources
}
```

**Service resources** (Container Apps, Functions, App Service) should have:
```bicep
tags: union(tags, {
  'azd-service-name': 'api'  // Must match service name in azure.yaml
})
```

**Check**: For each service in azure.yaml, verify the corresponding Bicep resource includes `azd-service-name` tag matching the service key.

| azure.yaml | Bicep tag required |
|------------|-------------------|
| `services.api:` | `'azd-service-name': 'api'` |
| `services.web:` | `'azd-service-name': 'web'` |

**Why it matters**: Without these tags, azd can't find deployed resources for `azd deploy` or `azd down`.

---

## ⚠️ Common Pitfalls (Runtime Failures)

### 5. Missing Outputs for Service Discovery

If you have services, azd needs outputs to know where they deployed:

```bicep
// For a service named "api" with host: containerapp
output SERVICE_API_ENDPOINT_URL string = containerApp.outputs.fqdn
output SERVICE_API_NAME string = containerApp.outputs.name
```

**Pattern**: `SERVICE_<SERVICE_NAME>_<PROPERTY>`

### 6. Hook Script Issues

If hooks are defined, verify:
- Script files exist at specified paths
- Required tools are available (uv, python, etc.)
- Scripts have proper error handling (non-zero exit = deployment stops)

**Undeclared hooks**: Check if hook scripts exist but aren't declared in azure.yaml:
```powershell
# Common hook script patterns to check in infra/scripts/
preprovision.py, postprovision.py, predeploy.py, postdeploy.py
```
If these files exist but aren't in azure.yaml `hooks:` section, they won't run during deployment.

### 7. Container Apps: Build Configuration

For `host: containerapp` services with a Dockerfile:

**Prefer `remoteBuild: true`** to avoid local Docker issues:
```yaml
services:
  api:
    host: containerapp
    docker:
      remoteBuild: true  # ✅ Builds in ACR, no local Docker needed
```

**Check**: If a service has a Dockerfile but no `docker.remoteBuild: true`, flag it:
- Local builds require Docker Desktop running
- Local builds fail in CI/CD without proper Docker setup
- Remote builds are more reliable and portable

### 8. Container Apps: Image References

For `host: containerapp` with `docker.remoteBuild: true`:
- Bicep must output `AZURE_CONTAINER_REGISTRY_ENDPOINT` or similar
- Container App must reference the correct registry

---

## 🏢 Shared Subscription Considerations

Issues specific to deploying in shared/team subscriptions:

### 9. Resource Naming Collisions

In shared subscriptions, globally unique names cause conflicts:

| Resource | Uniqueness | Fix |
|----------|------------|-----|
| Key Vault | Global | Include `resourceToken` (uniqueString) |
| Storage Account | Global | Include `resourceToken`, max 24 chars |
| Container Registry | Global | Include `resourceToken` |
| Cognitive Services | Global | Include `resourceToken` |

**Check**: Verify `main.bicep` uses `uniqueString()` or similar for these resources:
```bicep
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
```

### 10. Soft-Delete Conflicts

These resources have soft-delete enabled by default - redeploying fails if a deleted resource with same name exists:

- **Key Vault**: 90-day retention
- **Cognitive Services**: 48-hour retention  
- **API Management**: Soft-deleted instances block new ones

**Check**: Either use unique names per deployment OR handle purge in hooks.

### 11. Environment Isolation

For shared subscriptions, verify each developer's environment is isolated:

```bicep
// Good: Environment name in resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${abbrs.resourcesResourceGroups}${environmentName}'  // ✅ Includes env name
}
```

**Check**: Resource group name includes `environmentName` parameter.

### 12. Quota-Friendly Defaults

Shared subscriptions often hit quota limits. Verify reasonable defaults:

| Resource | Watch For |
|----------|-----------|
| Container Apps | CPU/memory requests |
| Cognitive Services | SKU tier (use S0 not S1+ unless needed) |
| AI Search | SKU (basic vs standard) |
| VMs/VMSS | Core counts |

### 13. principalId Handling for RBAC

RBAC assignments fail if `principalId` is empty. Verify conditional logic:

```bicep
// Good: Only create RBAC when principalId provided
resource roleAssignment '...' = if (!empty(principalId)) {
  // ...
}
```

**Check**: All RBAC assignments have `if (!empty(principalId))` or similar guard.

---

## ✅ Validation Steps

### Step 1: Structural Validation
```powershell
# These should complete without errors
azd config list
azd env list
```

### Step 2: Parameter Sync Check
Compare main.bicep parameters against main.parameters.json - flag any parameter without a default that's missing from parameters.json.

### Step 3: Path Verification
- Verify all `project` paths in azure.yaml exist
- Verify `infra.path` directory exists
- Verify hook script paths exist

### Step 4: Use MCP for Schema Validation
```
mcp_microsoft_doc_microsoft_docs_search - query: "azd azure.yaml schema"
mcp_azure_mcp_get_bestpractices - intent: "azd template configuration"
```

---

## Output: Actionable Report

Report only issues that will cause failures:

### 🔴 Blocking Issues
Issues that will cause `azd provision` or `azd deploy` to fail.

### 🟡 Likely Runtime Issues  
Configuration that will deploy but likely fail at runtime (missing env vars, wrong bindings).

### 🟢 Status
What's correctly configured.

**Skip**: Style issues, optional best practices, "nice to have" items.

---

## Quick Fixes

For each blocking issue, provide:
1. What's wrong (specific file + line if applicable)
2. Exact fix (copy-paste ready)

**Auto-Fix Mode**: If the user requests fixes (e.g., "fix it", "apply fixes", "auto-fix"), directly edit the files to resolve blocking issues:

- Update `main.parameters.json` to add missing parameter mappings
- Fix `azure.yaml` paths or structure issues
- Add missing Bicep outputs for service discovery
- Correct service-to-resource bindings

When applying fixes:
- Make minimal changes to resolve the issue
- Preserve existing formatting and comments
- Explain what was changed after applying

## References

- [azd schema reference](https://learn.microsoft.com/azure/developer/azure-developer-cli/azd-schema)
- [Azure Best Practices](../azure-bestpractices.md) (for security patterns)

---

## 🚀 Pre-Flight Checklist (Run Before Deploy)

Quick commands to validate before `azd up`:

```powershell
# 1. Verify azd can parse the project
azd config list

# 2. Check you're logged in
azd auth login --check-status

# 3. Verify environment is set
azd env list

# 4. Validate Bicep compiles (catches syntax errors)
az bicep build --file infra/main.bicep --stdout | Out-Null

# 5. What-if deployment (catches parameter/resource issues)
azd provision --preview
```

If all pass, `azd up` should succeed.
