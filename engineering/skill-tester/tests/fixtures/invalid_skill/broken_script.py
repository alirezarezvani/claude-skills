#!/usr/bin/env python3
"""Invalid script with external imports and syntax issues."""

import requests  # External import - should be flagged
import numpy as np  # External import - should be flagged
import sys

def broken_function(
    # Missing closing parenthesis and other syntax errors
    pass

def main():
    print("Hello"
    # Missing closing parenthesis

if __name__ == "__main__":
    main()