#!/usr/bin/env python3
"""
Code Quality Analyzer - Analyzes code for quality metrics, patterns, and best practices
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess

class CodeQualityAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.results = {
            'metrics': {},
            'issues': [],
            'suggestions': [],
            'score': 0
        }
        
    def analyze(self) -> Dict:
        """Run complete code quality analysis"""
        print("🔍 Analyzing code quality...")
        
        # Analyze different aspects
        self._analyze_code_metrics()
        self._analyze_complexity()
        self._analyze_dependencies()
        self._analyze_security()
        self._analyze_performance()
        self._analyze_tests()
        self._analyze_documentation()
        
        # Calculate overall score
        self._calculate_score()
        
        return self.results
    
    def _analyze_code_metrics(self):
        """Analyze basic code metrics"""
        metrics = {
            'total_files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'avg_file_length': 0,
            'languages': {}
        }
        
        extensions = {
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript React',
            '.js': 'JavaScript', 
            '.jsx': 'JavaScript React',
            '.py': 'Python',
            '.go': 'Go',
            '.sql': 'SQL',
            '.graphql': 'GraphQL'
        }
        
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                if 'node_modules' in str(file_path) or 'dist' in str(file_path):
                    continue
                    
                metrics['total_files'] += 1
                lang = extensions[file_path.suffix]
                metrics['languages'][lang] = metrics['languages'].get(lang, 0) + 1
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    metrics['total_lines'] += len(lines)
                    
                    for line in lines:
                        stripped = line.strip()
                        if not stripped:
                            metrics['blank_lines'] += 1
                        elif stripped.startswith(('#', '//', '/*', '*')):
                            metrics['comment_lines'] += 1
                        else:
                            metrics['code_lines'] += 1
        
        if metrics['total_files'] > 0:
            metrics['avg_file_length'] = metrics['total_lines'] / metrics['total_files']
            metrics['comment_ratio'] = metrics['comment_lines'] / metrics['code_lines'] if metrics['code_lines'] > 0 else 0
        
        self.results['metrics'] = metrics
    
    def _analyze_complexity(self):
        """Analyze code complexity"""
        complexity_issues = []
        
        # Check for TypeScript/JavaScript files
        for file_path in self.project_path.rglob('*.ts'):
            if 'node_modules' in str(file_path):
                continue
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check function length
                functions = re.findall(r'function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', content)
                if len(functions) > 20:
                    complexity_issues.append({
                        'file': str(file_path.relative_to(self.project_path)),
                        'issue': 'Too many functions in file',
                        'severity': 'warning',
                        'count': len(functions)
                    })
                
                # Check for deeply nested code
                max_indent = 0
                for line in content.split('\n'):
                    indent = len(line) - len(line.lstrip())
                    max_indent = max(max_indent, indent)
                
                if max_indent > 16:  # More than 4 levels of indentation
                    complexity_issues.append({
                        'file': str(file_path.relative_to(self.project_path)),
                        'issue': 'Deep nesting detected',
                        'severity': 'warning',
                        'max_indent': max_indent
                    })
                
                # Check for long functions
                function_blocks = re.split(r'function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', content)
                for block in function_blocks[1:]:
                    lines = block.split('\n')
                    if len(lines) > 50:
                        complexity_issues.append({
                            'file': str(file_path.relative_to(self.project_path)),
                            'issue': 'Long function detected',
                            'severity': 'warning',
                            'lines': len(lines)
                        })
        
        self.results['complexity'] = complexity_issues
    
    def _analyze_dependencies(self):
        """Analyze project dependencies"""
        dependency_analysis = {
            'outdated': [],
            'security_issues': [],
            'unused': [],
            'missing': []
        }
        
        # Check package.json files
        for package_json in self.project_path.rglob('package.json'):
            if 'node_modules' in str(package_json):
                continue
                
            with open(package_json, 'r') as f:
                data = json.load(f)
                
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                
                # Check for common issues
                for dep, version in deps.items():
                    if version.startswith('^') or version.startswith('~'):
                        # Good - using semver
                        pass
                    elif version == '*' or version == 'latest':
                        dependency_analysis['security_issues'].append({
                            'package': dep,
                            'issue': 'Using wildcard version',
                            'recommendation': 'Pin to specific version'
                        })
        
        self.results['dependencies'] = dependency_analysis
    
    def _analyze_security(self):
        """Analyze security issues"""
        security_issues = []
        
        patterns = [
            (r'console\.log\(.*password.*\)', 'Password logged to console'),
            (r'eval\(', 'Use of eval() detected'),
            (r'innerHTML\s*=', 'Direct innerHTML manipulation'),
            (r'document\.write\(', 'Use of document.write()'),
            (r'api[kK]ey\s*=\s*[\'"][^\'"]+[\'"]', 'Hardcoded API key'),
            (r'password\s*=\s*[\'"][^\'"]+[\'"]', 'Hardcoded password'),
            (r'secret\s*=\s*[\'"][^\'"]+[\'"]', 'Hardcoded secret'),
            (r'TODO:?\s+security', 'Security TODO found'),
            (r'FIXME:?\s+security', 'Security FIXME found'),
        ]
        
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                if 'node_modules' in str(file_path) or '.test.' in str(file_path):
                    continue
                    
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern, issue in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            security_issues.append({
                                'file': str(file_path.relative_to(self.project_path)),
                                'line': line_num,
                                'issue': issue,
                                'severity': 'high' if 'password' in issue.lower() or 'key' in issue.lower() else 'medium'
                            })
        
        self.results['security'] = security_issues
    
    def _analyze_performance(self):
        """Analyze performance issues"""
        performance_issues = []
        
        patterns = [
            (r'for\s*\(.*\)\s*{[^}]*for\s*\(', 'Nested loops detected'),
            (r'async\s+\w+\s*\([^)]*\)\s*{[^}]*await[^}]*await', 'Multiple sequential awaits'),
            (r'\.map\([^)]+\)\.filter\([^)]+\)\.map\(', 'Inefficient chaining'),
            (r'document\.querySelector.*inside.*loop', 'DOM query in loop'),
            (r'useState\([^)]*\).*useState\([^)]*\).*useState\([^)]*\).*useState\([^)]*\).*useState\(', 'Too many useState hooks'),
        ]
        
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                if 'node_modules' in str(file_path):
                    continue
                    
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern, issue in patterns:
                        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                            performance_issues.append({
                                'file': str(file_path.relative_to(self.project_path)),
                                'issue': issue,
                                'severity': 'medium'
                            })
        
        self.results['performance'] = performance_issues
    
    def _analyze_tests(self):
        """Analyze test coverage and quality"""
        test_analysis = {
            'test_files': 0,
            'test_suites': 0,
            'test_cases': 0,
            'coverage_configured': False,
            'e2e_tests': False,
            'unit_tests': False,
            'integration_tests': False
        }
        
        # Count test files
        for test_file in self.project_path.rglob('*.test.*'):
            if 'node_modules' not in str(test_file):
                test_analysis['test_files'] += 1
                test_analysis['unit_tests'] = True
                
                with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    test_analysis['test_suites'] += len(re.findall(r'describe\(', content))
                    test_analysis['test_cases'] += len(re.findall(r'(?:it|test)\(', content))
        
        # Check for E2E tests
        if (self.project_path / 'cypress').exists() or (self.project_path / 'tests' / 'e2e').exists():
            test_analysis['e2e_tests'] = True
        
        # Check for coverage configuration
        for config_file in ['jest.config.js', 'jest.config.ts', 'package.json']:
            config_path = self.project_path / config_file
            if config_path.exists():
                with open(config_path, 'r') as f:
                    if 'coverage' in f.read():
                        test_analysis['coverage_configured'] = True
                        break
        
        self.results['tests'] = test_analysis
    
    def _analyze_documentation(self):
        """Analyze documentation quality"""
        doc_analysis = {
            'readme_exists': False,
            'api_docs': False,
            'inline_comments_ratio': 0,
            'jsdoc_coverage': 0,
            'missing_docs': []
        }
        
        # Check for README
        if (self.project_path / 'README.md').exists():
            doc_analysis['readme_exists'] = True
            with open(self.project_path / 'README.md', 'r') as f:
                readme_content = f.read()
                doc_analysis['readme_quality'] = {
                    'has_installation': 'installation' in readme_content.lower(),
                    'has_usage': 'usage' in readme_content.lower(),
                    'has_api': 'api' in readme_content.lower(),
                    'has_contributing': 'contributing' in readme_content.lower(),
                    'length': len(readme_content)
                }
        
        # Check for API documentation
        if (self.project_path / 'docs').exists() or (self.project_path / 'api-docs').exists():
            doc_analysis['api_docs'] = True
        
        # Check JSDoc coverage
        total_functions = 0
        documented_functions = 0
        
        for file_path in self.project_path.rglob('*.ts'):
            if 'node_modules' in str(file_path) or '.test.' in str(file_path):
                continue
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Count functions
                functions = re.findall(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)', content)
                total_functions += len(functions)
                
                # Count documented functions (with JSDoc)
                jsdoc_blocks = re.findall(r'/\*\*[\s\S]*?\*/', content)
                documented_functions += len(jsdoc_blocks)
        
        if total_functions > 0:
            doc_analysis['jsdoc_coverage'] = (documented_functions / total_functions) * 100
        
        doc_analysis['inline_comments_ratio'] = self.results['metrics'].get('comment_ratio', 0)
        
        self.results['documentation'] = doc_analysis
    
    def _calculate_score(self):
        """Calculate overall quality score"""
        score = 100
        
        # Deduct points for issues
        score -= len(self.results.get('security', [])) * 5
        score -= len(self.results.get('complexity', [])) * 2
        score -= len(self.results.get('performance', [])) * 3
        
        # Add points for good practices
        if self.results.get('tests', {}).get('test_files', 0) > 0:
            score += 10
        if self.results.get('tests', {}).get('coverage_configured'):
            score += 5
        if self.results.get('tests', {}).get('e2e_tests'):
            score += 5
        if self.results.get('documentation', {}).get('readme_exists'):
            score += 5
        if self.results.get('documentation', {}).get('jsdoc_coverage', 0) > 50:
            score += 5
        
        # Ensure score is between 0 and 100
        self.results['score'] = max(0, min(100, score))
        
        # Generate recommendations
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Generate improvement recommendations"""
        recommendations = []
        
        if self.results['score'] < 70:
            recommendations.append({
                'priority': 'high',
                'category': 'overall',
                'recommendation': 'Code quality needs significant improvement'
            })
        
        if len(self.results.get('security', [])) > 0:
            recommendations.append({
                'priority': 'critical',
                'category': 'security',
                'recommendation': f"Fix {len(self.results['security'])} security issues immediately"
            })
        
        if self.results.get('tests', {}).get('test_files', 0) < 5:
            recommendations.append({
                'priority': 'high',
                'category': 'testing',
                'recommendation': 'Increase test coverage - aim for 80%+ coverage'
            })
        
        if not self.results.get('documentation', {}).get('readme_exists'):
            recommendations.append({
                'priority': 'medium',
                'category': 'documentation',
                'recommendation': 'Add comprehensive README.md'
            })
        
        if self.results.get('documentation', {}).get('jsdoc_coverage', 0) < 30:
            recommendations.append({
                'priority': 'medium',
                'category': 'documentation',
                'recommendation': 'Add JSDoc comments to public functions'
            })
        
        self.results['recommendations'] = recommendations
    
    def generate_report(self) -> str:
        """Generate human-readable report"""
        report = []
        report.append("=" * 60)
        report.append("CODE QUALITY ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"\nOverall Score: {self.results['score']}/100")
        report.append("-" * 60)
        
        # Metrics
        metrics = self.results.get('metrics', {})
        report.append("\n📊 Code Metrics:")
        report.append(f"  Total Files: {metrics.get('total_files', 0)}")
        report.append(f"  Total Lines: {metrics.get('total_lines', 0)}")
        report.append(f"  Code Lines: {metrics.get('code_lines', 0)}")
        report.append(f"  Comment Ratio: {metrics.get('comment_ratio', 0):.1%}")
        
        # Security
        security = self.results.get('security', [])
        report.append(f"\n🔒 Security Issues: {len(security)}")
        for issue in security[:5]:  # Show first 5
            report.append(f"  ⚠️  {issue['file']}:{issue['line']} - {issue['issue']}")
        
        # Tests
        tests = self.results.get('tests', {})
        report.append(f"\n🧪 Test Coverage:")
        report.append(f"  Test Files: {tests.get('test_files', 0)}")
        report.append(f"  Test Cases: {tests.get('test_cases', 0)}")
        report.append(f"  E2E Tests: {'✅' if tests.get('e2e_tests') else '❌'}")
        report.append(f"  Coverage Config: {'✅' if tests.get('coverage_configured') else '❌'}")
        
        # Documentation
        docs = self.results.get('documentation', {})
        report.append(f"\n📚 Documentation:")
        report.append(f"  README: {'✅' if docs.get('readme_exists') else '❌'}")
        report.append(f"  JSDoc Coverage: {docs.get('jsdoc_coverage', 0):.1f}%")
        
        # Recommendations
        report.append(f"\n💡 Top Recommendations:")
        for rec in self.results.get('recommendations', [])[:5]:
            emoji = '🔴' if rec['priority'] == 'critical' else '🟡' if rec['priority'] == 'high' else '🟢'
            report.append(f"  {emoji} [{rec['category']}] {rec['recommendation']}")
        
        return "\n".join(report)

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python code_quality_analyzer.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    analyzer = CodeQualityAnalyzer(project_path)
    analyzer.analyze()
    print(analyzer.generate_report())
    
    # Optionally save JSON report
    if len(sys.argv) > 2 and sys.argv[2] == '--json':
        with open('code_quality_report.json', 'w') as f:
            json.dump(analyzer.results, f, indent=2)
        print(f"\n📄 JSON report saved to code_quality_report.json")

if __name__ == '__main__':
    main()
