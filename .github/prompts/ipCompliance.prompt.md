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
- Review research collection findings for IP compliance, metadata, and validation patterns
- Use consolidated environment variables from collection template
- Reference code snippets from findings for compliance validation
- Validate against research gaps identified in collection phase

---
# IP Compliance Validation and Assessment
---
mode: 'agent'
model: Claude Sonnet 4 (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'runCommands']
description: 'Comprehensive IP compliance checker for Azure Developer CLI templates'
---

# IP Compliance Assessment

Perform a comprehensive compliance assessment of the repository to ensure it meets Azure Developer CLI template standards and is production-ready for deployment.

## Overview

This assessment covers multiple compliance areas:
- ✅ **IP Metadata Compliance**: Validates .github/ip-metadata.json against schema
- ✅ **Repository Structure**: Ensures proper folder organization and required files
- ✅ **Azure Developer CLI Configuration**: Validates azure.yaml completeness
- ✅ **Infrastructure as Code**: Checks Bicep templates and parameters
- ✅ **Deployment Readiness**: Verifies the repository can be deployed via `azd up`
- ✅ **Security & Best Practices**: Reviews security configurations and standards
- ✅ **Azure Security Compliance**: Validates adherence to [Azure Best Practices](../azure-bestpractices.md)
- ✅ **Documentation Quality**: Ensures comprehensive documentation

## Compliance Checks

### 1. IP Metadata Validation

**Check .github/ip-metadata.json file:**
- [ ] File exists in .github directory
- [ ] Validates against [.github/ip-metadata.schema.json](../ip-metadata.schema.json)
- [ ] All required fields are present and properly formatted
- [ ] Enum values match schema definitions
- [ ] Microsoft aliases are in correct format
- [ ] Dates are in YYYY-MM-DD format
- [ ] Azure services list is comprehensive and accurate
- [ ] Maturity level (Gold/Silver/Bronze) matches repository quality
- [ ] GBB patterns are relevant to the solution
- [ ] Industry vertical is correctly specified

**Required Fields Validation:**
```json
{
  "name": "string (1-100 chars)",
  "description": "string (10-500 chars)",
  "maturity": "Gold|Silver|Bronze",
  "region": "AMER|EMEA|ASIA",
  "industry": "Financial Services|Retail|Energy|Healthcare|Manufacturing|Government|Education|Media & Entertainment|Technology",
  "owner": "Microsoft alias",
  "pattern": ["AI/ML", "Data & Analytics", "Application Innovation", ...],
  "services": ["Azure service names"],
  "version": "semantic version",
  "createdDate": "YYYY-MM-DD",
  "lastUpdated": "YYYY-MM-DD"
}
```

### 2. Repository Structure Compliance

**Check required files and folders:**
- [ ] `README.md` exists and is comprehensive
- [ ] `azure.yaml` exists and is properly configured
- [ ] `infra/` directory with Bicep templates
- [ ] `infra/main.bicep` as primary template
- [ ] `infra/main.parameters.json` for parameters
- [ ] `.github/workflows/` for CI/CD pipelines
- [ ] `.azure/` directory for environment configurations
- [ ] `src/` directory for application code
- [ ] `.gitignore` with appropriate exclusions
- [ ] `LICENSE` file with proper license
- [ ] `.github/prompts/` directory for Copilot prompts

**Check documentation quality:**
- [ ] README has proper structure with all required sections
- [ ] Architecture documentation exists
- [ ] Deployment instructions are clear and complete
- [ ] Prerequisites are well documented
- [ ] Environment setup instructions are provided
- [ ] API documentation (if applicable)
- [ ] Troubleshooting section exists

### 3. Azure Developer CLI Configuration

**Validate azure.yaml:**
- [ ] File exists and has proper YAML syntax
- [ ] `name` field is set and descriptive
- [ ] `metadata` section includes template information
- [ ] `services` section is properly configured
- [ ] Each service has correct `project`, `language`, and `host` settings
- [ ] Docker configuration is present for containerized services
- [ ] `remoteBuild: true` is set for container services
- [ ] Environment variables are properly configured
- [ ] Resource group and location settings are correct
- [ ] No hardcoded values or secrets in configuration

**Service Configuration Validation:**
```yaml
services:
  api:
    project: "./src/api"
    language: python|js|csharp
    host: containerapp
    docker:
      remoteBuild: true
  web:
    project: "./src/web"
    language: js
    host: containerapp
    docker:
      remoteBuild: true
```

### 4. Infrastructure as Code Compliance

**Bicep Template Validation:**
- [ ] `infra/main.bicep` exists and is syntactically correct
- [ ] Uses Azure Verified Modules (AVM) where possible
- [ ] Proper parameter definitions with descriptions
- [ ] Resource naming follows Azure conventions
- [ ] Tags are properly applied to all resources
- [ ] Outputs are defined for integration points
- [ ] Security best practices are followed
- [ ] RBAC configurations are present
- [ ] Managed identities are used instead of service principals
- [ ] Key Vault integration for secrets management

**Parameter File Validation:**
- [ ] `infra/main.parameters.json` exists
- [ ] All required parameters have values
- [ ] No secrets or sensitive data in parameters
- [ ] Environment-specific configurations are handled
- [ ] Parameter values are appropriate for deployment

**Infrastructure Best Practices:**
- [ ] Container Apps Environment is configured
- [ ] Application Insights for monitoring
- [ ] Key Vault for secret management
- [ ] Container Registry for images
- [ ] User Assigned Managed Identity
- [ ] Proper network security configurations
- [ ] Resource allocation is appropriate

### 5. Deployment Readiness Assessment

**Azure Developer CLI Compatibility:**
- [ ] Repository can be initialized with `azd init`
- [ ] Infrastructure can be provisioned with `azd provision`
- [ ] Applications can be deployed with `azd deploy`
- [ ] End-to-end deployment works with `azd up`
- [ ] Environment variables are properly configured
- [ ] Dependencies between services are correctly defined
- [ ] Build processes complete successfully
- [ ] Container images build without errors

**Pre-deployment Checks:**
- [ ] All application dependencies are specified
- [ ] Build configurations are correct
- [ ] Port configurations match service definitions
- [ ] Health check endpoints are implemented
- [ ] Logging is properly configured
- [ ] Error handling is implemented

### 6. Security & Compliance

**Security Configuration:**
- [ ] No secrets or credentials in repository
- [ ] Managed identities are used for Azure authentication
- [ ] Key Vault integration for secret management
- [ ] RBAC permissions follow least privilege principle
- [ ] Network security groups are configured appropriately
- [ ] HTTPS is enforced for all endpoints
- [ ] Security headers are configured in applications
- [ ] Input validation is implemented

**Code Quality:**
- [ ] Linting configurations are present
- [ ] Code formatting standards are enforced
- [ ] Security scanning is configured in CI/CD
- [ ] Dependency vulnerability scanning is enabled
- [ ] Unit tests are present and comprehensive
- [ ] Integration tests are implemented

### 7. GitHub Integration

**GitHub Actions Workflows:**
- [ ] CI/CD workflows are present in `.github/workflows/`
- [ ] Workflows include security scanning
- [ ] Proper secrets management in GitHub
- [ ] Environment protection rules are configured
- [ ] Pull request validation is implemented
- [ ] Automated deployment to staging/production

**Repository Settings:**
- [ ] Branch protection rules are configured
- [ ] Required status checks are enabled
- [ ] Secrets are properly configured
- [ ] Environment-specific configurations

## Compliance Assessment Report

After running all checks, generate a comprehensive report with:

### ✅ Passed Checks
List all compliance areas that pass validation with details.

### ❌ Failed Checks
List all compliance violations with:
- **Issue Description**: Clear explanation of the problem
- **Impact**: How this affects deployment or functionality
- **Recommendation**: Specific steps to fix the issue
- **Priority**: High/Medium/Low based on impact

### ⚠️ Warnings
List potential issues or improvements with:
- **Observation**: What was found
- **Suggestion**: Recommended improvement
- **Benefit**: Why this improvement matters

### 📋 Summary
- **Overall Compliance Score**: Percentage of checks passed
- **Deployment Ready**: Yes/No based on critical checks
- **Recommended Actions**: Priority-ordered list of fixes needed

## Auto-Fix Capabilities

For issues that can be automatically resolved, ask user permission before implementing fixes:

### Automatic Fixes Available:
- [ ] Create missing .github/ip-metadata.json with template structure
- [ ] Add missing required files (README sections, .gitignore entries)
- [ ] Fix azure.yaml configuration issues
- [ ] Update Bicep templates to use AVM modules
- [ ] Add missing environment variables to container apps
- [ ] Create missing GitHub Actions workflows
- [ ] Fix parameter file issues
- [ ] Add missing documentation sections

### Manual Fixes Required:
- [ ] Business logic and application-specific configurations
- [ ] Environment-specific secrets and credentials
- [ ] Custom business requirements
- [ ] Organization-specific policies and standards

## Execution Instructions

1. **Run Comprehensive Assessment**: Execute all compliance checks
2. **Generate Detailed Report**: Provide findings with explanations
3. **Identify Auto-Fix Opportunities**: List what can be automatically resolved
4. **Request Permission**: Ask user if auto-fixes should be applied
5. **Implement Approved Fixes**: Apply only approved automatic fixes
6. **Provide Manual Fix Guidance**: Give detailed instructions for remaining issues
7. **Re-validate**: Run checks again after fixes to confirm resolution

## Usage Examples

### Quick Compliance Check
```bash
# This prompt will:
# 1. Scan all compliance areas
# 2. Report violations and recommendations
# 3. Offer to auto-fix approved issues
```

### Deployment Readiness Validation
```bash
# Validates that the repository is ready for:
# - azd init (if needed)
# - azd provision
# - azd deploy
# - azd up (end-to-end)
```

### Security Compliance Review
```bash
# Focuses on security-related compliance:
# - Secret management
# - Authentication configuration
# - Network security
# - RBAC settings
```

## Success Criteria

A repository is considered **fully compliant** when:
- ✅ All IP metadata is complete and valid
- ✅ Repository structure follows Azure Developer CLI standards
- ✅ Infrastructure templates are complete and use best practices
- ✅ Applications build and deploy successfully
- ✅ Security configurations meet enterprise standards
- ✅ Documentation is comprehensive and accurate
- ✅ `azd up` completes successfully without errors

**Deployment Ready Status**: The repository can be deployed to Azure using Azure Developer CLI with minimal configuration and meets all production readiness criteria.