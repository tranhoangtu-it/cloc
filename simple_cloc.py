#!/usr/bin/env python3
"""
Simple Code Lines of Code Counter (CLOC) - Version without Git dependencies.

A simplified version for testing the core functionality.
"""

import os
import re
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class FileStats:
    """Statistics for a single file."""
    file_path: str
    language: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    file_size: int


@dataclass
class LanguageStats:
    """Statistics aggregated by language."""
    language: str
    file_count: int
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    total_size: int


@dataclass
class ProjectStats:
    """Overall project statistics."""
    total_files: int
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    total_size: int
    languages: Dict[str, LanguageStats]
    files: List[FileStats]


class LanguageConfig:
    """Configuration for different programming languages."""
    
    # File extensions mapped to language names
    EXTENSIONS = {
        # Python
        '.py': 'Python',
        '.pyw': 'Python',
        
        # JavaScript/TypeScript
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        
        # Java
        '.java': 'Java',
        
        # C/C++
        '.c': 'C',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.h': 'C/C++',
        '.hpp': 'C++',
        '.hxx': 'C++',
        
        # Go
        '.go': 'Go',
        
        # Ruby
        '.rb': 'Ruby',
        
        # PHP
        '.php': 'PHP',
        
        # C#
        '.cs': 'C#',
        
        # Rust
        '.rs': 'Rust',
        
        # Swift
        '.swift': 'Swift',
        
        # Kotlin
        '.kt': 'Kotlin',
        '.kts': 'Kotlin',
        
        # Scala
        '.scala': 'Scala',
        
        # Shell scripts
        '.sh': 'Shell',
        '.bash': 'Shell',
        '.zsh': 'Shell',
        
        # HTML/CSS
        '.html': 'HTML',
        '.htm': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        
        # Markup
        '.md': 'Markdown',
        '.xml': 'XML',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.toml': 'TOML',
        '.ini': 'INI',
        '.cfg': 'INI',
        '.conf': 'INI',
    }
    
    # Comment patterns for different languages
    COMMENT_PATTERNS = {
        'Python': {
            'single_line': r'#.*$',
            'multi_line_start': r'"""|\'\'\'',
            'multi_line_end': r'"""|\'\'\'',
        },
        'JavaScript': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'TypeScript': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Java': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'C': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'C++': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Go': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Ruby': {
            'single_line': r'#.*$',
            'multi_line_start': r'=begin',
            'multi_line_end': r'=end',
        },
        'PHP': {
            'single_line': r'//.*$|#.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'C#': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Rust': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Swift': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Kotlin': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Scala': {
            'single_line': r'//.*$',
            'multi_line_start': r'/\*',
            'multi_line_end': r'\*/',
        },
        'Shell': {
            'single_line': r'#.*$',
            'multi_line_start': None,
            'multi_line_end': None,
        },
    }


def get_language_from_extension(file_path: str) -> Optional[str]:
    """Get programming language from file extension."""
    ext = Path(file_path).suffix.lower()
    return LanguageConfig.EXTENSIONS.get(ext)


def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except (IOError, OSError):
        return True


def should_ignore_file(file_path: str, ignore_patterns: Optional[List[str]] = None) -> bool:
    """Check if a file should be ignored based on patterns."""
    if ignore_patterns is None:
        ignore_patterns = [
            r'\.git/',
            r'\.svn/',
            r'\.hg/',
            r'__pycache__/',
            r'\.pyc$',
            r'\.pyo$',
            r'\.pyd$',
            r'\.so$',
            r'\.dll$',
            r'\.exe$',
            r'\.o$',
            r'\.a$',
            r'\.lib$',
            r'\.dylib$',
            r'\.class$',
            r'\.jar$',
            r'\.war$',
            r'\.ear$',
            r'\.zip$',
            r'\.tar$',
            r'\.gz$',
            r'\.bz2$',
            r'\.xz$',
            r'\.7z$',
            r'\.rar$',
            r'node_modules/',
            r'vendor/',
            r'\.venv/',
            r'venv/',
            r'env/',
            r'\.env/',
            r'\.idea/',
            r'\.vscode/',
            r'\.DS_Store$',
            r'Thumbs\.db$',
        ]
    
    file_path_str = str(file_path)
    for pattern in ignore_patterns:
        if re.search(pattern, file_path_str, re.IGNORECASE):
            return True
    
    return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except (OSError, IOError):
        return 0


class SimpleCodeCounter:
    """Simple code counter without Git dependencies."""
    
    def __init__(self, ignore_patterns: Optional[List[str]] = None):
        """Initialize the SimpleCodeCounter."""
        self.ignore_patterns = ignore_patterns
        self._comment_patterns = LanguageConfig.COMMENT_PATTERNS
    
    def count_file(self, file_path: str) -> Optional[FileStats]:
        """Count Lines of Code for a single file."""
        if not os.path.isfile(file_path):
            return None
            
        if should_ignore_file(file_path, self.ignore_patterns):
            return None
            
        if is_binary_file(file_path):
            return None
            
        language = get_language_from_extension(file_path)
        if not language:
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except (IOError, OSError, UnicodeDecodeError):
            return None
            
        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        in_multiline_comment = False
        
        # Get comment patterns for the language
        single_line_pattern = None
        multiline_start_pattern = None
        multiline_end_pattern = None
        
        if language in self._comment_patterns:
            patterns = self._comment_patterns[language]
            single_line_pattern = patterns.get('single_line')
            multiline_start_pattern = patterns.get('multi_line_start')
            multiline_end_pattern = patterns.get('multi_line_end')
        
        for line in lines:
            line = line.rstrip('\r\n')
            
            # Check for blank lines
            if not line.strip():
                blank_lines += 1
                continue
                
            # Check for multiline comments
            if multiline_start_pattern and multiline_end_pattern:
                # Check if multiline comment starts and ends on the same line
                if re.search(multiline_start_pattern, line) and re.search(multiline_end_pattern, line):
                    comment_lines += 1
                    continue
                
                # Check if multiline comment starts
                if re.search(multiline_start_pattern, line):
                    in_multiline_comment = True
                    comment_lines += 1
                    continue
                
                # Check if we're in a multiline comment
                if in_multiline_comment:
                    comment_lines += 1
                    # Check if multiline comment ends
                    if re.search(multiline_end_pattern, line):
                        in_multiline_comment = False
                    continue
            
            # Check for single line comments (only if not in multiline comment)
            if not in_multiline_comment and single_line_pattern and re.search(single_line_pattern, line):
                comment_lines += 1
                continue
                
            # If we reach here, it's a code line
            code_lines += 1
        
        file_size = get_file_size(file_path)
        
        return FileStats(
            file_path=file_path,
            language=language,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            file_size=file_size
        )
    
    def count_directory(self, directory_path: str) -> ProjectStats:
        """Count Lines of Code for an entire directory."""
        if not os.path.isdir(directory_path):
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        files = []
        language_stats = {}
        
        for root, dirs, filenames in os.walk(directory_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not should_ignore_file(os.path.join(root, d), self.ignore_patterns)]
            
            for filename in filenames:
                file_path = os.path.join(root, filename)
                file_stats = self.count_file(file_path)
                
                if file_stats:
                    files.append(file_stats)
                    
                    # Aggregate by language
                    language = file_stats.language
                    if language not in language_stats:
                        language_stats[language] = LanguageStats(
                            language=language,
                            file_count=0,
                            total_lines=0,
                            code_lines=0,
                            comment_lines=0,
                            blank_lines=0,
                            total_size=0
                        )
                    
                    lang_stats = language_stats[language]
                    lang_stats.file_count += 1
                    lang_stats.total_lines += file_stats.total_lines
                    lang_stats.code_lines += file_stats.code_lines
                    lang_stats.comment_lines += file_stats.comment_lines
                    lang_stats.blank_lines += file_stats.blank_lines
                    lang_stats.total_size += file_stats.file_size
        
        # Calculate totals
        total_files = len(files)
        total_lines = sum(f.total_lines for f in files)
        code_lines = sum(f.code_lines for f in files)
        comment_lines = sum(f.comment_lines for f in files)
        blank_lines = sum(f.blank_lines for f in files)
        total_size = sum(f.file_size for f in files)
        
        return ProjectStats(
            total_files=total_files,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            total_size=total_size,
            languages=language_stats,
            files=files
        )


class SimpleReporter:
    """Simple report generator without external dependencies."""
    
    def format_console_report(self, stats: ProjectStats, show_files: bool = False) -> str:
        """Format project statistics for console output."""
        lines = []
        
        # Header
        lines.append("=" * 60)
        lines.append("Code Lines of Code Counter Report")
        lines.append("=" * 60)
        lines.append("")
        
        # Summary
        lines.append("Summary:")
        lines.append(f"  Total Files: {stats.total_files:,}")
        lines.append(f"  Total Lines: {stats.total_lines:,}")
        lines.append(f"  Code Lines: {stats.code_lines:,}")
        lines.append(f"  Comment Lines: {stats.comment_lines:,}")
        lines.append(f"  Blank Lines: {stats.blank_lines:,}")
        lines.append("")
        
        # Language breakdown
        if stats.languages:
            lines.append("Breakdown by Language:")
            lines.append("")
            
            # Table header
            lines.append(f"{'Language':<15} {'Files':<8} {'Total':<8} {'Code':<8} {'Comments':<10} {'Blanks':<8} {'Size':<10}")
            lines.append("-" * 80)
            
            # Table data
            for lang_stats in sorted(stats.languages.values(), key=lambda x: x.code_lines, reverse=True):
                lines.append(
                    f"{lang_stats.language:<15} {lang_stats.file_count:<8,} "
                    f"{lang_stats.total_lines:<8,} {lang_stats.code_lines:<8,} "
                    f"{lang_stats.comment_lines:<10,} {lang_stats.blank_lines:<8,} "
                    f"{lang_stats.total_size:<10,} B"
                )
            lines.append("")
        
        # Individual files (if requested)
        if show_files and stats.files:
            lines.append("Individual Files:")
            lines.append("")
            
            # Group files by language
            files_by_lang = {}
            for file_stats in stats.files:
                lang = file_stats.language
                if lang not in files_by_lang:
                    files_by_lang[lang] = []
                files_by_lang[lang].append(file_stats)
            
            for language in sorted(files_by_lang.keys()):
                lines.append(f"\n{language}:")
                lines.append(f"{'File':<30} {'Total':<8} {'Code':<8} {'Comments':<10} {'Blanks':<8} {'Size':<10}")
                lines.append("-" * 80)
                
                for file_stats in sorted(files_by_lang[language], key=lambda x: x.code_lines, reverse=True):
                    lines.append(
                        f"{Path(file_stats.file_path).name:<30} {file_stats.total_lines:<8,} "
                        f"{file_stats.code_lines:<8,} {file_stats.comment_lines:<10,} "
                        f"{file_stats.blank_lines:<8,} {file_stats.file_size:<10,} B"
                    )
        
        return "\n".join(lines)
    
    def export_json(self, data: Any, output_file: str) -> None:
        """Export data to JSON format."""
        def serialize_datetime(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        def serialize_dataclass(obj):
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            return str(obj)
        
        def custom_serializer(obj):
            try:
                return serialize_datetime(obj)
            except TypeError:
                try:
                    return serialize_dataclass(obj)
                except:
                    return str(obj)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=custom_serializer)
    
    def export_csv(self, stats: ProjectStats, output_file: str) -> None:
        """Export project statistics to CSV format."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Language', 'Files', 'Total Lines', 'Code Lines', 'Comment Lines', 'Blank Lines', 'Size (bytes)'])
            
            # Write data
            for lang_stats in sorted(stats.languages.values(), key=lambda x: x.code_lines, reverse=True):
                writer.writerow([
                    lang_stats.language,
                    lang_stats.file_count,
                    lang_stats.total_lines,
                    lang_stats.code_lines,
                    lang_stats.comment_lines,
                    lang_stats.blank_lines,
                    lang_stats.total_size
                ])


def main():
    """Main function for simple CLOC tool."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Simple Code Lines of Code Counter")
    parser.add_argument('--path', type=str, default='.', help='Path to analyze (default: current directory)')
    parser.add_argument('--show-files', action='store_true', help='Show individual file details')
    parser.add_argument('--output-format', choices=['console', 'json', 'csv'], default='console', help='Output format')
    parser.add_argument('--output-file', type=str, help='Output file path')
    
    args = parser.parse_args()
    
    try:
        # Initialize counter and reporter
        counter = SimpleCodeCounter()
        reporter = SimpleReporter()
        
        # Analyze directory
        print(f"Analyzing directory: {args.path}")
        stats = counter.count_directory(args.path)
        
        if args.output_format == 'console':
            report = reporter.format_console_report(stats, show_files=args.show_files)
            print(report)
        elif args.output_format == 'json':
            if not args.output_file:
                args.output_file = 'cloc_report.json'
            reporter.export_json(stats.__dict__, args.output_file)
            print(f"Report exported to: {args.output_file}")
        elif args.output_format == 'csv':
            if not args.output_file:
                args.output_file = 'cloc_report.csv'
            reporter.export_csv(stats, args.output_file)
            print(f"Report exported to: {args.output_file}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()