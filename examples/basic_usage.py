#!/usr/bin/env python3
"""
Basic usage example for CLOC tool.
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cloc.counter import CodeCounter
from cloc.reporter import Reporter


def main():
    """Demonstrate basic usage of CLOC tool."""
    
    # Initialize the counter and reporter
    counter = CodeCounter()
    reporter = Reporter()
    
    # Example 1: Count lines in current directory
    print("=== Example 1: Count lines in current directory ===")
    try:
        stats = counter.count_directory('.')
        
        # Print console report
        report = reporter.format_console_report(stats, show_files=True)
        print(report)
        
        # Export to different formats
        reporter.export_json(stats.__dict__, 'report.json')
        reporter.export_csv(stats, 'report.csv')
        reporter.export_markdown(stats, 'report.md')
        reporter.export_html(stats, 'report.html')
        
        print("\nReports exported to: report.json, report.csv, report.md, report.html")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Count specific files
    print("\n=== Example 2: Count specific files ===")
    try:
        # Create some example files
        with open('example.py', 'w') as f:
            f.write('''#!/usr/bin/env python3
# This is a Python example
"""
Docstring example
"""

def hello():
    """Say hello."""
    print("Hello, World!")  # Inline comment
    return True

# End of file
''')
        
        with open('example.js', 'w') as f:
            f.write('''// JavaScript example
/*
 * Multi-line comment
 */

function hello() {
    // Say hello
    console.log("Hello, World!");
    return true;
}

// End of file
''')
        
        # Count specific files
        file_paths = ['example.py', 'example.js']
        stats = counter.count_files(file_paths)
        
        print("Files analyzed:")
        for file_stats in stats.files:
            print(f"  {file_stats.file_path}: {file_stats.code_lines} code lines")
        
        # Clean up
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Custom ignore patterns
    print("\n=== Example 3: Custom ignore patterns ===")
    try:
        # Create files that should be ignored
        with open('temp.py', 'w') as f:
            f.write('print("temp")')
        
        with open('test.py', 'w') as f:
            f.write('print("test")')
        
        # Use custom ignore patterns
        custom_counter = CodeCounter(ignore_patterns=[r'temp\.py'])
        stats = custom_counter.count_directory('.')
        
        print(f"Files found: {stats.total_files}")
        for file_stats in stats.files:
            print(f"  {file_stats.file_path}")
        
        # Clean up
        for file_path in ['temp.py', 'test.py']:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()