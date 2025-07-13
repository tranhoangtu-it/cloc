#!/usr/bin/env python3
"""
Code Lines of Code Counter (CLOC) - Main entry point.

A powerful tool for counting Lines of Code and analyzing code changes in Git repositories.
"""

import sys
import os

# Add the current directory to Python path to import the cloc package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloc.cli import main

if __name__ == '__main__':
    main()