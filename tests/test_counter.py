"""
Test cases for the counter module.
"""

import os
import tempfile
import unittest
from pathlib import Path

from cloc.counter import CodeCounter, FileStats, ProjectStats


class TestCodeCounter(unittest.TestCase):
    """Test cases for CodeCounter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.counter = CodeCounter()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_file(self, filename: str, content: str) -> str:
        """Create a test file with given content."""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_count_python_file(self):
        """Test counting lines in a Python file."""
        content = '''#!/usr/bin/env python3
# This is a comment
"""
This is a docstring
with multiple lines
"""

def hello_world():
    """Print hello world."""
    print("Hello, World!")  # Inline comment
    
    # Another comment
    return True

# End of file
'''
        file_path = self.create_test_file('test.py', content)
        stats = self.counter.count_file(file_path)
        
        self.assertIsNotNone(stats)
        if stats is not None:  # Type guard for linter
            self.assertEqual(stats.language, 'Python')
            self.assertEqual(stats.total_lines, 15)
            self.assertEqual(stats.code_lines, 4)  # def, print, return, empty line
            self.assertEqual(stats.comment_lines, 9)  # # comments + docstring
            self.assertEqual(stats.blank_lines, 2)
    
    def test_count_javascript_file(self):
        """Test counting lines in a JavaScript file."""
        content = '''// This is a comment
/*
 * Multi-line comment
 * with multiple lines
 */

function helloWorld() {
    // Inline comment
    console.log("Hello, World!");
    
    return true;
}

// End of file
'''
        file_path = self.create_test_file('test.js', content)
        stats = self.counter.count_file(file_path)
        
        self.assertIsNotNone(stats)
        if stats is not None:  # Type guard for linter
            self.assertEqual(stats.language, 'JavaScript')
            self.assertEqual(stats.total_lines, 15)
            self.assertEqual(stats.code_lines, 4)  # function, console.log, return, empty line
            self.assertEqual(stats.comment_lines, 9)  # // comments + /* */ block
            self.assertEqual(stats.blank_lines, 2)
    
    def test_count_java_file(self):
        """Test counting lines in a Java file."""
        content = '''// This is a comment
/*
 * Multi-line comment
 * for Java
 */

public class HelloWorld {
    // Method comment
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        
        return;
    }
}

// End of file
'''
        file_path = self.create_test_file('HelloWorld.java', content)
        stats = self.counter.count_file(file_path)
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats.language, 'Java')
        self.assertEqual(stats.total_lines, 16)
        self.assertEqual(stats.code_lines, 6)  # public class, public static, System.out.println, return, empty lines
        self.assertEqual(stats.comment_lines, 8)  # // comments + /* */ block
        self.assertEqual(stats.blank_lines, 2)
    
    def test_ignore_binary_file(self):
        """Test that binary files are ignored."""
        # Create a file with binary content
        file_path = os.path.join(self.temp_dir, 'test.bin')
        with open(file_path, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
        
        stats = self.counter.count_file(file_path)
        self.assertIsNone(stats)
    
    def test_ignore_unknown_extension(self):
        """Test that files with unknown extensions are ignored."""
        file_path = self.create_test_file('test.xyz', 'Some content')
        stats = self.counter.count_file(file_path)
        self.assertIsNone(stats)
    
    def test_count_directory(self):
        """Test counting lines in a directory."""
        # Create multiple files
        self.create_test_file('test1.py', 'print("Hello")\n# comment\n')
        self.create_test_file('test2.js', 'console.log("World");\n// comment\n')
        self.create_test_file('test3.java', 'public class Test {}\n// comment\n')
        
        stats = self.counter.count_directory(self.temp_dir)
        
        self.assertIsInstance(stats, ProjectStats)
        self.assertEqual(stats.total_files, 3)
        self.assertEqual(len(stats.languages), 3)
        self.assertIn('Python', stats.languages)
        self.assertIn('JavaScript', stats.languages)
        self.assertIn('Java', stats.languages)
    
    def test_ignore_patterns(self):
        """Test that ignore patterns work correctly."""
        # Create files that should be ignored
        self.create_test_file('test.pyc', 'binary content')
        self.create_test_file('.gitignore', '*.pyc')
        self.create_test_file('__pycache__/test.py', 'print("test")')
        
        # Create a file that should not be ignored
        self.create_test_file('valid.py', 'print("valid")')
        
        counter = CodeCounter(ignore_patterns=[r'\.pyc$', r'__pycache__/', r'\.gitignore'])
        stats = counter.count_directory(self.temp_dir)
        
        self.assertEqual(stats.total_files, 1)  # Only valid.py should be counted
        self.assertIn('Python', stats.languages)
    
    def test_file_stats_validation(self):
        """Test that FileStats validation works correctly."""
        # Create a file with known line counts
        content = 'line1\nline2\n\nline4\n'
        file_path = self.create_test_file('test.py', content)
        
        stats = self.counter.count_file(file_path)
        
        # Verify that total_lines equals the sum of other line types
        if stats is not None:  # Type guard for linter
            calculated_total = stats.code_lines + stats.comment_lines + stats.blank_lines
            self.assertEqual(stats.total_lines, calculated_total)


if __name__ == '__main__':
    unittest.main()