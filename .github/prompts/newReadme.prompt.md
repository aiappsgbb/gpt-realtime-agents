---
mode: 'agent'
model: Auto (copilot)
tools: ['githubRepo', 'search/codebase', 'edit', 'changes', 'runCommands']
description: 'Create a new README file with standard IP structure'
---
# Comprehensive README.md Generation for IP Project

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
- Review research collection findings for documentation structure, code samples, and configuration
- Use consolidated environment variables from collection template
- Reference code snippets from findings for documentation
- Validate against research gaps identified in collection phase

---

1. Generate a README.md file with the following sections:

2. **Header Section**:
   - Project title with badge/logo placeholder
   - Brief one-line description
   - Status badges (build, license, version)
   - Table of contents

3. **Overview Section**:
   - Business problem statement
   - Solution overview
   - Key benefits and value proposition
   - Target audience

4. **Technical Overview**:
   - Architecture diagram placeholder
   - Technology stack
   - Key components and services
   - System requirements
   - Data flow description

5. **Features Section**:
   - Core capabilities
   - Advanced features
   - Planned features/roadmap

6. **Getting Started**:
   - Prerequisites (tools, accounts, versions)
   - Installation instructions
   - Initial setup and configuration
   - Quick start guide
   - First-time user walkthrough

7. **Usage**:
   - Common use cases
   - Code examples
   - API documentation links
   - Configuration options

8. **Development**:
   - Development environment setup
   - Coding standards
   - Testing guidelines
   - Contribution guidelines
   - Local development workflow

9. **Deployment**:
   - Azure deployment instructions
   - Environment configuration
   - CI/CD pipeline information
   - Production considerations

10. **Monitoring and Troubleshooting**:
    - Monitoring setup
    - Common issues and solutions
    - Debugging guides
    - Performance optimization

11. **Security**:
    - Security considerations
    - Authentication and authorization
    - Data protection measures
    - Compliance information

12. **Footer Sections**:
    - Contributing guidelines
    - License information
    - Support and contact information
    - Acknowledgments

Use placeholder content that can be easily customized for specific projects. Include proper markdown formatting with headings, lists, code blocks, and links.