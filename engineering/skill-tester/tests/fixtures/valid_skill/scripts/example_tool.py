#!/usr/bin/env python3
"""
Example Tool - A sample tool for testing the script_tester

This script demonstrates a well-structured Python tool that follows
all the requirements for the skill-tester validation.

Usage:
    python example_tool.py --input FILE [--output FILE] [--json] [--verbose]

Author: Test Author
Version: 1.0.0
Dependencies: Python Standard Library Only
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class ExampleProcessor:
    """Processes input data and generates output."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {}
        
    def log(self, message: str) -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)
            
    def process_file(self, input_path: Path) -> Dict[str, Any]:
        """Process an input file and return results."""
        self.log(f"Processing file: {input_path}")
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        try:
            content = input_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            raise ValueError(f"Cannot read file as UTF-8: {e}")
            
        # Analyze the content
        lines = content.split('\n')
        words = content.split()
        
        result = {
            "file": str(input_path),
            "lines": len(lines),
            "words": len(words),
            "characters": len(content),
            "status": "processed"
        }
        
        self.results = result
        return result
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report."""
        return {
            "summary": self.results,
            "timestamp": "2026-03-26T00:00:00Z",
            "version": "1.0.0"
        }


def format_output(result: Dict[str, Any], json_format: bool) -> str:
    """Format the output for display."""
    if json_format:
        return json.dumps(result, indent=2)
    
    lines = []
    lines.append("=" * 50)
    lines.append("PROCESSING REPORT")
    lines.append("=" * 50)
    lines.append(f"File: {result.get('file', 'N/A')}")
    lines.append(f"Lines: {result.get('lines', 0)}")
    lines.append(f"Words: {result.get('words', 0)}")
    lines.append(f"Characters: {result.get('characters', 0)}")
    lines.append(f"Status: {result.get('status', 'unknown')}")
    lines.append("=" * 50)
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Example tool for testing the script_tester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python example_tool.py --input data.txt
  python example_tool.py --input data.txt --output result.json
  python example_tool.py --input data.txt --json
  python example_tool.py --input data.txt --verbose

Output Formats:
  Default: Human-readable text report
  --json:  JSON-formatted output for programmatic use
        """
    )
    
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Input file to process"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    try:
        # Create processor and run
        processor = ExampleProcessor(verbose=args.verbose)
        result = processor.process_file(args.input)
        report = processor.generate_report()
        
        # Format and output
        output = format_output(report, args.json)
        
        if args.output:
            args.output.write_text(output, encoding='utf-8')
            if args.verbose:
                print(f"[INFO] Output written to {args.output}", file=sys.stderr)
        else:
            print(output)
            
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()