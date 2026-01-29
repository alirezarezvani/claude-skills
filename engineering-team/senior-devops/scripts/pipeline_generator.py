#!/usr/bin/env python3
"""
CI/CD Pipeline Generator
Generates GitHub Actions or GitLab CI pipeline configurations based on detected tech stack.

Usage:
    python pipeline_generator.py <project-path> [options]

    --platform github|gitlab    CI platform (default: github)
    --output <file>            Output file path (default: stdout)
    --with-docker              Include Docker build stage
    --with-deploy              Include deployment stage
    --env staging|production   Target environment for deployment

Examples:
    python pipeline_generator.py ./my-project --platform github
    python pipeline_generator.py ./api --platform gitlab --with-docker --with-deploy
    python pipeline_generator.py . --platform github --output .github/workflows/ci.yml

Table of Contents:
==================

CLASS: PipelineGenerator
    __init__()                  - Initialize with project path and options
    generate()                  - Main entry: detect stack and generate pipeline
    detect_tech_stack()         - Detect language, framework, package manager
    generate_github_actions()   - Generate GitHub Actions workflow YAML
    generate_gitlab_ci()        - Generate GitLab CI YAML

DETECTION METHODS:
    _detect_node_project()      - Check for package.json, detect framework
    _detect_python_project()    - Check for requirements.txt, pyproject.toml
    _detect_go_project()        - Check for go.mod
    _detect_docker()            - Check for Dockerfile

GITHUB ACTIONS GENERATORS:
    _github_lint_job()          - Generate lint job
    _github_test_job()          - Generate test job with services
    _github_build_job()         - Generate Docker build job
    _github_deploy_job()        - Generate deployment job

GITLAB CI GENERATORS:
    _gitlab_stages()            - Generate stage definitions
    _gitlab_lint_job()          - Generate lint job
    _gitlab_test_job()          - Generate test job
    _gitlab_build_job()         - Generate Docker build job
    _gitlab_deploy_job()        - Generate deployment job

UTILITIES:
    _get_node_version()         - Extract Node version from .nvmrc or package.json
    _get_python_version()       - Extract Python version from pyproject.toml

FUNCTION: main()                - CLI entry point
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class PipelineGenerator:
    """Generate CI/CD pipelines for GitHub Actions or GitLab CI"""

    def __init__(self, project_path: str, platform: str = "github",
                 with_docker: bool = False, with_deploy: bool = False,
                 environment: str = "staging"):
        self.project_path = Path(project_path)
        self.platform = platform
        self.with_docker = with_docker
        self.with_deploy = with_deploy
        self.environment = environment
        self.tech_stack = {}

    def generate(self) -> str:
        """Detect tech stack and generate pipeline configuration"""
        if not self.project_path.exists():
            raise ValueError(f"Project path does not exist: {self.project_path}")

        self.tech_stack = self.detect_tech_stack()

        if self.platform == "github":
            return self.generate_github_actions()
        elif self.platform == "gitlab":
            return self.generate_gitlab_ci()
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

    def detect_tech_stack(self) -> Dict:
        """Detect project's technology stack"""
        stack = {
            "language": None,
            "framework": None,
            "package_manager": None,
            "has_docker": False,
            "has_tests": False,
            "node_version": "20",
            "python_version": "3.11"
        }

        # Check for Node.js project
        if (self.project_path / "package.json").exists():
            stack.update(self._detect_node_project())

        # Check for Python project
        elif (self.project_path / "requirements.txt").exists() or \
             (self.project_path / "pyproject.toml").exists():
            stack.update(self._detect_python_project())

        # Check for Go project
        elif (self.project_path / "go.mod").exists():
            stack.update(self._detect_go_project())

        # Check for Dockerfile
        if (self.project_path / "Dockerfile").exists():
            stack["has_docker"] = True

        return stack

    def _detect_node_project(self) -> Dict:
        """Detect Node.js project details"""
        result = {
            "language": "node",
            "package_manager": "npm",
            "framework": None,
            "has_tests": False
        }

        package_json_path = self.project_path / "package.json"
        try:
            with open(package_json_path) as f:
                pkg = json.load(f)

            # Detect package manager
            if (self.project_path / "pnpm-lock.yaml").exists():
                result["package_manager"] = "pnpm"
            elif (self.project_path / "yarn.lock").exists():
                result["package_manager"] = "yarn"

            # Detect framework
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                result["framework"] = "nextjs"
            elif "react" in deps:
                result["framework"] = "react"
            elif "vue" in deps:
                result["framework"] = "vue"
            elif "express" in deps:
                result["framework"] = "express"

            # Check for test scripts
            scripts = pkg.get("scripts", {})
            if "test" in scripts:
                result["has_tests"] = True

            # Get Node version
            result["node_version"] = self._get_node_version()

        except (json.JSONDecodeError, FileNotFoundError):
            pass

        return result

    def _detect_python_project(self) -> Dict:
        """Detect Python project details"""
        result = {
            "language": "python",
            "package_manager": "pip",
            "framework": None,
            "has_tests": False
        }

        # Check for framework in requirements.txt
        req_path = self.project_path / "requirements.txt"
        if req_path.exists():
            try:
                with open(req_path) as f:
                    reqs = f.read().lower()
                    if "django" in reqs:
                        result["framework"] = "django"
                    elif "fastapi" in reqs:
                        result["framework"] = "fastapi"
                    elif "flask" in reqs:
                        result["framework"] = "flask"
                    if "pytest" in reqs:
                        result["has_tests"] = True
            except FileNotFoundError:
                pass

        # Check for poetry
        if (self.project_path / "poetry.lock").exists():
            result["package_manager"] = "poetry"

        # Get Python version
        result["python_version"] = self._get_python_version()

        return result

    def _detect_go_project(self) -> Dict:
        """Detect Go project details"""
        return {
            "language": "go",
            "package_manager": "go",
            "framework": None,
            "has_tests": (self.project_path / "**/*_test.go").exists()
        }

    def _get_node_version(self) -> str:
        """Get Node.js version from project"""
        nvmrc = self.project_path / ".nvmrc"
        if nvmrc.exists():
            try:
                return nvmrc.read_text().strip()
            except:
                pass

        # Default to LTS
        return "20"

    def _get_python_version(self) -> str:
        """Get Python version from project"""
        pyproject = self.project_path / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                # Simple extraction - look for python = "^3.x"
                import re
                match = re.search(r'python\s*=\s*"[\^~]?(3\.\d+)"', content)
                if match:
                    return match.group(1)
            except:
                pass

        return "3.11"

    def generate_github_actions(self) -> str:
        """Generate GitHub Actions workflow"""
        lines = [
            "name: CI",
            "",
            "on:",
            "  push:",
            "    branches: [main, develop]",
            "  pull_request:",
            "    branches: [main]",
            "",
            "env:"
        ]

        # Add environment variables based on stack
        if self.tech_stack["language"] == "node":
            lines.append(f"  NODE_VERSION: '{self.tech_stack.get('node_version', '20')}'")
        elif self.tech_stack["language"] == "python":
            lines.append(f"  PYTHON_VERSION: '{self.tech_stack.get('python_version', '3.11')}'")

        if self.with_docker:
            lines.extend([
                "  REGISTRY: ghcr.io",
                "  IMAGE_NAME: ${{ github.repository }}"
            ])

        lines.extend(["", "jobs:"])

        # Lint job
        lines.extend(self._github_lint_job())

        # Test job
        if self.tech_stack.get("has_tests"):
            lines.extend(self._github_test_job())

        # Build job (Docker)
        if self.with_docker or self.tech_stack.get("has_docker"):
            lines.extend(self._github_build_job())

        # Deploy job
        if self.with_deploy:
            lines.extend(self._github_deploy_job())

        return "\n".join(lines)

    def _github_lint_job(self) -> List[str]:
        """Generate GitHub Actions lint job"""
        lines = [
            "  lint:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4"
        ]

        if self.tech_stack["language"] == "node":
            pm = self.tech_stack.get("package_manager", "npm")
            lines.extend([
                "      - uses: actions/setup-node@v4",
                "        with:",
                "          node-version: ${{ env.NODE_VERSION }}",
                f"          cache: '{pm}'",
                f"      - run: {pm} {'install' if pm == 'npm' else 'install --frozen-lockfile' if pm == 'pnpm' else 'install --frozen-lockfile'}",
                f"      - run: {pm} run lint"
            ])
        elif self.tech_stack["language"] == "python":
            lines.extend([
                "      - uses: actions/setup-python@v5",
                "        with:",
                "          python-version: ${{ env.PYTHON_VERSION }}",
                "      - run: pip install ruff",
                "      - run: ruff check ."
            ])
        elif self.tech_stack["language"] == "go":
            lines.extend([
                "      - uses: actions/setup-go@v5",
                "        with:",
                "          go-version: '1.21'",
                "      - run: go vet ./..."
            ])

        lines.append("")
        return lines

    def _github_test_job(self) -> List[str]:
        """Generate GitHub Actions test job"""
        lines = [
            "  test:",
            "    runs-on: ubuntu-latest",
            "    needs: lint"
        ]

        # Add database service if needed
        if self.tech_stack.get("framework") in ["django", "express", "nextjs", "fastapi"]:
            lines.extend([
                "    services:",
                "      postgres:",
                "        image: postgres:15",
                "        env:",
                "          POSTGRES_PASSWORD: postgres",
                "          POSTGRES_DB: test",
                "        ports:",
                "          - 5432:5432",
                "        options: >-",
                "          --health-cmd pg_isready",
                "          --health-interval 10s",
                "          --health-timeout 5s",
                "          --health-retries 5"
            ])

        lines.append("    steps:")
        lines.append("      - uses: actions/checkout@v4")

        if self.tech_stack["language"] == "node":
            pm = self.tech_stack.get("package_manager", "npm")
            run_cmd = f"{pm} {'run test' if pm == 'npm' else 'test'}"
            lines.extend([
                "      - uses: actions/setup-node@v4",
                "        with:",
                "          node-version: ${{ env.NODE_VERSION }}",
                f"          cache: '{pm}'",
                f"      - run: {pm} {'ci' if pm == 'npm' else 'install --frozen-lockfile'}",
                f"      - run: {run_cmd}",
                "        env:",
                "          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test"
            ])
        elif self.tech_stack["language"] == "python":
            lines.extend([
                "      - uses: actions/setup-python@v5",
                "        with:",
                "          python-version: ${{ env.PYTHON_VERSION }}",
                "      - run: pip install -r requirements.txt",
                "      - run: pip install pytest pytest-cov",
                "      - run: pytest --cov=. --cov-report=xml",
                "        env:",
                "          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test"
            ])
        elif self.tech_stack["language"] == "go":
            lines.extend([
                "      - uses: actions/setup-go@v5",
                "        with:",
                "          go-version: '1.21'",
                "      - run: go test -v -race -coverprofile=coverage.out ./..."
            ])

        lines.append("")
        return lines

    def _github_build_job(self) -> List[str]:
        """Generate GitHub Actions Docker build job"""
        return [
            "  build:",
            "    runs-on: ubuntu-latest",
            "    needs: " + ("test" if self.tech_stack.get("has_tests") else "lint"),
            "    permissions:",
            "      contents: read",
            "      packages: write",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "",
            "      - name: Set up Docker Buildx",
            "        uses: docker/setup-buildx-action@v3",
            "",
            "      - name: Log in to Container Registry",
            "        uses: docker/login-action@v3",
            "        with:",
            "          registry: ${{ env.REGISTRY }}",
            "          username: ${{ github.actor }}",
            "          password: ${{ secrets.GITHUB_TOKEN }}",
            "",
            "      - name: Extract metadata",
            "        id: meta",
            "        uses: docker/metadata-action@v5",
            "        with:",
            "          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}",
            "          tags: |",
            "            type=sha,prefix=",
            "            type=ref,event=branch",
            "",
            "      - name: Build and push",
            "        uses: docker/build-push-action@v5",
            "        with:",
            "          context: .",
            "          push: ${{ github.event_name != 'pull_request' }}",
            "          tags: ${{ steps.meta.outputs.tags }}",
            "          labels: ${{ steps.meta.outputs.labels }}",
            "          cache-from: type=gha",
            "          cache-to: type=gha,mode=max",
            ""
        ]

    def _github_deploy_job(self) -> List[str]:
        """Generate GitHub Actions deployment job"""
        return [
            f"  deploy-{self.environment}:",
            "    runs-on: ubuntu-latest",
            "    needs: build",
            "    if: github.ref == 'refs/heads/main'",
            f"    environment: {self.environment}",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "",
            "      - name: Configure AWS credentials",
            "        uses: aws-actions/configure-aws-credentials@v4",
            "        with:",
            "          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}",
            "          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}",
            "          aws-region: us-east-1",
            "",
            "      - name: Deploy to ECS",
            "        run: |",
            "          aws ecs update-service \\",
            f"            --cluster {self.environment}-cluster \\",
            "            --service app-service \\",
            "            --force-new-deployment",
            "",
            "      - name: Wait for deployment",
            "        run: |",
            "          aws ecs wait services-stable \\",
            f"            --cluster {self.environment}-cluster \\",
            "            --services app-service",
            ""
        ]

    def generate_gitlab_ci(self) -> str:
        """Generate GitLab CI configuration"""
        lines = [
            "stages:",
            "  - lint",
            "  - test",
        ]

        if self.with_docker or self.tech_stack.get("has_docker"):
            lines.append("  - build")

        if self.with_deploy:
            lines.append("  - deploy")

        lines.extend([
            "",
            "variables:",
            "  DOCKER_TLS_CERTDIR: \"/certs\""
        ])

        if self.with_docker:
            lines.append("  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA")

        lines.append("")

        # Cache configuration for Node.js
        if self.tech_stack["language"] == "node":
            lines.extend([
                ".node-cache: &node-cache",
                "  cache:",
                "    key: ${CI_COMMIT_REF_SLUG}",
                "    paths:",
                "      - node_modules/",
                ""
            ])

        # Lint job
        lines.extend(self._gitlab_lint_job())

        # Test job
        if self.tech_stack.get("has_tests"):
            lines.extend(self._gitlab_test_job())

        # Build job
        if self.with_docker or self.tech_stack.get("has_docker"):
            lines.extend(self._gitlab_build_job())

        # Deploy job
        if self.with_deploy:
            lines.extend(self._gitlab_deploy_job())

        return "\n".join(lines)

    def _gitlab_lint_job(self) -> List[str]:
        """Generate GitLab CI lint job"""
        lines = ["lint:"]
        lines.append("  stage: lint")

        if self.tech_stack["language"] == "node":
            lines.extend([
                f"  image: node:{self.tech_stack.get('node_version', '20')}-alpine",
                "  <<: *node-cache",
                "  script:",
                f"    - npm ci",
                "    - npm run lint"
            ])
        elif self.tech_stack["language"] == "python":
            lines.extend([
                f"  image: python:{self.tech_stack.get('python_version', '3.11')}-slim",
                "  script:",
                "    - pip install ruff",
                "    - ruff check ."
            ])
        elif self.tech_stack["language"] == "go":
            lines.extend([
                "  image: golang:1.21",
                "  script:",
                "    - go vet ./..."
            ])

        lines.extend([
            "  rules:",
            "    - if: $CI_PIPELINE_SOURCE == \"merge_request_event\"",
            "    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH",
            ""
        ])
        return lines

    def _gitlab_test_job(self) -> List[str]:
        """Generate GitLab CI test job"""
        lines = [
            "test:",
            "  stage: test"
        ]

        if self.tech_stack["language"] == "node":
            lines.extend([
                f"  image: node:{self.tech_stack.get('node_version', '20')}-alpine",
                "  <<: *node-cache",
                "  services:",
                "    - postgres:15",
                "  variables:",
                "    POSTGRES_DB: test",
                "    POSTGRES_PASSWORD: postgres",
                "    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test",
                "  script:",
                "    - npm ci",
                "    - npm run test:coverage",
                "  coverage: '/Lines\\s*:\\s*(\\d+\\.?\\d*)%/'"
            ])
        elif self.tech_stack["language"] == "python":
            lines.extend([
                f"  image: python:{self.tech_stack.get('python_version', '3.11')}-slim",
                "  services:",
                "    - postgres:15",
                "  variables:",
                "    POSTGRES_DB: test",
                "    POSTGRES_PASSWORD: postgres",
                "    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test",
                "  script:",
                "    - pip install -r requirements.txt",
                "    - pip install pytest pytest-cov",
                "    - pytest --cov=. --cov-report=xml",
                "  coverage: '/TOTAL.*\\s+(\\d+%)$/'"
            ])

        lines.append("")
        return lines

    def _gitlab_build_job(self) -> List[str]:
        """Generate GitLab CI Docker build job"""
        return [
            "build:",
            "  stage: build",
            "  image: docker:24",
            "  services:",
            "    - docker:24-dind",
            "  before_script:",
            "    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY",
            "  script:",
            "    - docker build -t $IMAGE_TAG .",
            "    - docker push $IMAGE_TAG",
            "  rules:",
            "    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH",
            ""
        ]

    def _gitlab_deploy_job(self) -> List[str]:
        """Generate GitLab CI deployment job"""
        return [
            f"deploy:{self.environment}:",
            "  stage: deploy",
            "  image: alpine/k8s:1.28.0",
            "  environment:",
            f"    name: {self.environment}",
            f"    url: https://{self.environment}.example.com",
            "  script:",
            f"    - kubectl set image deployment/app app=$IMAGE_TAG -n {self.environment}",
            f"    - kubectl rollout status deployment/app -n {self.environment} --timeout=300s",
            "  rules:",
            "    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH",
            "      when: " + ("manual" if self.environment == "production" else "on_success"),
            ""
        ]


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate CI/CD pipeline configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./my-project --platform github
  %(prog)s ./api --platform gitlab --with-docker
  %(prog)s . --platform github --with-docker --with-deploy --env production
        """
    )
    parser.add_argument(
        'project_path',
        help='Path to the project to analyze'
    )
    parser.add_argument(
        '--platform',
        choices=['github', 'gitlab'],
        default='github',
        help='CI/CD platform (default: github)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--with-docker',
        action='store_true',
        help='Include Docker build stage'
    )
    parser.add_argument(
        '--with-deploy',
        action='store_true',
        help='Include deployment stage'
    )
    parser.add_argument(
        '--env',
        choices=['staging', 'production'],
        default='staging',
        help='Deployment environment (default: staging)'
    )

    args = parser.parse_args()

    try:
        generator = PipelineGenerator(
            args.project_path,
            platform=args.platform,
            with_docker=args.with_docker,
            with_deploy=args.with_deploy,
            environment=args.env
        )

        output = generator.generate()

        # Show detected stack info
        print(f"# Detected: {generator.tech_stack.get('language', 'unknown')} "
              f"({generator.tech_stack.get('framework', 'no framework')})", file=sys.stderr)
        print(f"# Package manager: {generator.tech_stack.get('package_manager', 'unknown')}", file=sys.stderr)
        print(f"# Has tests: {generator.tech_stack.get('has_tests', False)}", file=sys.stderr)
        print(f"# Has Docker: {generator.tech_stack.get('has_docker', False)}", file=sys.stderr)
        print("", file=sys.stderr)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output)
            print(f"Pipeline written to: {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
