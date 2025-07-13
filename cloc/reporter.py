"""
Report generation module.
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from tabulate import tabulate
from colorama import Fore, Style, init

from .counter import ProjectStats, LanguageStats, FileStats
from .git_analyzer import CommitStats, CommitComparison

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class Reporter:
    """Report generator for CLOC tool."""
    
    def __init__(self):
        """Initialize the Reporter."""
        pass
    
    def format_console_report(self, stats: ProjectStats, show_files: bool = False) -> str:
        """
        Format project statistics for console output.
        
        Args:
            stats: ProjectStats object
            show_files: Whether to include individual file details
            
        Returns:
            Formatted string for console output
        """
        lines = []
        
        # Header
        lines.append(f"{Fore.CYAN}{'='*60}")
        lines.append(f"{Fore.CYAN}Code Lines of Code Counter Report")
        lines.append(f"{Fore.CYAN}{'='*60}")
        lines.append("")
        
        # Summary
        lines.append(f"{Fore.YELLOW}Summary:")
        lines.append(f"  Total Files: {Fore.GREEN}{stats.total_files:,}")
        lines.append(f"  Total Lines: {Fore.GREEN}{stats.total_lines:,}")
        lines.append(f"  Code Lines: {Fore.GREEN}{stats.code_lines:,}")
        lines.append(f"  Comment Lines: {Fore.GREEN}{stats.comment_lines:,}")
        lines.append(f"  Blank Lines: {Fore.GREEN}{stats.blank_lines:,}")
        lines.append("")
        
        # Language breakdown
        if stats.languages:
            lines.append(f"{Fore.YELLOW}Breakdown by Language:")
            
            # Prepare table data
            table_data = []
            for lang_stats in sorted(stats.languages.values(), key=lambda x: x.code_lines, reverse=True):
                table_data.append([
                    lang_stats.language,
                    f"{lang_stats.file_count:,}",
                    f"{lang_stats.total_lines:,}",
                    f"{Fore.GREEN}{lang_stats.code_lines:,}{Style.RESET_ALL}",
                    f"{lang_stats.comment_lines:,}",
                    f"{lang_stats.blank_lines:,}",
                    f"{lang_stats.total_size:,} B"
                ])
            
            headers = ["Language", "Files", "Total", "Code", "Comments", "Blanks", "Size"]
            table = tabulate(table_data, headers=headers, tablefmt="grid")
            lines.append(table)
            lines.append("")
        
        # Individual files (if requested)
        if show_files and stats.files:
            lines.append(f"{Fore.YELLOW}Individual Files:")
            
            # Group files by language
            files_by_lang = {}
            for file_stats in stats.files:
                lang = file_stats.language
                if lang not in files_by_lang:
                    files_by_lang[lang] = []
                files_by_lang[lang].append(file_stats)
            
            for language in sorted(files_by_lang.keys()):
                lines.append(f"\n{Fore.CYAN}{language}:")
                
                table_data = []
                for file_stats in sorted(files_by_lang[language], key=lambda x: x.code_lines, reverse=True):
                    table_data.append([
                        Path(file_stats.file_path).name,
                        f"{file_stats.total_lines:,}",
                        f"{Fore.GREEN}{file_stats.code_lines:,}{Style.RESET_ALL}",
                        f"{file_stats.comment_lines:,}",
                        f"{file_stats.blank_lines:,}",
                        f"{file_stats.file_size:,} B"
                    ])
                
                headers = ["File", "Total", "Code", "Comments", "Blanks", "Size"]
                table = tabulate(table_data, headers=headers, tablefmt="simple")
                lines.append(table)
        
        return "\n".join(lines)
    
    def format_commit_comparison_report(self, comparison: CommitComparison) -> str:
        """
        Format commit comparison for console output.
        
        Args:
            comparison: CommitComparison object
            
        Returns:
            Formatted string for console output
        """
        lines = []
        
        # Header
        lines.append(f"{Fore.CYAN}{'='*80}")
        lines.append(f"{Fore.CYAN}Commit Comparison Report")
        lines.append(f"{Fore.CYAN}{'='*80}")
        lines.append("")
        
        # Commit information
        lines.append(f"{Fore.YELLOW}Commit 1:")
        lines.append(f"  ID: {comparison.commit1.commit_id}")
        lines.append(f"  Date: {comparison.commit1.commit_date}")
        lines.append(f"  Author: {comparison.commit1.author}")
        lines.append(f"  Message: {comparison.commit1.message}")
        lines.append("")
        
        lines.append(f"{Fore.YELLOW}Commit 2:")
        lines.append(f"  ID: {comparison.commit2.commit_id}")
        lines.append(f"  Date: {comparison.commit2.commit_date}")
        lines.append(f"  Author: {comparison.commit2.author}")
        lines.append(f"  Message: {comparison.commit2.message}")
        lines.append("")
        
        # File changes summary
        lines.append(f"{Fore.YELLOW}File Changes:")
        lines.append(f"  Added: {Fore.GREEN}{len(comparison.added_files)}")
        lines.append(f"  Removed: {Fore.RED}{len(comparison.removed_files)}")
        lines.append(f"  Modified: {Fore.YELLOW}{len(comparison.modified_files)}")
        lines.append("")
        
        # LOC changes
        total_loc_change = sum(comparison.loc_changes.values())
        loc_change_color = Fore.GREEN if total_loc_change >= 0 else Fore.RED
        loc_change_sign = "+" if total_loc_change >= 0 else ""
        
        lines.append(f"{Fore.YELLOW}Lines of Code Changes:")
        lines.append(f"  Total Change: {loc_change_color}{loc_change_sign}{total_loc_change:,}")
        lines.append("")
        
        # Detailed LOC changes for modified files
        if comparison.loc_changes:
            lines.append(f"{Fore.YELLOW}Detailed LOC Changes:")
            
            table_data = []
            for file_path, loc_change in sorted(comparison.loc_changes.items(), key=lambda x: abs(x[1]), reverse=True):
                change_color = Fore.GREEN if loc_change >= 0 else Fore.RED
                change_sign = "+" if loc_change >= 0 else ""
                table_data.append([
                    Path(file_path).name,
                    f"{change_color}{change_sign}{loc_change:,}{Style.RESET_ALL}"
                ])
            
            headers = ["File", "LOC Change"]
            table = tabulate(table_data, headers=headers, tablefmt="grid")
            lines.append(table)
            lines.append("")
        
        # Statistics comparison
        lines.append(f"{Fore.YELLOW}Statistics Comparison:")
        
        stats1 = comparison.commit1.project_stats
        stats2 = comparison.commit2.project_stats
        
        comparison_data = [
            ["Files", f"{stats1.total_files:,}", f"{stats2.total_files:,}", 
             f"{stats2.total_files - stats1.total_files:+,}"],
            ["Total Lines", f"{stats1.total_lines:,}", f"{stats2.total_lines:,}", 
             f"{stats2.total_lines - stats1.total_lines:+,}"],
            ["Code Lines", f"{stats1.code_lines:,}", f"{stats2.code_lines:,}", 
             f"{stats2.code_lines - stats1.code_lines:+,}"],
            ["Comment Lines", f"{stats1.comment_lines:,}", f"{stats2.comment_lines:,}", 
             f"{stats2.comment_lines - stats1.comment_lines:+,}"],
            ["Blank Lines", f"{stats1.blank_lines:,}", f"{stats2.blank_lines:,}", 
             f"{stats2.blank_lines - stats1.blank_lines:+,}"],
        ]
        
        headers = ["Metric", "Commit 1", "Commit 2", "Difference"]
        table = tabulate(comparison_data, headers=headers, tablefmt="grid")
        lines.append(table)
        
        return "\n".join(lines)
    
    def export_json(self, data: Any, output_file: str) -> None:
        """
        Export data to JSON format.
        
        Args:
            data: Data to export
            output_file: Output file path
        """
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=serialize_datetime)
    
    def export_csv(self, stats: ProjectStats, output_file: str) -> None:
        """
        Export project statistics to CSV format.
        
        Args:
            stats: ProjectStats object
            output_file: Output file path
        """
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
    
    def export_markdown(self, stats: ProjectStats, output_file: str) -> None:
        """
        Export project statistics to Markdown format.
        
        Args:
            stats: ProjectStats object
            output_file: Output file path
        """
        lines = []
        
        # Header
        lines.append("# Code Lines of Code Counter Report")
        lines.append("")
        lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Files:** {stats.total_files:,}")
        lines.append(f"- **Total Lines:** {stats.total_lines:,}")
        lines.append(f"- **Code Lines:** {stats.code_lines:,}")
        lines.append(f"- **Comment Lines:** {stats.comment_lines:,}")
        lines.append(f"- **Blank Lines:** {stats.blank_lines:,}")
        lines.append("")
        
        # Language breakdown
        if stats.languages:
            lines.append("## Breakdown by Language")
            lines.append("")
            
            # Table header
            lines.append("| Language | Files | Total Lines | Code Lines | Comment Lines | Blank Lines | Size |")
            lines.append("|----------|-------|-------------|------------|---------------|-------------|------|")
            
            # Table data
            for lang_stats in sorted(stats.languages.values(), key=lambda x: x.code_lines, reverse=True):
                lines.append(
                    f"| {lang_stats.language} | {lang_stats.file_count:,} | "
                    f"{lang_stats.total_lines:,} | {lang_stats.code_lines:,} | "
                    f"{lang_stats.comment_lines:,} | {lang_stats.blank_lines:,} | "
                    f"{lang_stats.total_size:,} B |"
                )
            lines.append("")
        
        # Individual files
        if stats.files:
            lines.append("## Individual Files")
            lines.append("")
            
            # Group files by language
            files_by_lang = {}
            for file_stats in stats.files:
                lang = file_stats.language
                if lang not in files_by_lang:
                    files_by_lang[lang] = []
                files_by_lang[lang].append(file_stats)
            
            for language in sorted(files_by_lang.keys()):
                lines.append(f"### {language}")
                lines.append("")
                
                # Table header
                lines.append("| File | Total Lines | Code Lines | Comment Lines | Blank Lines | Size |")
                lines.append("|------|-------------|------------|---------------|-------------|------|")
                
                # Table data
                for file_stats in sorted(files_by_lang[language], key=lambda x: x.code_lines, reverse=True):
                    lines.append(
                        f"| {Path(file_stats.file_path).name} | {file_stats.total_lines:,} | "
                        f"{file_stats.code_lines:,} | {file_stats.comment_lines:,} | "
                        f"{file_stats.blank_lines:,} | {file_stats.file_size:,} B |"
                    )
                lines.append("")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def export_html(self, stats: ProjectStats, output_file: str) -> None:
        """
        Export project statistics to HTML format.
        
        Args:
            stats: ProjectStats object
            output_file: Output file path
        """
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CLOC Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .summary-item {{ margin: 10px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .language-section {{ margin: 30px 0; }}
        .file-section {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Code Lines of Code Counter Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-item"><strong>Total Files:</strong> {stats.total_files:,}</div>
        <div class="summary-item"><strong>Total Lines:</strong> {stats.total_lines:,}</div>
        <div class="summary-item"><strong>Code Lines:</strong> {stats.code_lines:,}</div>
        <div class="summary-item"><strong>Comment Lines:</strong> {stats.comment_lines:,}</div>
        <div class="summary-item"><strong>Blank Lines:</strong> {stats.blank_lines:,}</div>
    </div>
"""
        
        # Language breakdown
        if stats.languages:
            html += """
    <div class="language-section">
        <h2>Breakdown by Language</h2>
        <table>
            <thead>
                <tr>
                    <th>Language</th>
                    <th>Files</th>
                    <th>Total Lines</th>
                    <th>Code Lines</th>
                    <th>Comment Lines</th>
                    <th>Blank Lines</th>
                    <th>Size</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for lang_stats in sorted(stats.languages.values(), key=lambda x: x.code_lines, reverse=True):
                html += f"""
                <tr>
                    <td>{lang_stats.language}</td>
                    <td>{lang_stats.file_count:,}</td>
                    <td>{lang_stats.total_lines:,}</td>
                    <td>{lang_stats.code_lines:,}</td>
                    <td>{lang_stats.comment_lines:,}</td>
                    <td>{lang_stats.blank_lines:,}</td>
                    <td>{lang_stats.total_size:,} B</td>
                </tr>
"""
            
            html += """
            </tbody>
        </table>
    </div>
"""
        
        # Individual files
        if stats.files:
            # Group files by language
            files_by_lang = {}
            for file_stats in stats.files:
                lang = file_stats.language
                if lang not in files_by_lang:
                    files_by_lang[lang] = []
                files_by_lang[lang].append(file_stats)
            
            for language in sorted(files_by_lang.keys()):
                html += f"""
    <div class="file-section">
        <h3>{language}</h3>
        <table>
            <thead>
                <tr>
                    <th>File</th>
                    <th>Total Lines</th>
                    <th>Code Lines</th>
                    <th>Comment Lines</th>
                    <th>Blank Lines</th>
                    <th>Size</th>
                </tr>
            </thead>
            <tbody>
"""
                
                for file_stats in sorted(files_by_lang[language], key=lambda x: x.code_lines, reverse=True):
                    html += f"""
                <tr>
                    <td>{Path(file_stats.file_path).name}</td>
                    <td>{file_stats.total_lines:,}</td>
                    <td>{file_stats.code_lines:,}</td>
                    <td>{file_stats.comment_lines:,}</td>
                    <td>{file_stats.blank_lines:,}</td>
                    <td>{file_stats.file_size:,} B</td>
                </tr>
"""
                
                html += """
            </tbody>
        </table>
    </div>
"""
        
        html += """
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)