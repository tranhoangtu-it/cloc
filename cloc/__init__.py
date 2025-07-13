"""
Code Lines of Code Counter (CLOC)

A powerful tool for counting Lines of Code and analyzing code changes in Git repositories.
"""

__version__ = "1.0.0"
__author__ = "CLOC Team"

from .counter import CodeCounter
from .git_analyzer import GitAnalyzer
from .reporter import Reporter
from .cli import main

__all__ = ["CodeCounter", "GitAnalyzer", "Reporter", "main"]