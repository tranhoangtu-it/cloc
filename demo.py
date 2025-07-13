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
    create_demo_files()
    
    # Initialize counter and reporter
    counter = CodeCounter()
    reporter = Reporter()
    
    # Analyze current directory
    print("\nAnalyzing current directory...")
    stats = counter.count_directory('.')
    
    # Print console report
    print("\nConsole Report:")
    report = reporter.format_console_report(stats, show_files=True)
    print(report)
    
    # Export to different formats
    print("\nExporting reports...")
    reporter.export_json(stats.__dict__, 'demo_report.json')
    reporter.export_csv(stats, 'demo_report.csv')
    reporter.export_markdown(stats, 'demo_report.md')
    reporter.export_html(stats, 'demo_report.html')
    
    print("Reports exported to:")
    print("  - demo_report.json")
    print("  - demo_report.csv")
    print("  - demo_report.md")
    print("  - demo_report.html")
    
    # Clean up demo files
    print("\nCleaning up demo files...")
    for file_path in ['demo.py', 'demo.js', 'Demo.java']:
        if os.path.exists(file_path):
            os.remove(file_path)
    
    print("Demo completed!")


if __name__ == '__main__':
    main()