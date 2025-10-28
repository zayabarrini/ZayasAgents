terraform-app-infrastructure/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── versions.tf
├── providers.tf
├── monitoring.tf
├── security.tf
├── dns.tf
├── compute.tf
├── storage.tf
├── modules/
│   ├── vpc/
│   ├── alb/
│   ├── autoscaling/
│   └── security/
├── environments/
│   ├── production/
│   │   ├── emea/
│   │   │   └── main.tf
│   │   └── china/
│   │       └── main.tf
│   ├── staging/
│   └── development/
├── scripts/
│   ├── deployment/
│   │   └── deploy.sh
│   ├── incident-response/
│   │   └── remediation.py
│   └── monitoring/
│       └── health-check.py
├── docs/
│   ├── architecture.md
│   ├── runbooks.md
│   └── network-diagram.md
├── .github/
│   └── workflows/
│       └── terraform.yml
├── .gitlab-ci.yml
├── .terraform-version
├── .tflint.hcl
└── .pre-commit-config.yaml


1. Initialize the Project


# Install pre-commit hooks
pre-commit install

# Install Terraform tools
tfenv install 1.5.0  # If using tfenv
tfenv use 1.5.0

# Install TFLint
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Install pre-commit
pip install pre-commit

2. Development Workflow Commands

# Format Terraform code
terraform fmt -recursive

# Validate Terraform configuration
terraform validate

# Run security scan
tfsec .

# Run linter
tflint

# Run all pre-commit hooks
pre-commit run --all-files

# Plan infrastructure changes
terraform plan -out=plan.tfplan

# Apply changes
terraform apply plan.tfplan

3. Useful Shell Aliases

# Add to ~/.bashrc or ~/.zshrc
alias tf='terraform'
alias tffmt='terraform fmt -recursive'
alias tfval='terraform validate'
alias tfplan='terraform plan -out=plan.tfplan'
alias tfapply='terraform apply plan.tfplan'
alias tflint-all='tflint && tfsec .'
alias tfprecommit='pre-commit run --all-files'


This setup provides:

Complete project structure for multi-environment infrastructure

Comprehensive linting with pre-commit hooks for quality control

CI/CD integration with GitHub Actions

VS Code optimization with recommended extensions and settings

Automated validation for Terraform, Python, and shell scripts