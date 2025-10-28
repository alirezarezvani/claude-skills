# Security Policy

## Supported Versions

We release updates and security fixes for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

All skills are currently at version 1.0.0 and receive active support.

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability within this repository, please follow these steps:

### 1. Do NOT Open a Public Issue

Please **do not** create a public GitHub issue for security vulnerabilities. This helps protect users while we work on a fix.

### 2. Contact Us Privately

Report security vulnerabilities through:

**Primary Contact:**
- **Website:** [alirezarezvani.com](https://alirezarezvani.com) (use contact form)
- **Medium:** [@alirezarezvani](https://medium.com/@alirezarezvani) (private message)

**Information to Include:**
- Type of vulnerability
- Full details of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)
- Your contact information

### 3. Response Timeline

We aim to respond to security reports according to this timeline:

- **Initial Response:** Within 48 hours
- **Vulnerability Assessment:** Within 1 week
- **Fix Development:** Based on severity (see below)
- **Public Disclosure:** After fix is deployed

### Severity Levels

**Critical (24-48 hours):**
- Remote code execution
- Unauthorized access to sensitive data
- Privilege escalation

**High (1 week):**
- Data exposure
- Authentication bypass
- Significant security weakness

**Medium (2 weeks):**
- Cross-site scripting (XSS)
- Information disclosure
- Security misconfigurations

**Low (1 month):**
- Minor information leaks
- Best practice violations
- Non-critical security improvements

---

## Security Best Practices for Users

### When Using Skills

**1. Review Python Scripts Before Execution**

Always review what a script does before running it:
```bash
# Read the script first
cat scripts/tool.py

# Check for:
# - External network calls
# - File system modifications
# - Environment variable access
# - Suspicious imports
```

**2. Run Scripts in Sandboxed Environments**

For untrusted or new scripts:
```bash
# Use virtual environments
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or use Docker
docker run -it --rm -v $(pwd):/work python:3.11 python /work/scripts/tool.py
```

**3. Verify SKILL.md Content**

Check that SKILL.md:
- Doesn't request sensitive information
- Has clear, documented workflows
- Follows Anthropic's spec
- Has valid YAML frontmatter

**4. Use allowed-tools Restrictions**

If a skill has `allowed-tools` in frontmatter, it's restricted to those tools only:
```yaml
---
allowed-tools: Read, Grep, Glob
---
```
This provides an additional safety layer.

---

## Security in Skill Development

### Secure Coding Practices

**For Python Scripts:**

**DO:**
- ✅ Validate all inputs
- ✅ Use parameterized queries (if using databases)
- ✅ Handle errors gracefully
- ✅ Limit file system access to necessary directories
- ✅ Use type hints for safety
- ✅ Sanitize user input

**DON'T:**
- ❌ Use eval() or exec() with user input
- ❌ Execute shell commands with unsanitized input
- ❌ Store credentials in code
- ❌ Make unchecked network requests
- ❌ Access sensitive system files
- ❌ Use deprecated libraries with known vulnerabilities

**Example - Secure Input Handling:**
```python
import os
import re

def safe_read_file(filename: str) -> str:
    """Safely read a file with validation."""
    # Validate filename
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise ValueError("Invalid filename")

    # Prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        raise ValueError("Invalid file path")

    # Read from safe directory
    safe_dir = os.path.join(os.getcwd(), 'data')
    full_path = os.path.join(safe_dir, filename)

    # Verify path is within safe directory
    if not full_path.startswith(safe_dir):
        raise ValueError("Path outside safe directory")

    with open(full_path, 'r') as f:
        return f.read()
```

### Dependency Management

**Keep Dependencies Minimal:**
- Prefer Python standard library
- Document all external dependencies
- Pin dependency versions
- Regularly update for security patches

**Check Dependencies:**
```bash
# Audit Python dependencies
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

---

## Vulnerability Disclosure Process

### For Maintainers

When a vulnerability is reported:

1. **Acknowledge Receipt** (48 hours)
   - Confirm we received the report
   - Provide expected timeline

2. **Assess Severity** (1 week)
   - Evaluate impact and scope
   - Determine priority level
   - Assign severity rating

3. **Develop Fix** (Based on severity)
   - Create patch in private branch
   - Test thoroughly
   - Prepare security advisory

4. **Deploy Fix**
   - Merge to main
   - Tag new version
   - Publish GitHub security advisory

5. **Public Disclosure**
   - Announce in CHANGELOG
   - Credit reporter (if desired)
   - Provide mitigation guidance

---

## Security Features

### Current Security Measures

**Repository:**
- All skills open source (transparent review)
- MIT License (clear usage terms)
- No secrets or credentials committed
- Clean .gitignore for sensitive files

**Python Scripts:**
- Standard library preferred (minimal attack surface)
- No network calls in core tools
- File system access limited
- Input validation implemented

**Documentation:**
- Clear usage instructions
- Security considerations documented
- Best practices included
- Safe examples provided

### Planned Security Enhancements

**v1.1.0:**
- Automated dependency scanning
- GitHub Dependabot integration
- Security advisories enabled
- Vulnerability scanning in CI/CD

---

## Responsible Disclosure

We appreciate security researchers who:
- Report vulnerabilities responsibly
- Give us time to fix before public disclosure
- Provide detailed reproduction steps
- Suggest potential fixes

### Recognition

Security researchers who responsibly disclose will be:
- Credited in CHANGELOG (if desired)
- Mentioned in security advisory
- Recognized in README (optional)
- Thanked publicly on social media (with permission)

---

## Contact

For security-related inquiries:

- **Website:** [alirezarezvani.com](https://alirezarezvani.com)
- **Blog:** [medium.com/@alirezarezvani](https://medium.com/@alirezarezvani)
- **GitHub Issues:** For non-security bugs only

**Please do not use public channels for security vulnerabilities.**

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)

---

Thank you for helping keep the Claude Skills Library and its users safe!
