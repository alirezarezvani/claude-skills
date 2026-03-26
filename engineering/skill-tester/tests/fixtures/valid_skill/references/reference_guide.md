# Reference Guide

This document provides reference information for the valid test skill.

## Overview

The valid test skill is designed to test the skill-tester's validation capabilities.

## API Reference

### ExampleProcessor

The main processor class for handling input data.

#### Methods

| Method | Description |
|--------|-------------|
| `process_file(path)` | Process an input file |
| `generate_report()` | Generate a comprehensive report |

## Configuration

No configuration required. The skill uses sensible defaults.

## Error Handling

The tool handles the following errors:

1. **FileNotFoundError**: Input file doesn't exist
2. **ValueError**: File cannot be read as UTF-8
3. **Exception**: Unexpected errors

## Performance

Processing time depends on file size:
- Small files (<1KB): <1ms
- Medium files (1KB-1MB): <100ms
- Large files (>1MB): varies

## Best Practices

1. Always validate input before processing
2. Use verbose mode for debugging
3. Use JSON output for automation