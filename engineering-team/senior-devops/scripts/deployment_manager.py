#!/usr/bin/env python3
"""
Deployment Manager - Orchestrate deployments with blue-green, canary, and rolling strategies.

Table of Contents:
    DeploymentManager - Main class for deployment orchestration
        __init__             - Initialize with deployment configuration
        deploy()             - Execute deployment with selected strategy
        _validate_config()   - Validate deployment configuration
        _blue_green_deploy() - Execute blue-green deployment
        _canary_deploy()     - Execute canary deployment with traffic shifting
        _rolling_deploy()    - Execute rolling update deployment
        _check_health()      - Verify deployment health
        _rollback()          - Execute rollback procedure
        status()             - Get current deployment status
        generate_manifest()  - Generate Kubernetes deployment manifest
    main() - CLI entry point

Supported Platforms:
    - Kubernetes (kubectl)
    - AWS ECS (aws cli)
    - AWS Lambda (aws cli)

Usage:
    python deployment_manager.py deploy --strategy blue-green --image myapp:v2
    python deployment_manager.py deploy --strategy canary --image myapp:v2 --canary-percent 10
    python deployment_manager.py deploy --strategy rolling --image myapp:v2
    python deployment_manager.py status --deployment myapp
    python deployment_manager.py rollback --deployment myapp
"""

import os
import sys
import json
import argparse
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class DeploymentConfig:
    """Configuration for a deployment."""
    name: str
    namespace: str = "default"
    image: str = ""
    replicas: int = 3
    port: int = 8080
    health_path: str = "/health"
    strategy: str = "rolling"  # rolling, blue-green, canary
    canary_percent: int = 10
    canary_steps: List[int] = None
    platform: str = "kubernetes"  # kubernetes, ecs

    def __post_init__(self):
        if self.canary_steps is None:
            self.canary_steps = [10, 25, 50, 100]


class DeploymentManager:
    """Orchestrate deployments with blue-green, canary, and rolling strategies."""

    def __init__(self, config: DeploymentConfig, verbose: bool = False, dry_run: bool = False):
        """
        Initialize deployment manager.

        Args:
            config: Deployment configuration
            verbose: Enable verbose output
            dry_run: Preview commands without executing
        """
        self.config = config
        self.verbose = verbose
        self.dry_run = dry_run
        self.deployment_history = []

    def deploy(self) -> Dict:
        """
        Execute deployment with selected strategy.

        Returns:
            Dict with deployment status and details
        """
        print(f"Starting {self.config.strategy} deployment for {self.config.name}")
        print(f"Image: {self.config.image}")
        print(f"Platform: {self.config.platform}")
        print()

        if not self._validate_config():
            return {"status": "error", "message": "Invalid configuration"}

        try:
            if self.config.strategy == "blue-green":
                result = self._blue_green_deploy()
            elif self.config.strategy == "canary":
                result = self._canary_deploy()
            else:
                result = self._rolling_deploy()

            self.deployment_history.append({
                "timestamp": datetime.now().isoformat(),
                "strategy": self.config.strategy,
                "image": self.config.image,
                "result": result["status"]
            })

            return result

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _validate_config(self) -> bool:
        """Validate deployment configuration."""
        if not self.config.name:
            print("Error: Deployment name is required")
            return False

        if not self.config.image:
            print("Error: Container image is required")
            return False

        if self.config.strategy not in ["rolling", "blue-green", "canary"]:
            print(f"Error: Invalid strategy '{self.config.strategy}'")
            return False

        return True

    def _run_command(self, cmd: List[str], description: str = "") -> Tuple[bool, str]:
        """Run a shell command and return success status and output."""
        cmd_str = " ".join(cmd)

        if self.verbose or self.dry_run:
            print(f"  $ {cmd_str}")

        if self.dry_run:
            return True, "[dry-run] Command not executed"

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)

    def _blue_green_deploy(self) -> Dict:
        """
        Execute blue-green deployment.

        Steps:
        1. Deploy new version to green environment
        2. Run health checks on green
        3. Switch traffic from blue to green
        4. Keep blue running for rollback
        """
        print("Executing blue-green deployment...")

        steps = []
        green_name = f"{self.config.name}-green"
        blue_name = f"{self.config.name}-blue"

        # Step 1: Deploy green environment
        print("\n[1/4] Deploying green environment...")
        manifest = self._generate_deployment_manifest(green_name)

        if self.config.platform == "kubernetes":
            success, output = self._run_command(
                ["kubectl", "apply", "-f", "-", "--namespace", self.config.namespace],
                "Apply green deployment"
            )
            steps.append({"step": "deploy_green", "success": success})

            if not success and not self.dry_run:
                return {"status": "error", "message": f"Failed to deploy green: {output}", "steps": steps}

        # Step 2: Wait for green to be ready
        print("\n[2/4] Waiting for green deployment to be ready...")
        if self.config.platform == "kubernetes" and not self.dry_run:
            success, output = self._run_command(
                ["kubectl", "rollout", "status", f"deployment/{green_name}",
                 "--namespace", self.config.namespace, "--timeout=300s"],
                "Wait for rollout"
            )
            steps.append({"step": "wait_green_ready", "success": success})

            if not success:
                print("Green deployment failed, initiating rollback...")
                self._cleanup_deployment(green_name)
                return {"status": "error", "message": "Green deployment failed", "steps": steps}
        else:
            steps.append({"step": "wait_green_ready", "success": True})

        # Step 3: Health check
        print("\n[3/4] Running health checks on green...")
        health_ok = self._check_health(green_name)
        steps.append({"step": "health_check", "success": health_ok})

        if not health_ok and not self.dry_run:
            print("Health check failed, cleaning up green...")
            self._cleanup_deployment(green_name)
            return {"status": "error", "message": "Health check failed", "steps": steps}

        # Step 4: Switch traffic
        print("\n[4/4] Switching traffic to green...")
        if self.config.platform == "kubernetes":
            # Update service selector to point to green
            success, output = self._run_command(
                ["kubectl", "patch", "service", self.config.name,
                 "--namespace", self.config.namespace,
                 "-p", f'{{"spec":{{"selector":{{"version":"green"}}}}}}'],
                "Switch service to green"
            )
            steps.append({"step": "switch_traffic", "success": success})

        print("\nBlue-green deployment completed successfully!")
        print(f"Green deployment ({green_name}) is now serving traffic")
        print(f"Blue deployment ({blue_name}) kept for rollback")

        return {
            "status": "success",
            "strategy": "blue-green",
            "active": green_name,
            "standby": blue_name,
            "steps": steps
        }

    def _canary_deploy(self) -> Dict:
        """
        Execute canary deployment with gradual traffic shifting.

        Steps:
        1. Deploy canary with small percentage of traffic
        2. Monitor metrics and health
        3. Gradually increase traffic
        4. Complete rollout or rollback
        """
        print("Executing canary deployment...")
        print(f"Canary steps: {self.config.canary_steps}%")

        steps = []
        canary_name = f"{self.config.name}-canary"

        # Step 1: Deploy canary
        print("\n[1/N] Deploying canary version...")

        if self.config.platform == "kubernetes":
            # Create canary deployment with 1 replica
            canary_manifest = self._generate_deployment_manifest(canary_name, replicas=1)
            success, output = self._run_command(
                ["kubectl", "apply", "-f", "-", "--namespace", self.config.namespace],
                "Apply canary deployment"
            )
            steps.append({"step": "deploy_canary", "success": success, "replicas": 1})

        # Step 2: Progressive traffic shift
        for i, percentage in enumerate(self.config.canary_steps):
            print(f"\n[{i+2}/N] Shifting {percentage}% traffic to canary...")

            if self.config.platform == "kubernetes":
                # Scale canary replicas proportionally
                canary_replicas = max(1, int(self.config.replicas * percentage / 100))
                stable_replicas = self.config.replicas - canary_replicas

                success, _ = self._run_command(
                    ["kubectl", "scale", f"deployment/{canary_name}",
                     f"--replicas={canary_replicas}", "--namespace", self.config.namespace],
                    f"Scale canary to {canary_replicas}"
                )

                success, _ = self._run_command(
                    ["kubectl", "scale", f"deployment/{self.config.name}",
                     f"--replicas={stable_replicas}", "--namespace", self.config.namespace],
                    f"Scale stable to {stable_replicas}"
                )

            # Health check at each step
            print(f"  Checking health at {percentage}%...")
            health_ok = self._check_health(canary_name)
            steps.append({
                "step": f"canary_{percentage}%",
                "success": health_ok,
                "canary_replicas": canary_replicas if self.config.platform == "kubernetes" else 0
            })

            if not health_ok and not self.dry_run:
                print(f"Health check failed at {percentage}%, rolling back...")
                self._rollback_canary(canary_name)
                return {
                    "status": "error",
                    "message": f"Canary failed at {percentage}%",
                    "steps": steps
                }

            if percentage < 100:
                print(f"  Success! Waiting before next step...")
                if not self.dry_run:
                    time.sleep(30)  # Wait between steps

        # Step 3: Complete promotion
        print("\n[Final] Promoting canary to stable...")
        if self.config.platform == "kubernetes":
            # Update stable deployment with new image
            success, _ = self._run_command(
                ["kubectl", "set", "image", f"deployment/{self.config.name}",
                 f"app={self.config.image}", "--namespace", self.config.namespace],
                "Update stable deployment"
            )

            # Scale stable back up
            success, _ = self._run_command(
                ["kubectl", "scale", f"deployment/{self.config.name}",
                 f"--replicas={self.config.replicas}", "--namespace", self.config.namespace],
                "Scale stable to full"
            )

            # Remove canary
            self._cleanup_deployment(canary_name)

        print("\nCanary deployment completed successfully!")

        return {
            "status": "success",
            "strategy": "canary",
            "image": self.config.image,
            "steps": steps
        }

    def _rolling_deploy(self) -> Dict:
        """
        Execute rolling update deployment.

        Steps:
        1. Update deployment with new image
        2. Kubernetes handles rolling update automatically
        3. Monitor rollout status
        """
        print("Executing rolling deployment...")

        steps = []

        if self.config.platform == "kubernetes":
            # Update image
            print("\n[1/2] Updating deployment image...")
            success, output = self._run_command(
                ["kubectl", "set", "image", f"deployment/{self.config.name}",
                 f"app={self.config.image}", "--namespace", self.config.namespace],
                "Update deployment image"
            )
            steps.append({"step": "update_image", "success": success})

            if not success and not self.dry_run:
                return {"status": "error", "message": f"Failed to update image: {output}", "steps": steps}

            # Wait for rollout
            print("\n[2/2] Waiting for rollout to complete...")
            success, output = self._run_command(
                ["kubectl", "rollout", "status", f"deployment/{self.config.name}",
                 "--namespace", self.config.namespace, "--timeout=600s"],
                "Wait for rollout"
            )
            steps.append({"step": "rollout_status", "success": success})

            if not success and not self.dry_run:
                print("Rollout failed, initiating rollback...")
                self._run_command(
                    ["kubectl", "rollout", "undo", f"deployment/{self.config.name}",
                     "--namespace", self.config.namespace],
                    "Rollback deployment"
                )
                return {"status": "error", "message": "Rollout failed, rolled back", "steps": steps}

        elif self.config.platform == "ecs":
            print("\n[1/2] Updating ECS service...")
            success, output = self._run_command(
                ["aws", "ecs", "update-service",
                 "--cluster", self.config.namespace,
                 "--service", self.config.name,
                 "--force-new-deployment"],
                "Update ECS service"
            )
            steps.append({"step": "update_service", "success": success})

            print("\n[2/2] Waiting for service stability...")
            success, output = self._run_command(
                ["aws", "ecs", "wait", "services-stable",
                 "--cluster", self.config.namespace,
                 "--services", self.config.name],
                "Wait for service stability"
            )
            steps.append({"step": "wait_stable", "success": success})

        print("\nRolling deployment completed successfully!")

        return {
            "status": "success",
            "strategy": "rolling",
            "image": self.config.image,
            "steps": steps
        }

    def _check_health(self, deployment_name: str) -> bool:
        """Check health of a deployment."""
        if self.dry_run:
            print("  [dry-run] Skipping health check")
            return True

        if self.config.platform == "kubernetes":
            # Check pod status
            success, output = self._run_command(
                ["kubectl", "get", "pods", "-l", f"app={deployment_name}",
                 "--namespace", self.config.namespace, "-o", "json"],
                "Get pod status"
            )

            if not success:
                return False

            try:
                pods = json.loads(output)
                for pod in pods.get("items", []):
                    status = pod.get("status", {}).get("phase")
                    if status != "Running":
                        return False

                    # Check container readiness
                    for container in pod.get("status", {}).get("containerStatuses", []):
                        if not container.get("ready", False):
                            return False
            except json.JSONDecodeError:
                return False

        return True

    def _cleanup_deployment(self, deployment_name: str):
        """Remove a deployment."""
        if self.config.platform == "kubernetes":
            self._run_command(
                ["kubectl", "delete", "deployment", deployment_name,
                 "--namespace", self.config.namespace, "--ignore-not-found"],
                f"Delete deployment {deployment_name}"
            )

    def _rollback_canary(self, canary_name: str):
        """Rollback canary deployment."""
        print("Rolling back canary...")

        # Remove canary
        self._cleanup_deployment(canary_name)

        # Scale stable back to full
        if self.config.platform == "kubernetes":
            self._run_command(
                ["kubectl", "scale", f"deployment/{self.config.name}",
                 f"--replicas={self.config.replicas}", "--namespace", self.config.namespace],
                "Scale stable to full"
            )

    def _rollback(self) -> Dict:
        """Execute rollback to previous version."""
        print(f"Rolling back {self.config.name}...")

        if self.config.platform == "kubernetes":
            success, output = self._run_command(
                ["kubectl", "rollout", "undo", f"deployment/{self.config.name}",
                 "--namespace", self.config.namespace],
                "Rollback deployment"
            )

            if success:
                return {"status": "success", "message": "Rollback completed"}
            else:
                return {"status": "error", "message": f"Rollback failed: {output}"}

        return {"status": "error", "message": "Rollback not implemented for this platform"}

    def status(self) -> Dict:
        """Get current deployment status."""
        if self.config.platform == "kubernetes":
            success, output = self._run_command(
                ["kubectl", "get", "deployment", self.config.name,
                 "--namespace", self.config.namespace, "-o", "json"],
                "Get deployment status"
            )

            if success:
                try:
                    deployment = json.loads(output)
                    spec = deployment.get("spec", {})
                    status = deployment.get("status", {})

                    return {
                        "name": self.config.name,
                        "namespace": self.config.namespace,
                        "replicas": spec.get("replicas", 0),
                        "ready": status.get("readyReplicas", 0),
                        "available": status.get("availableReplicas", 0),
                        "image": spec.get("template", {}).get("spec", {})
                            .get("containers", [{}])[0].get("image", "unknown"),
                        "conditions": status.get("conditions", [])
                    }
                except json.JSONDecodeError:
                    pass

        return {"status": "error", "message": "Could not get deployment status"}

    def _generate_deployment_manifest(self, name: str, replicas: int = None) -> str:
        """Generate Kubernetes deployment manifest."""
        if replicas is None:
            replicas = self.config.replicas

        manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": name,
                "namespace": self.config.namespace,
                "labels": {
                    "app": name
                }
            },
            "spec": {
                "replicas": replicas,
                "selector": {
                    "matchLabels": {
                        "app": name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": name
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": "app",
                            "image": self.config.image,
                            "ports": [{
                                "containerPort": self.config.port
                            }],
                            "readinessProbe": {
                                "httpGet": {
                                    "path": self.config.health_path,
                                    "port": self.config.port
                                },
                                "initialDelaySeconds": 10,
                                "periodSeconds": 5
                            },
                            "livenessProbe": {
                                "httpGet": {
                                    "path": self.config.health_path,
                                    "port": self.config.port
                                },
                                "initialDelaySeconds": 30,
                                "periodSeconds": 10
                            },
                            "resources": {
                                "requests": {
                                    "cpu": "100m",
                                    "memory": "128Mi"
                                },
                                "limits": {
                                    "cpu": "500m",
                                    "memory": "512Mi"
                                }
                            }
                        }]
                    }
                }
            }
        }

        return json.dumps(manifest, indent=2)

    def generate_manifest(self) -> str:
        """Generate and return deployment manifest."""
        return self._generate_deployment_manifest(self.config.name)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Orchestrate deployments with blue-green, canary, and rolling strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s deploy --name myapp --image myapp:v2 --strategy rolling
  %(prog)s deploy --name myapp --image myapp:v2 --strategy blue-green
  %(prog)s deploy --name myapp --image myapp:v2 --strategy canary --canary-steps 10,25,50,100
  %(prog)s status --name myapp
  %(prog)s rollback --name myapp
  %(prog)s manifest --name myapp --image myapp:v2
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Execute a deployment")
    deploy_parser.add_argument("--name", "-n", required=True, help="Deployment name")
    deploy_parser.add_argument("--namespace", "-ns", default="default", help="Kubernetes namespace")
    deploy_parser.add_argument("--image", "-i", required=True, help="Container image")
    deploy_parser.add_argument("--replicas", "-r", type=int, default=3, help="Number of replicas")
    deploy_parser.add_argument("--port", "-p", type=int, default=8080, help="Container port")
    deploy_parser.add_argument("--health-path", default="/health", help="Health check path")
    deploy_parser.add_argument("--strategy", "-s", choices=["rolling", "blue-green", "canary"],
                               default="rolling", help="Deployment strategy")
    deploy_parser.add_argument("--canary-steps", help="Canary traffic percentages (e.g., 10,25,50,100)")
    deploy_parser.add_argument("--platform", choices=["kubernetes", "ecs"],
                               default="kubernetes", help="Deployment platform")
    deploy_parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    deploy_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get deployment status")
    status_parser.add_argument("--name", "-n", required=True, help="Deployment name")
    status_parser.add_argument("--namespace", "-ns", default="default", help="Kubernetes namespace")
    status_parser.add_argument("--platform", choices=["kubernetes", "ecs"],
                               default="kubernetes", help="Deployment platform")

    # Rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Rollback deployment")
    rollback_parser.add_argument("--name", "-n", required=True, help="Deployment name")
    rollback_parser.add_argument("--namespace", "-ns", default="default", help="Kubernetes namespace")
    rollback_parser.add_argument("--platform", choices=["kubernetes", "ecs"],
                                 default="kubernetes", help="Deployment platform")
    rollback_parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    rollback_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # Manifest command
    manifest_parser = subparsers.add_parser("manifest", help="Generate deployment manifest")
    manifest_parser.add_argument("--name", "-n", required=True, help="Deployment name")
    manifest_parser.add_argument("--namespace", "-ns", default="default", help="Kubernetes namespace")
    manifest_parser.add_argument("--image", "-i", required=True, help="Container image")
    manifest_parser.add_argument("--replicas", "-r", type=int, default=3, help="Number of replicas")
    manifest_parser.add_argument("--port", "-p", type=int, default=8080, help="Container port")
    manifest_parser.add_argument("--health-path", default="/health", help="Health check path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Create config based on command
    if args.command in ["deploy", "manifest"]:
        canary_steps = None
        if hasattr(args, "canary_steps") and args.canary_steps:
            canary_steps = [int(x) for x in args.canary_steps.split(",")]

        config = DeploymentConfig(
            name=args.name,
            namespace=args.namespace,
            image=args.image,
            replicas=args.replicas,
            port=args.port,
            health_path=args.health_path,
            strategy=getattr(args, "strategy", "rolling"),
            canary_steps=canary_steps,
            platform=getattr(args, "platform", "kubernetes")
        )
    else:
        config = DeploymentConfig(
            name=args.name,
            namespace=args.namespace,
            platform=getattr(args, "platform", "kubernetes")
        )

    manager = DeploymentManager(
        config,
        verbose=getattr(args, "verbose", False),
        dry_run=getattr(args, "dry_run", False)
    )

    # Execute command
    if args.command == "deploy":
        result = manager.deploy()
    elif args.command == "status":
        result = manager.status()
    elif args.command == "rollback":
        result = manager._rollback()
    elif args.command == "manifest":
        print(manager.generate_manifest())
        sys.exit(0)

    # Output result
    print("\n" + "=" * 50)
    print("Result:")
    print(json.dumps(result, indent=2))

    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
