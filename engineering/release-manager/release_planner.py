#!/usr/bin/env python3
"""
Release Planner

Takes a list of features/PRs/tickets planned for release and assesses release readiness.
Checks for required approvals, test coverage thresholds, breaking change documentation,
dependency updates, migration steps needed. Generates release checklist, communication
plan, and rollback procedures.

Input: release plan JSON (features, PRs, target date)
Output: release readiness report + checklist + rollback runbook + announcement draft
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum


class RiskLevel(Enum):
    """Risk levels for release components."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComponentStatus(Enum):
    """Status of release components."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class Feature:
    """Represents a feature in the release."""
    id: str
    title: str
    description: str
    type: str  # feature, bugfix, security, breaking_change, etc.
    assignee: str
    status: ComponentStatus
    pull_request_url: Optional[str] = None
    issue_url: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    test_coverage_required: float = 80.0
    test_coverage_actual: Optional[float] = None
    requires_migration: bool = False
    migration_complexity: str = "simple"  # simple, moderate, complex
    breaking_changes: List[str] = None
    dependencies: List[str] = None
    qa_approved: bool = False
    security_approved: bool = False
    pm_approved: bool = False
    
    def __post_init__(self):
        if self.breaking_changes is None:
            self.breaking_changes = []
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class QualityGate:
    """Quality gate requirements."""
    name: str
    required: bool
    status: ComponentStatus
    details: Optional[str] = None
    threshold: Optional[float] = None
    actual_value: Optional[float] = None


@dataclass
class Stakeholder:
    """Stakeholder for release communication."""
    name: str
    role: str
    contact: str
    notification_type: str  # email, slack, teams
    critical_path: bool = False


@dataclass
class RollbackStep:
    """Individual rollback step."""
    order: int
    description: str
    command: Optional[str] = None
    estimated_time: str = "5 minutes"
    risk_level: RiskLevel = RiskLevel.LOW
    verification: str = ""


class ReleasePlanner:
    """Main release planning and assessment logic."""
    
    def __init__(self):
        self.release_name: str = ""
        self.version: str = ""
        self.target_date: Optional[datetime] = None
        self.features: List[Feature] = []
        self.quality_gates: List[QualityGate] = []
        self.stakeholders: List[Stakeholder] = []
        self.rollback_steps: List[RollbackStep] = []
        
        # Configuration
        self.min_test_coverage = 80.0
        self.required_approvals = ['pm_approved', 'qa_approved']
        self.high_risk_approval_requirements = ['pm_approved', 'qa_approved', 'security_approved']
        
    def load_release_plan(self, plan_data: Union[str, Dict]):
        """Load release plan from JSON."""
        if isinstance(plan_data, str):
            data = json.loads(plan_data)
        else:
            data = plan_data
        
        self.release_name = data.get('release_name', 'Unnamed Release')
        self.version = data.get('version', '1.0.0')
        
        if 'target_date' in data:
            self.target_date = datetime.fromisoformat(data['target_date'].replace('Z', '+00:00'))
        
        # Load features
        self.features = []
        for feature_data in data.get('features', []):
            try:
                status = ComponentStatus(feature_data.get('status', 'pending'))
                risk_level = RiskLevel(feature_data.get('risk_level', 'medium'))
                
                feature = Feature(
                    id=feature_data['id'],
                    title=feature_data['title'],
                    description=feature_data.get('description', ''),
                    type=feature_data.get('type', 'feature'),
                    assignee=feature_data.get('assignee', ''),
                    status=status,
                    pull_request_url=feature_data.get('pull_request_url'),
                    issue_url=feature_data.get('issue_url'),
                    risk_level=risk_level,
                    test_coverage_required=feature_data.get('test_coverage_required', 80.0),
                    test_coverage_actual=feature_data.get('test_coverage_actual'),
                    requires_migration=feature_data.get('requires_migration', False),
                    migration_complexity=feature_data.get('migration_complexity', 'simple'),
                    breaking_changes=feature_data.get('breaking_changes', []),
                    dependencies=feature_data.get('dependencies', []),
                    qa_approved=feature_data.get('qa_approved', False),
                    security_approved=feature_data.get('security_approved', False),
                    pm_approved=feature_data.get('pm_approved', False)
                )
                self.features.append(feature)
            except Exception as e:
                print(f"Warning: Error parsing feature {feature_data.get('id', 'unknown')}: {e}", 
                      file=sys.stderr)
        
        # Load quality gates
        self.quality_gates = []
        for gate_data in data.get('quality_gates', []):
            try:
                status = ComponentStatus(gate_data.get('status', 'pending'))
                gate = QualityGate(
                    name=gate_data['name'],
                    required=gate_data.get('required', True),
                    status=status,
                    details=gate_data.get('details'),
                    threshold=gate_data.get('threshold'),
                    actual_value=gate_data.get('actual_value')
                )
                self.quality_gates.append(gate)
            except Exception as e:
                print(f"Warning: Error parsing quality gate {gate_data.get('name', 'unknown')}: {e}", 
                      file=sys.stderr)
        
        # Load stakeholders
        self.stakeholders = []
        for stakeholder_data in data.get('stakeholders', []):
            stakeholder = Stakeholder(
                name=stakeholder_data['name'],
                role=stakeholder_data['role'],
                contact=stakeholder_data['contact'],
                notification_type=stakeholder_data.get('notification_type', 'email'),
                critical_path=stakeholder_data.get('critical_path', False)
            )
            self.stakeholders.append(stakeholder)
        
        # Load or generate default quality gates if none provided
        if not self.quality_gates:
            self._generate_default_quality_gates()
        
        # Load or generate default rollback steps
        if 'rollback_steps' in data:
            self.rollback_steps = []
            for step_data in data['rollback_steps']:
                risk_level = RiskLevel(step_data.get('risk_level', 'low'))
                step = RollbackStep(
                    order=step_data['order'],
                    description=step_data['description'],
                    command=step_data.get('command'),
                    estimated_time=step_data.get('estimated_time', '5 minutes'),
                    risk_level=risk_level,
                    verification=step_data.get('verification', '')
                )
                self.rollback_steps.append(step)
        else:
            self._generate_default_rollback_steps()
    
    def _generate_default_quality_gates(self):
        """Generate default quality gates."""
        default_gates = [
            {
                'name': 'Unit Test Coverage',
                'required': True,
                'threshold': self.min_test_coverage,
                'details': f'Minimum {self.min_test_coverage}% code coverage required'
            },
            {
                'name': 'Integration Tests',
                'required': True,
                'details': 'All integration tests must pass'
            },
            {
                'name': 'Security Scan',
                'required': True,
                'details': 'No high or critical security vulnerabilities'
            },
            {
                'name': 'Performance Testing',
                'required': True,
                'details': 'Performance metrics within acceptable thresholds'
            },
            {
                'name': 'Documentation Review',
                'required': True,
                'details': 'API docs and user docs updated for new features'
            },
            {
                'name': 'Dependency Audit',
                'required': True,
                'details': 'All dependencies scanned for vulnerabilities'
            }
        ]
        
        self.quality_gates = []
        for gate_data in default_gates:
            gate = QualityGate(
                name=gate_data['name'],
                required=gate_data['required'],
                status=ComponentStatus.PENDING,
                details=gate_data['details'],
                threshold=gate_data.get('threshold')
            )
            self.quality_gates.append(gate)
    
    def _generate_default_rollback_steps(self):
        """Generate default rollback procedure."""
        default_steps = [
            {
                'order': 1,
                'description': 'Alert on-call team and stakeholders',
                'estimated_time': '2 minutes',
                'verification': 'Confirm team is aware and responding'
            },
            {
                'order': 2,
                'description': 'Switch load balancer to previous version',
                'command': 'kubectl patch service app --patch \'{"spec": {"selector": {"version": "previous"}}}\'',
                'estimated_time': '30 seconds',
                'verification': 'Check that traffic is routing to old version'
            },
            {
                'order': 3,
                'description': 'Verify application health after rollback',
                'estimated_time': '5 minutes',
                'verification': 'Check error rates, response times, and health endpoints'
            },
            {
                'order': 4,
                'description': 'Roll back database migrations if needed',
                'command': 'python manage.py migrate app 0001',
                'estimated_time': '10 minutes',
                'risk_level': 'high',
                'verification': 'Verify data integrity and application functionality'
            },
            {
                'order': 5,
                'description': 'Update monitoring dashboards and alerts',
                'estimated_time': '5 minutes',
                'verification': 'Confirm metrics reflect rollback state'
            },
            {
                'order': 6,
                'description': 'Notify stakeholders of successful rollback',
                'estimated_time': '5 minutes',
                'verification': 'All stakeholders acknowledge rollback completion'
            }
        ]
        
        self.rollback_steps = []
        for step_data in default_steps:
            risk_level = RiskLevel(step_data.get('risk_level', 'low'))
            step = RollbackStep(
                order=step_data['order'],
                description=step_data['description'],
                command=step_data.get('command'),
                estimated_time=step_data.get('estimated_time', '5 minutes'),
                risk_level=risk_level,
                verification=step_data.get('verification', '')
            )
            self.rollback_steps.append(step)
    
    def assess_release_readiness(self) -> Dict:
        """Assess overall release readiness."""
        assessment = {
            'overall_status': 'ready',
            'readiness_score': 0.0,
            'blocking_issues': [],
            'warnings': [],
            'recommendations': [],
            'feature_summary': {},
            'quality_gate_summary': {},
            'timeline_assessment': {}
        }
        
        total_score = 0
        max_score = 0
        
        # Assess features
        feature_stats = {
            'total': len(self.features),
            'ready': 0,
            'blocked': 0,
            'in_progress': 0,
            'pending': 0,
            'high_risk': 0,
            'breaking_changes': 0,
            'missing_approvals': 0,
            'low_test_coverage': 0
        }
        
        for feature in self.features:
            max_score += 10  # Each feature worth 10 points
            
            if feature.status == ComponentStatus.READY:
                feature_stats['ready'] += 1
                total_score += 10
            elif feature.status == ComponentStatus.BLOCKED:
                feature_stats['blocked'] += 1
                assessment['blocking_issues'].append(
                    f"Feature '{feature.title}' ({feature.id}) is blocked"
                )
            elif feature.status == ComponentStatus.IN_PROGRESS:
                feature_stats['in_progress'] += 1
                total_score += 5  # Partial credit
                assessment['warnings'].append(
                    f"Feature '{feature.title}' ({feature.id}) still in progress"
                )
            else:
                feature_stats['pending'] += 1
                assessment['warnings'].append(
                    f"Feature '{feature.title}' ({feature.id}) is pending"
                )
            
            # Check risk level
            if feature.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                feature_stats['high_risk'] += 1
            
            # Check breaking changes
            if feature.breaking_changes:
                feature_stats['breaking_changes'] += 1
            
            # Check approvals
            missing_approvals = self._check_feature_approvals(feature)
            if missing_approvals:
                feature_stats['missing_approvals'] += 1
                assessment['blocking_issues'].append(
                    f"Feature '{feature.title}' missing approvals: {', '.join(missing_approvals)}"
                )
            
            # Check test coverage
            if (feature.test_coverage_actual is not None and 
                feature.test_coverage_actual < feature.test_coverage_required):
                feature_stats['low_test_coverage'] += 1
                assessment['warnings'].append(
                    f"Feature '{feature.title}' has low test coverage: "
                    f"{feature.test_coverage_actual}% < {feature.test_coverage_required}%"
                )
        
        assessment['feature_summary'] = feature_stats
        
        # Assess quality gates
        gate_stats = {
            'total': len(self.quality_gates),
            'passed': 0,
            'failed': 0,
            'pending': 0,
            'required_failed': 0
        }
        
        for gate in self.quality_gates:
            max_score += 5  # Each gate worth 5 points
            
            if gate.status == ComponentStatus.READY:
                gate_stats['passed'] += 1
                total_score += 5
            elif gate.status == ComponentStatus.FAILED:
                gate_stats['failed'] += 1
                if gate.required:
                    gate_stats['required_failed'] += 1
                    assessment['blocking_issues'].append(
                        f"Required quality gate '{gate.name}' failed"
                    )
            else:
                gate_stats['pending'] += 1
                if gate.required:
                    assessment['warnings'].append(
                        f"Required quality gate '{gate.name}' is pending"
                    )
        
        assessment['quality_gate_summary'] = gate_stats
        
        # Timeline assessment
        if self.target_date:
            # Handle timezone-aware datetime comparison
            now = datetime.now(self.target_date.tzinfo) if self.target_date.tzinfo else datetime.now()
            days_until_release = (self.target_date - now).days
            assessment['timeline_assessment'] = {
                'target_date': self.target_date.isoformat(),
                'days_remaining': days_until_release,
                'timeline_status': 'on_track' if days_until_release > 0 else 'overdue'
            }
            
            if days_until_release < 0:
                assessment['blocking_issues'].append(f"Release is {abs(days_until_release)} days overdue")
            elif days_until_release < 3 and feature_stats['blocked'] > 0:
                assessment['blocking_issues'].append("Not enough time to resolve blocked features")
        
        # Calculate overall readiness score
        if max_score > 0:
            assessment['readiness_score'] = (total_score / max_score) * 100
        
        # Determine overall status
        if assessment['blocking_issues']:
            assessment['overall_status'] = 'blocked'
        elif assessment['warnings']:
            assessment['overall_status'] = 'at_risk'
        else:
            assessment['overall_status'] = 'ready'
        
        # Generate recommendations
        if feature_stats['missing_approvals'] > 0:
            assessment['recommendations'].append("Obtain required approvals for pending features")
        
        if feature_stats['low_test_coverage'] > 0:
            assessment['recommendations'].append("Improve test coverage for features below threshold")
        
        if gate_stats['pending'] > 0:
            assessment['recommendations'].append("Complete pending quality gate validations")
        
        if feature_stats['high_risk'] > 0:
            assessment['recommendations'].append("Review high-risk features for additional validation")
        
        return assessment
    
    def _check_feature_approvals(self, feature: Feature) -> List[str]:
        """Check which approvals are missing for a feature."""
        missing = []
        
        # Determine required approvals based on risk level
        required = self.required_approvals.copy()
        if feature.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            required = self.high_risk_approval_requirements.copy()
        
        if 'pm_approved' in required and not feature.pm_approved:
            missing.append('PM approval')
        
        if 'qa_approved' in required and not feature.qa_approved:
            missing.append('QA approval')
        
        if 'security_approved' in required and not feature.security_approved:
            missing.append('Security approval')
        
        return missing
    
    def generate_release_checklist(self) -> List[Dict]:
        """Generate comprehensive release checklist."""
        checklist = []
        
        # Pre-release validation
        checklist.extend([
            {
                'category': 'Pre-Release Validation',
                'item': 'All features implemented and tested',
                'status': 'ready' if all(f.status == ComponentStatus.READY for f in self.features) else 'pending',
                'details': f"{len([f for f in self.features if f.status == ComponentStatus.READY])}/{len(self.features)} features ready"
            },
            {
                'category': 'Pre-Release Validation', 
                'item': 'Breaking changes documented',
                'status': 'ready' if self._check_breaking_change_docs() else 'pending',
                'details': f"{len([f for f in self.features if f.breaking_changes])} features have breaking changes"
            },
            {
                'category': 'Pre-Release Validation',
                'item': 'Migration scripts tested',
                'status': 'ready' if self._check_migrations() else 'pending',
                'details': f"{len([f for f in self.features if f.requires_migration])} features require migrations"
            }
        ])
        
        # Quality gates
        for gate in self.quality_gates:
            checklist.append({
                'category': 'Quality Gates',
                'item': gate.name,
                'status': gate.status.value,
                'details': gate.details,
                'required': gate.required
            })
        
        # Approvals
        approval_items = [
            ('Product Manager sign-off', self._check_pm_approvals()),
            ('QA validation complete', self._check_qa_approvals()), 
            ('Security team clearance', self._check_security_approvals())
        ]
        
        for item, status in approval_items:
            checklist.append({
                'category': 'Approvals',
                'item': item,
                'status': 'ready' if status else 'pending'
            })
        
        # Documentation
        doc_items = [
            'CHANGELOG.md updated',
            'API documentation updated', 
            'User documentation updated',
            'Migration guide written',
            'Rollback procedure documented'
        ]
        
        for item in doc_items:
            checklist.append({
                'category': 'Documentation',
                'item': item,
                'status': 'pending'  # Would need integration with docs system to check
            })
        
        # Deployment preparation
        deployment_items = [
            'Database migrations prepared',
            'Environment variables configured',
            'Monitoring alerts updated',
            'Rollback plan tested',
            'Stakeholders notified'
        ]
        
        for item in deployment_items:
            checklist.append({
                'category': 'Deployment',
                'item': item,
                'status': 'pending'
            })
        
        return checklist
    
    def _check_breaking_change_docs(self) -> bool:
        """Check if breaking changes are properly documented."""
        features_with_breaking_changes = [f for f in self.features if f.breaking_changes]
        return all(len(f.breaking_changes) > 0 for f in features_with_breaking_changes)
    
    def _check_migrations(self) -> bool:
        """Check migration readiness."""
        features_with_migrations = [f for f in self.features if f.requires_migration]
        return all(f.status == ComponentStatus.READY for f in features_with_migrations)
    
    def _check_pm_approvals(self) -> bool:
        """Check PM approvals."""
        return all(f.pm_approved for f in self.features if f.risk_level != RiskLevel.LOW)
    
    def _check_qa_approvals(self) -> bool:
        """Check QA approvals.""" 
        return all(f.qa_approved for f in self.features)
    
    def _check_security_approvals(self) -> bool:
        """Check security approvals."""
        high_risk_features = [f for f in self.features if f.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        return all(f.security_approved for f in high_risk_features)
    
    def generate_communication_plan(self) -> Dict:
        """Generate stakeholder communication plan."""
        plan = {
            'internal_notifications': [],
            'external_notifications': [],
            'timeline': [],
            'channels': {},
            'templates': {}
        }
        
        # Group stakeholders by type
        internal_stakeholders = [s for s in self.stakeholders if s.role in 
                               ['developer', 'qa', 'pm', 'devops', 'security']]
        external_stakeholders = [s for s in self.stakeholders if s.role in 
                               ['customer', 'partner', 'support']]
        
        # Internal notifications
        for stakeholder in internal_stakeholders:
            plan['internal_notifications'].append({
                'recipient': stakeholder.name,
                'role': stakeholder.role,
                'method': stakeholder.notification_type,
                'content_type': 'technical_details',
                'timing': 'T-24h and T-0'
            })
        
        # External notifications
        for stakeholder in external_stakeholders:
            plan['external_notifications'].append({
                'recipient': stakeholder.name,
                'role': stakeholder.role,
                'method': stakeholder.notification_type,
                'content_type': 'user_facing_changes',
                'timing': 'T-48h and T+1h'
            })
        
        # Communication timeline
        if self.target_date:
            timeline_items = [
                (timedelta(days=-2), 'Send pre-release notification to external stakeholders'),
                (timedelta(days=-1), 'Send deployment notification to internal teams'),
                (timedelta(hours=-2), 'Final go/no-go decision'),
                (timedelta(hours=0), 'Begin deployment'),
                (timedelta(hours=1), 'Post-deployment status update'),
                (timedelta(hours=24), 'Post-release summary')
            ]
            
            for delta, description in timeline_items:
                notification_time = self.target_date + delta
                plan['timeline'].append({
                    'time': notification_time.isoformat(),
                    'description': description,
                    'recipients': 'all' if 'all' in description.lower() else 'internal'
                })
        
        # Communication channels
        channels = {}
        for stakeholder in self.stakeholders:
            if stakeholder.notification_type not in channels:
                channels[stakeholder.notification_type] = []
            channels[stakeholder.notification_type].append(stakeholder.contact)
        plan['channels'] = channels
        
        # Message templates
        plan['templates'] = self._generate_message_templates()
        
        return plan
    
    def _generate_message_templates(self) -> Dict:
        """Generate message templates for different audiences."""
        breaking_changes = [f for f in self.features if f.breaking_changes]
        new_features = [f for f in self.features if f.type == 'feature']
        bug_fixes = [f for f in self.features if f.type == 'bugfix']
        
        templates = {
            'internal_pre_release': {
                'subject': f'Release {self.version} - Pre-deployment Notification',
                'body': f"""Team,

We are preparing to deploy {self.release_name} version {self.version} on {self.target_date.strftime('%Y-%m-%d %H:%M UTC') if self.target_date else 'TBD'}.

Key Changes:
- {len(new_features)} new features
- {len(bug_fixes)} bug fixes
- {len(breaking_changes)} breaking changes

Please review the release notes and prepare for any needed support activities.

Rollback plan: Available in release documentation
On-call: Please be available during deployment window

Best regards,
Release Team"""
            },
            'external_user_notification': {
                'subject': f'Product Update - Version {self.version} Now Available',
                'body': f"""Dear Users,

We're excited to announce version {self.version} of {self.release_name} is now available!

What's New:
{chr(10).join(f"- {f.title}" for f in new_features[:5])}

Bug Fixes:
{chr(10).join(f"- {f.title}" for f in bug_fixes[:3])}

{'Important: This release includes breaking changes. Please review the migration guide.' if breaking_changes else ''}

For full release notes and migration instructions, visit our documentation.

Thank you for using our product!

The Development Team"""
            },
            'rollback_notification': {
                'subject': f'URGENT: Release {self.version} Rollback Initiated',
                'body': f"""ATTENTION: Release rollback in progress.

Release: {self.version}
Reason: [TO BE FILLED]
Rollback initiated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
Estimated completion: [TO BE FILLED]

Current status: Rolling back to previous stable version
Impact: [TO BE FILLED]

We will provide updates every 15 minutes until rollback is complete.

Incident Commander: [TO BE FILLED]
Status page: [TO BE FILLED]"""
            }
        }
        
        return templates
    
    def generate_rollback_runbook(self) -> Dict:
        """Generate detailed rollback runbook."""
        runbook = {
            'overview': {
                'purpose': f'Emergency rollback procedure for {self.release_name} v{self.version}',
                'triggers': [
                    'Error rate spike (>2x baseline for >15 minutes)',
                    'Critical functionality failure',
                    'Security incident',
                    'Data corruption detected',
                    'Performance degradation (>50% latency increase)',
                    'Manual decision by incident commander'
                ],
                'decision_makers': ['On-call Engineer', 'Engineering Lead', 'Incident Commander'],
                'estimated_total_time': self._calculate_rollback_time()
            },
            'prerequisites': [
                'Confirm rollback is necessary (check with incident commander)',
                'Notify stakeholders of rollback decision', 
                'Ensure database backups are available',
                'Verify monitoring systems are operational',
                'Have communication channels ready'
            ],
            'steps': [],
            'verification': {
                'health_checks': [
                    'Application responds to health endpoint',
                    'Database connectivity confirmed',
                    'Authentication system functional',
                    'Core user workflows working',
                    'Error rates back to baseline',
                    'Performance metrics within normal range'
                ],
                'rollback_confirmation': [
                    'Previous version fully deployed',
                    'Database in consistent state',
                    'All services communicating properly',
                    'Monitoring shows stable metrics',
                    'Sample user workflows tested'
                ]
            },
            'post_rollback': [
                'Update status page with resolution',
                'Notify all stakeholders of successful rollback',
                'Schedule post-incident review',
                'Document issues encountered during rollback',
                'Plan investigation of root cause',
                'Determine timeline for next release attempt'
            ],
            'emergency_contacts': []
        }
        
        # Convert rollback steps to detailed format
        for step in sorted(self.rollback_steps, key=lambda x: x.order):
            step_data = {
                'order': step.order,
                'title': step.description,
                'estimated_time': step.estimated_time,
                'risk_level': step.risk_level.value,
                'instructions': step.description,
                'command': step.command,
                'verification': step.verification,
                'rollback_possible': step.risk_level != RiskLevel.CRITICAL
            }
            runbook['steps'].append(step_data)
        
        # Add emergency contacts
        critical_stakeholders = [s for s in self.stakeholders if s.critical_path]
        for stakeholder in critical_stakeholders:
            runbook['emergency_contacts'].append({
                'name': stakeholder.name,
                'role': stakeholder.role,
                'contact': stakeholder.contact,
                'method': stakeholder.notification_type
            })
        
        return runbook
    
    def _calculate_rollback_time(self) -> str:
        """Calculate estimated total rollback time."""
        total_minutes = 0
        for step in self.rollback_steps:
            # Parse time estimates like "5 minutes", "30 seconds", "1 hour"
            time_str = step.estimated_time.lower()
            if 'minute' in time_str:
                minutes = int(re.search(r'(\d+)', time_str).group(1))
                total_minutes += minutes
            elif 'hour' in time_str:
                hours = int(re.search(r'(\d+)', time_str).group(1))
                total_minutes += hours * 60
            elif 'second' in time_str:
                # Round up seconds to minutes
                total_minutes += 1
        
        if total_minutes < 60:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours}h {minutes}m"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Assess release readiness and generate release plans")
    parser.add_argument('--input', '-i', required=True,
                       help='Release plan JSON file')
    parser.add_argument('--output-format', '-f',
                       choices=['json', 'markdown', 'text'], 
                       default='text', help='Output format')
    parser.add_argument('--output', '-o', type=str,
                       help='Output file (default: stdout)')
    parser.add_argument('--include-checklist', action='store_true',
                       help='Include release checklist in output')
    parser.add_argument('--include-communication', action='store_true', 
                       help='Include communication plan')
    parser.add_argument('--include-rollback', action='store_true',
                       help='Include rollback runbook')
    parser.add_argument('--min-coverage', type=float, default=80.0,
                       help='Minimum test coverage threshold')
    
    args = parser.parse_args()
    
    # Load release plan
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            plan_data = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize planner
    planner = ReleasePlanner()
    planner.min_test_coverage = args.min_coverage
    
    try:
        planner.load_release_plan(plan_data)
    except Exception as e:
        print(f"Error loading release plan: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate assessment
    assessment = planner.assess_release_readiness()
    
    # Generate optional components
    checklist = planner.generate_release_checklist() if args.include_checklist else None
    communication = planner.generate_communication_plan() if args.include_communication else None
    rollback = planner.generate_rollback_runbook() if args.include_rollback else None
    
    # Generate output
    if args.output_format == 'json':
        output_data = {
            'assessment': assessment,
            'checklist': checklist,
            'communication_plan': communication,
            'rollback_runbook': rollback
        }
        output_text = json.dumps(output_data, indent=2, default=str)
    
    elif args.output_format == 'markdown':
        output_lines = [
            f"# Release Readiness Report - {planner.release_name} v{planner.version}",
            "",
            f"**Overall Status:** {assessment['overall_status'].upper()}",
            f"**Readiness Score:** {assessment['readiness_score']:.1f}%",
            ""
        ]
        
        if assessment['blocking_issues']:
            output_lines.extend([
                "## 🚫 Blocking Issues",
                ""
            ])
            for issue in assessment['blocking_issues']:
                output_lines.append(f"- {issue}")
            output_lines.append("")
        
        if assessment['warnings']:
            output_lines.extend([
                "## ⚠️ Warnings",
                ""
            ])
            for warning in assessment['warnings']:
                output_lines.append(f"- {warning}")
            output_lines.append("")
        
        # Feature summary
        fs = assessment['feature_summary']
        output_lines.extend([
            "## Features Summary",
            "",
            f"- **Total:** {fs['total']}",
            f"- **Ready:** {fs['ready']}",
            f"- **In Progress:** {fs['in_progress']}",
            f"- **Blocked:** {fs['blocked']}",
            f"- **Breaking Changes:** {fs['breaking_changes']}",
            ""
        ])
        
        if checklist:
            output_lines.extend([
                "## Release Checklist",
                ""
            ])
            current_category = ""
            for item in checklist:
                if item['category'] != current_category:
                    current_category = item['category']
                    output_lines.append(f"### {current_category}")
                    output_lines.append("")
                
                status_icon = "✅" if item['status'] == 'ready' else "❌" if item['status'] == 'failed' else "⏳"
                output_lines.append(f"- {status_icon} {item['item']}")
            output_lines.append("")
        
        output_text = '\n'.join(output_lines)
    
    else:  # text format
        output_lines = [
            f"Release Readiness Report",
            f"========================",
            f"Release: {planner.release_name} v{planner.version}",
            f"Status: {assessment['overall_status'].upper()}",
            f"Readiness Score: {assessment['readiness_score']:.1f}%",
            ""
        ]
        
        if assessment['blocking_issues']:
            output_lines.extend(["BLOCKING ISSUES:", ""])
            for issue in assessment['blocking_issues']:
                output_lines.append(f"  ❌ {issue}")
            output_lines.append("")
        
        if assessment['warnings']:
            output_lines.extend(["WARNINGS:", ""])
            for warning in assessment['warnings']:
                output_lines.append(f"  ⚠️  {warning}")
            output_lines.append("")
        
        if assessment['recommendations']:
            output_lines.extend(["RECOMMENDATIONS:", ""])
            for rec in assessment['recommendations']:
                output_lines.append(f"  💡 {rec}")
            output_lines.append("")
        
        # Summary stats
        fs = assessment['feature_summary']
        gs = assessment['quality_gate_summary']
        
        output_lines.extend([
            f"FEATURE SUMMARY:",
            f"  Total: {fs['total']} | Ready: {fs['ready']} | Blocked: {fs['blocked']}",
            f"  Breaking Changes: {fs['breaking_changes']} | Missing Approvals: {fs['missing_approvals']}",
            "",
            f"QUALITY GATES:",
            f"  Total: {gs['total']} | Passed: {gs['passed']} | Failed: {gs['failed']}",
            ""
        ])
        
        output_text = '\n'.join(output_lines)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_text)
    else:
        print(output_text)


if __name__ == '__main__':
    main()