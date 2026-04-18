# Install Claude Skills to Claude Code
# Usage: .\install-skills.ps1

$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsDir = "$env:USERPROFILE\.claude\skills"

# Create skills directory if it doesn't exist
if (-not (Test-Path $skillsDir)) {
    Write-Host "Creating skills directory: $skillsDir"
    New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
}

# List of skill domains to copy
$skillDomains = @(
    "engineering-team",
    "engineering",
    "product-team",
    "marketing-skill",
    "c-level-advisor",
    "project-management",
    "ra-qm-team",
    "business-growth",
    "finance",
    "agents",
    "commands",
    "standards",
    "templates"
)

# Copy each skill domain
$copied = 0
$skipped = 0

foreach ($domain in $skillDomains) {
    $sourcePath = Join-Path $sourceDir $domain
    $destPath = Join-Path $skillsDir $domain

    if (Test-Path $sourcePath) {
        # Remove existing if present
        if (Test-Path $destPath) {
            Write-Host "Updating: $domain"
            Remove-Item -Recurse -Force $destPath
        } else {
            Write-Host "Installing: $domain"
        }

        # Copy the domain folder
        Copy-Item -Recurse -Force $sourcePath $destPath
        $copied++
    } else {
        Write-Host "Skipped: $domain (not found)"
        $skipped++
    }
}

Write-Host ""
Write-Host "✓ Installation complete!"
Write-Host "  - Installed: $copied domains"
Write-Host "  - Skipped: $skipped"
Write-Host "  - Location: $skillsDir"
