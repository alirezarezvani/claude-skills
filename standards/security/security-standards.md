# Security Standards

## Core Security Principles

### **1. No Secrets in Code**
- Never hardcode API keys, passwords, or tokens
- Use environment variables for sensitive data
- Exclude sensitive files from git (.env, credentials.json)
- Scan for secrets before committing

### **2. Dependency Security**
- Use standard library when possible
- Minimize external dependencies
- Keep dependencies updated
- Audit dependencies for vulnerabilities

### **3. Input Validation**
- Validate all user input
- Sanitize file paths
- Prevent command injection
- Handle edge cases safely

### **4. Data Protection**
- Don't store sensitive user data
- Encrypt data in transit
- Follow privacy best practices
- Comply with GDPR/CCPA when applicable

## Secret Detection

### **Pre-Commit Secret Scanning**

```bash
# Check for common secrets before committing
git diff --cached | grep -iE 'api[_-]?key|secret|password|token|Bearer|Authorization'

# Specific patterns to detect
patterns=(
  "api[_-]?key.*=.*['\"][^x']+"
  "secret.*=.*['\"][^x']+"
  "password.*=.*['\"][^x']+"
  "token.*=.*['\"][^x']+"
  "Bearer\s+[A-Za-z0-9\-._~+/]+"
  "sk-[A-Za-z0-9]{20,}"  # OpenAI API keys
  "ghp_[A-Za-z0-9]{36}"  # GitHub Personal Access Tokens
  "AKIA[A-Z0-9]{16}"     # AWS Access Keys
)
```

### **Prohibited Patterns**

```python
# ❌ Bad - Hardcoded secret
API_KEY = "sk-1234567890abcdef"
password = "mypassword123"

# ✅ Good - Environment variable
import os
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### **Git Ignore Patterns**

```gitignore
# Secrets and credentials
.env
.env.*
*.key
*.pem
credentials.json
secrets.yaml
config/local.py

# Python cache (may contain sensitive data)
__pycache__/
*.pyc
*.pyo

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/settings.json
.idea/
```

## Python Security Best Practices

### **1. Safe File Handling**

```python
# ✅ Good - Safe path handling
import os
from pathlib import Path

def read_user_file(filename: str) -> str:
    """Safely read user-provided file."""
    # Validate filename
    if not filename or '..' in filename or filename.startswith('/'):
        raise ValueError("Invalid filename")

    # Use Path for safe path manipulation
    base_dir = Path(__file__).parent
    file_path = (base_dir / filename).resolve()

    # Ensure file is within allowed directory
    if not file_path.is_relative_to(base_dir):
        raise ValueError("File path outside allowed directory")

    # Read safely
    with open(file_path, 'r') as f:
        return f.read()

# ❌ Bad - Unsafe path handling
def read_file_unsafe(filename: str) -> str:
    # Vulnerable to directory traversal
    with open(filename, 'r') as f:
        return f.read()
```

### **2. Command Execution Safety**

```python
# ✅ Good - Safe command execution
import subprocess
from typing import List

def run_safe_command(args: List[str]) -> str:
    """Execute command safely with argument list."""
    # Use argument list, not shell=True
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=True,
        timeout=30  # Prevent hanging
    )
    return result.stdout

# Example
output = run_safe_command(['python', 'script.py', '--input', 'file.txt'])

# ❌ Bad - Shell injection vulnerability
def run_command_unsafe(command: str) -> str:
    # Vulnerable to command injection
    result = subprocess.run(
        command,
        shell=True,  # DANGEROUS!
        capture_output=True
    )
    return result.stdout.decode()
```

### **3. Input Validation**

```python
# ✅ Good - Validate and sanitize input
def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from filename."""
    import re
    # Remove path separators and null bytes
    safe = re.sub(r'[/\\:\0]', '', filename)
    # Remove leading dots (hidden files)
    safe = safe.lstrip('.')
    # Limit length
    return safe[:255]

# ❌ Bad - No validation
def process_input_unsafe(user_input: str):
    # Directly using unvalidated input
    exec(user_input)  # EXTREMELY DANGEROUS!
```

### **4. Error Handling**

```python
# ✅ Good - Don't expose sensitive info in errors
def connect_to_api(api_key: str):
    try:
        # Connection logic
        pass
    except Exception as e:
        # Don't log the API key!
        print("API connection failed. Check your credentials.")
        raise ValueError("Authentication failed") from None

# ❌ Bad - Exposing secrets in error messages
def connect_unsafe(api_key: str):
    try:
        pass
    except Exception as e:
        # Leaks API key in logs!
        print(f"Failed to connect with key: {api_key}")
        raise
```

## Dependency Management

### **Dependency Security Checklist**

```yaml
dependency_security:
  minimize_dependencies:
    - [ ] Use Python standard library when possible
    - [ ] Justify each external dependency
    - [ ] Prefer well-maintained packages
    - [ ] Check package reputation (downloads, stars, maintenance)

  version_pinning:
    - [ ] Pin exact versions in requirements.txt
    - [ ] Use version constraints (>=, <)
    - [ ] Document why specific versions required
    - [ ] Test upgrades before deploying

  vulnerability_scanning:
    - [ ] Run `pip-audit` or `safety check` regularly
    - [ ] Review security advisories
    - [ ] Update vulnerable packages promptly
    - [ ] Monitor dependabot alerts (GitHub)

  license_compliance:
    - [ ] Check package licenses
    - [ ] Avoid GPL in commercial code (if applicable)
    - [ ] Document all licenses
    - [ ] Comply with attribution requirements
```

### **Security Scanning Commands**

```bash
# Check for known vulnerabilities in dependencies
pip install pip-audit
pip-audit

# Or use safety
pip install safety
safety check

# Check for outdated packages
pip list --outdated

# Generate requirements with version pins
pip freeze > requirements.txt
```

### **Safe Requirements.txt**

```txt
# Pin exact versions for reproducibility
requests==2.31.0
pyyaml==6.0.1

# Use version constraints for flexibility
click>=8.0.0,<9.0.0
python-dateutil>=2.8.0

# Document why specific versions
# numpy==1.24.0  # Required for Python 3.11 compatibility
```

## Data Protection

### **1. User Data Handling**

```python
# ✅ Good - Minimal data collection
def analyze_text(text: str) -> dict:
    """Analyze text without storing it."""
    # Process locally, don't send to external services
    score = calculate_score(text)
    return {"score": score}

# ❌ Bad - Unnecessary data storage
def analyze_text_unsafe(text: str, user_id: str) -> dict:
    # Stores user data unnecessarily
    save_to_database(user_id, text)
    return analyze(text)
```

### **2. Privacy Best Practices**

```yaml
privacy_guidelines:
  data_minimization:
    - Collect only essential data
    - Process data locally when possible
    - Delete data after processing
    - Don't log sensitive information

  transparency:
    - Document what data is collected
    - Explain how data is used
    - Provide opt-out mechanisms
    - Allow data export/deletion

  compliance:
    - Follow GDPR if EU users
    - Follow CCPA if California users
    - Obtain consent for data collection
    - Provide privacy policy
```

## Code Review Security Checklist

### **Pre-Commit Security Review**

```yaml
security_review:
  secrets_and_credentials:
    - [ ] No hardcoded API keys
    - [ ] No hardcoded passwords
    - [ ] No hardcoded tokens
    - [ ] No private keys committed
    - [ ] .env files in .gitignore

  input_validation:
    - [ ] All user input validated
    - [ ] File paths sanitized
    - [ ] SQL queries parameterized (if applicable)
    - [ ] Command injection prevented
    - [ ] XSS prevention (if web app)

  dependency_security:
    - [ ] No known vulnerable dependencies
    - [ ] Dependencies minimized
    - [ ] Versions pinned in requirements.txt
    - [ ] Licenses checked and compatible

  error_handling:
    - [ ] Errors don't expose sensitive data
    - [ ] Stack traces sanitized in production
    - [ ] Logging doesn't include secrets
    - [ ] Error messages are user-friendly

  data_protection:
    - [ ] Sensitive data not logged
    - [ ] Personal data handled properly
    - [ ] Encryption used where needed
    - [ ] Privacy policy updated (if applicable)
```

## Incident Response

### **Security Issue Severity**

```yaml
severity_levels:
  P0_critical:
    description: "Exposed secrets, active exploits, data breach"
    response_time: "<1 hour"
    actions:
      - Rotate exposed credentials immediately
      - Disable compromised accounts
      - Notify affected users
      - Patch vulnerability
      - Document incident

  P1_high:
    description: "Vulnerable dependencies, potential exploits"
    response_time: "<24 hours"
    actions:
      - Update vulnerable packages
      - Test fixes thoroughly
      - Deploy security patches
      - Monitor for exploitation

  P2_medium:
    description: "Security best practice violations"
    response_time: "<1 week"
    actions:
      - Review and fix issues
      - Update security documentation
      - Educate team

  P3_low:
    description: "Minor security improvements"
    response_time: "<1 month"
    actions:
      - Schedule fixes in backlog
      - Update standards
```

### **Exposed Secret Response**

```bash
# If you accidentally commit a secret:

# 1. IMMEDIATELY rotate the credential
# (Change password, regenerate API key, etc.)

# 2. Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (only if not on main/production!)
git push origin --force --all

# 4. Notify security team
# Document the incident
```

## Security Tools

### **Recommended Security Tools**

```yaml
security_tools:
  secret_detection:
    - gitleaks: "Scan git repos for secrets"
    - trufflehog: "Find secrets in git history"
    - detect-secrets: "Prevent new secrets"

  dependency_scanning:
    - pip-audit: "Scan Python dependencies"
    - safety: "Check for known vulnerabilities"
    - dependabot: "Automated dependency updates (GitHub)"

  code_analysis:
    - bandit: "Python security linter"
    - pylint: "General Python linter with security checks"
    - semgrep: "Static analysis for security patterns"

  runtime_protection:
    - fail2ban: "Prevent brute force attacks (if applicable)"
    - rate limiting: "Prevent abuse"
    - monitoring: "Detect anomalous behavior"
```

### **Security Scanning Script**

```bash
#!/bin/bash
# security-scan.sh - Run all security checks

echo "🔒 Running security scans..."

# Secret detection
echo "Scanning for secrets..."
gitleaks detect --verbose --redact || echo "⚠️  Potential secrets found"

# Dependency vulnerabilities
echo "Checking dependencies..."
pip-audit || echo "⚠️  Vulnerable dependencies found"

# Python security linter
echo "Running Bandit security linter..."
bandit -r . -f screen || echo "⚠️  Security issues found"

# Check for common security issues
echo "Checking for hardcoded secrets..."
grep -r "password\s*=" --include="*.py" . && echo "⚠️  Potential hardcoded passwords"

echo "✅ Security scan complete"
```

## Security Update Process

### **Regular Security Maintenance**

- **Weekly:** Review dependabot alerts, scan for secrets
- **Monthly:** Run full security audit, update dependencies
- **Quarterly:** Review security standards, update tools
- **Annually:** Comprehensive security assessment

### **Security Documentation**

```markdown
## Security Policy

### Reporting Security Issues

**Do NOT open public issues for security vulnerabilities!**

Email: security@example.com
PGP Key: [link to public key]

Expected response time: 24 hours

### Disclosure Process

1. Report received and acknowledged
2. Issue verified and assessed
3. Fix developed and tested
4. Security advisory published
5. Credits given to reporter
```

---

**Focus**: Python security, secret detection, dependency management
**Updated**: November 2025
**Review**: Monthly security assessment
**Compliance**: OWASP Top 10, Python security best practices
