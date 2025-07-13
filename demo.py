#!/usr/bin/env python3
"""
Demo script to test the CLOC tool.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloc.counter import CodeCounter
from cloc.reporter import Reporter


def create_demo_files():
    """Create demo files for testing."""
    
    # Create a Python file
    with open('demo.py', 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""
Demo Python file for CLOC testing.
"""

import os
import sys

# Configuration
DEBUG = True
VERSION = "1.0.0"

def main():
    """Main function."""
    print("Hello, World!")
    
    # Process arguments
    if len(sys.argv) > 1:
        print(f"Arguments: {sys.argv[1:]}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
''')
    
    # Create a JavaScript file
    with open('demo.js', 'w', encoding='utf-8') as f:
        f.write('''// Demo JavaScript file for CLOC testing

/**
 * Configuration object
 */
const config = {
    debug: true,
    version: "1.0.0"
};

/**
 * Main function
 * @returns {number} Exit code
 */
function main() {
    console.log("Hello, World!");
    
    // Process arguments
    const args = process.argv.slice(2);
    if (args.length > 0) {
        console.log(`Arguments: ${args.join(', ')}`);
    }
    
    return 0;
}

// Run main function
main();
''')
    
    # Create a Java file
    with open('Demo.java', 'w', encoding='utf-8') as f:
        f.write('''// Demo Java file for CLOC testing

/**
 * Demo class for CLOC testing
 */
public class Demo {
    
    // Configuration constants
    private static final boolean DEBUG = true;
    private static final String VERSION = "1.0.0";
    
    /**
     * Main method
     * @param args Command line arguments
     */
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        
        // Process arguments
        if (args.length > 0) {
            System.out.println("Arguments: " + String.join(", ", args));
        }
    }
}
''')


def main():
    """Main demo function."""
    
    print("=== CLOC Tool Demo ===")
    
    # Create demo files
    print("Creating demo files...")
    try:
        create_demo_files()
    except Exception as e:
        print(f"Error creating demo files: {e}")
        print("Continuing with existing files...")
    
    # Initialize counter and reporter
    counter = CodeCounter()
    reporter = Reporter()
    
    # Analyze current directory
    print("\nAnalyzing current directory...")
    try:
        stats = counter.count_directory('.')
    except Exception as e:
        print(f"Error analyzing directory: {e}")
        return

    # Print console report
    print("\nConsole Report:")
    report = reporter.format_console_report(stats, show_files=True)
    print(report)

    # Export to different formats
    print("\nExporting reports...")
    exported_files = []
    
    try:
        reporter.export_json(stats.__dict__, 'demo_report.json')
        exported_files.append('demo_report.json')
    except Exception as e:
        print(f"Warning: Failed to export JSON report: {e}")
    
    try:
        reporter.export_csv(stats, 'demo_report.csv')
        exported_files.append('demo_report.csv')
    except Exception as e:
        print(f"Warning: Failed to export CSV report: {e}")
    
    try:
        reporter.export_markdown(stats, 'demo_report.md')
        exported_files.append('demo_report.md')
    except Exception as e:
        print(f"Warning: Failed to export Markdown report: {e}")
    
    try:
        reporter.export_html(stats, 'demo_report.html')
        exported_files.append('demo_report.html')
    except Exception as e:
        print(f"Warning: Failed to export HTML report: {e}")
    
    if exported_files:
        print("Reports exported to:")
        for file_path in exported_files:
            print(f"  - {file_path}")
    else:
        print("Warning: No reports were successfully exported")

    # Clean up demo files
    print("\nCleaning up demo files...")
    cleanup_files = ['demo.py', 'demo.js', 'Demo.java']
    cleaned_files = []
    failed_cleanups = []
    
    for file_path in cleanup_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                cleaned_files.append(file_path)
        except Exception as e:
            print(f"Warning: Failed to remove {file_path}: {e}")
            failed_cleanups.append(file_path)
    
    if cleaned_files:
        print(f"Successfully cleaned up {len(cleaned_files)} files")
    if failed_cleanups:
        print(f"Warning: Failed to clean up {len(failed_cleanups)} files: {', '.join(failed_cleanups)}")

    print("Demo completed!")


if __name__ == '__main__':
    main()