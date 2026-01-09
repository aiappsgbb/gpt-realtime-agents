# GitHub Workflows

This directory contains GitHub Actions workflows for CI/CD.

You can add workflow files here to automate building, testing, and deploying your application.

## Example Workflow

A typical azd workflow might include:

1. **CI Workflow**: Build and test on pull requests
2. **CD Workflow**: Deploy to Azure when code is merged to main

For Azure Developer CLI integration, consider using the official azd GitHub Action:
<https://github.com/Azure/azure-dev>

## Sample workflow structure

```yaml
name: Deploy to Azure
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Azure Developer CLI
        uses: Azure/setup-azd@v0.1.0
      - name: Deploy to Azure
        run: |
          azd auth login --service-principal --tenant-id ${{ secrets.AZURE_TENANT_ID }} --client-id ${{ secrets.AZURE_CLIENT_ID }} --client-secret ${{ secrets.AZURE_CLIENT_SECRET }}
          azd up --no-prompt
        env:
          AZURE_ENV_NAME: ${{ vars.AZURE_ENV_NAME }}
          AZURE_LOCATION: ${{ vars.AZURE_LOCATION }}
          AZURE_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```