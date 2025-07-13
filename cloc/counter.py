"""
Code Lines of Code Counter module.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass

from .utils import (
    LanguageConfig, get_language_from_extension, is_binary_file,
    should_ignore_file, get_file_size, get_relative_path
)


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
    
    def __post_init__(self):
        """Validate that total lines equals sum of other line types."""
        calculated_total = self.code_lines + self.comment_lines + self.blank_lines
        if self.total_lines != calculated_total:
            self.total_lines = calculated_total


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


class CodeCounter:
    """Main class for counting Lines of Code."""
    
    def __init__(self, ignore_patterns: Optional[List[str]] = None):
        """
        Initialize the CodeCounter.
        
        Args:
            ignore_patterns: List of patterns to ignore
        """
        self.ignore_patterns = ignore_patterns
        self._comment_patterns = LanguageConfig.COMMENT_PATTERNS
    
    def count_file(self, file_path: str) -> Optional[FileStats]:
        """
        Count Lines of Code for a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileStats object or None if file should be ignored
        """
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
        multiline_start_pattern = None
        multiline_end_pattern = None
        
        # Get comment patterns for the language
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
                if re.search(multiline_start_pattern, line):
                    in_multiline_comment = True
                    comment_lines += 1
                    continue
                    
                if in_multiline_comment:
                    comment_lines += 1
                    if re.search(multiline_end_pattern, line):
                        in_multiline_comment = False
                    continue
            
            # Check for single line comments
            if single_line_pattern and re.search(single_line_pattern, line):
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
        """
        Count Lines of Code for an entire directory.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            ProjectStats object
        """
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
    
    def count_files(self, file_paths: List[str]) -> ProjectStats:
        """
        Count Lines of Code for a list of files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            ProjectStats object
        """
        files = []
        language_stats = {}
        
        for file_path in file_paths:
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