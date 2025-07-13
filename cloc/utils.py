"""
Utility functions for CLOC tool.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


class LanguageConfig:
    """Configuration for different programming languages."""
    
    # File extensions mapped to language names
    EXTENSIONS = {
        # Python
        '.py': 'Python',
        '.pyw': 'Python',
        '.pyx': 'Python',
        '.pxd': 'Python',
        
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
        '.erb': 'Ruby',
        
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
    """
    Get programming language from file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Language name or None if not recognized
    """
    ext = Path(file_path).suffix.lower()
    return LanguageConfig.EXTENSIONS.get(ext)


def is_binary_file(file_path: str) -> bool:
    """
    Check if a file is binary.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is binary, False otherwise
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except (IOError, OSError):
        return True


def should_ignore_file(file_path: str, ignore_patterns: Optional[List[str]] = None) -> bool:
    """
    Check if a file should be ignored based on patterns.
    
    Args:
        file_path: Path to the file
        ignore_patterns: List of patterns to ignore
        
    Returns:
        True if file should be ignored, False otherwise
    """
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
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except (OSError, IOError):
        return 0


def format_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size_float = float(size_bytes)
    while size_float >= 1024 and i < len(size_names) - 1:
        size_float = size_float / 1024.0
        i += 1
    
    return f"{size_float:.1f} {size_names[i]}"


def get_relative_path(file_path: str, base_path: str) -> str:
    """
    Get relative path from base path.
    
    Args:
        file_path: Absolute file path
        base_path: Base directory path
        
    Returns:
        Relative path string
    """
    try:
        return os.path.relpath(file_path, base_path)
    except ValueError:
        return file_path