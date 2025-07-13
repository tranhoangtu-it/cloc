"""
Command Line Interface for CLOC tool.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

from .counter import CodeCounter
from .git_analyzer import GitAnalyzer
from .reporter import Reporter


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        description="Code Lines of Code Counter - Analyze code metrics in Git repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count LoC in current directory
  cloc --path .

  # Compare two commits
  cloc --path . --commit-id-1 abc123 --commit-id-2 def456

  # Analyze commits in date range
  cloc --path . --start-date 2024-01-01 --end-date 2024-12-31

  # Export to JSON
  cloc --path . --output-format json --output-file report.json

  # Show detailed file information
  cloc --path . --show-files
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to the directory or Git repository to analyze (default: current directory)'
    )
    
    # Git analysis options
    git_group = parser.add_argument_group('Git Analysis')
    git_group.add_argument(
        '--commit-id-1',
        type=str,
        help='First commit ID for comparison'
    )
    git_group.add_argument(
        '--commit-id-2',
        type=str,
        help='Second commit ID for comparison'
    )
    git_group.add_argument(
        '--start-date',
        type=str,
        help='Start date for time range analysis (YYYY-MM-DD)'
    )
    git_group.add_argument(
        '--end-date',
        type=str,
        help='End date for time range analysis (YYYY-MM-DD)'
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--output-format',
        choices=['console', 'json', 'csv', 'markdown', 'html'],
        default='console',
        help='Output format (default: console)'
    )
    output_group.add_argument(
        '--output-file',
        type=str,
        help='Output file path (required for non-console formats)'
    )
    output_group.add_argument(
        '--show-files',
        action='store_true',
        help='Show detailed information for individual files'
    )
    
    # Filtering options
    filter_group = parser.add_argument_group('Filtering Options')
    filter_group.add_argument(
        '--ignore-patterns',
        type=str,
        nargs='+',
        help='Additional patterns to ignore (regex)'
    )
    filter_group.add_argument(
        '--languages',
        type=str,
        nargs='+',
        help='Only analyze specific languages'
    )
    
    # Repository information
    info_group = parser.add_argument_group('Repository Information')
    info_group.add_argument(
        '--repo-info',
        action='store_true',
        help='Show repository information'
    )
    
    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    """
    Validate command line arguments.
    
    Args:
        args: Parsed arguments
        
    Raises:
        ValueError: If arguments are invalid
    """
    # Check if path exists
    if not os.path.exists(args.path):
        raise ValueError(f"Path does not exist: {args.path}")
    
    # Check commit comparison arguments
    if args.commit_id_1 and not args.commit_id_2:
        raise ValueError("--commit-id-2 is required when --commit-id-1 is specified")
    if args.commit_id_2 and not args.commit_id_1:
        raise ValueError("--commit-id-1 is required when --commit-id-2 is specified")
    
    # Check date range arguments
    if args.start_date and not args.end_date:
        raise ValueError("--end-date is required when --start-date is specified")
    if args.end_date and not args.start_date:
        raise ValueError("--start-date is required when --end-date is specified")
    
    # Check output file for non-console formats
    if args.output_format != 'console' and not args.output_file:
        raise ValueError(f"--output-file is required for {args.output_format} format")
    
    # Check if output directory exists
    if args.output_file:
        output_dir = os.path.dirname(args.output_file)
        if output_dir and not os.path.exists(output_dir):
            raise ValueError(f"Output directory does not exist: {output_dir}")


def analyze_directory(args: argparse.Namespace) -> None:
    """
    Analyze a directory and generate report.
    
    Args:
        args: Parsed arguments
    """
    counter = CodeCounter(ignore_patterns=args.ignore_patterns)
    reporter = Reporter()
    
    try:
        print(f"Analyzing directory: {args.path}")
        stats = counter.count_directory(args.path)
        
        if args.output_format == 'console':
            report = reporter.format_console_report(stats, show_files=args.show_files)
            print(report)
        elif args.output_format == 'json':
            reporter.export_json(stats.__dict__, args.output_file)
            print(f"Report exported to: {args.output_file}")
        elif args.output_format == 'csv':
            reporter.export_csv(stats, args.output_file)
            print(f"Report exported to: {args.output_file}")
        elif args.output_format == 'markdown':
            reporter.export_markdown(stats, args.output_file)
            print(f"Report exported to: {args.output_file}")
        elif args.output_format == 'html':
            reporter.export_html(stats, args.output_file)
            print(f"Report exported to: {args.output_file}")
    
    except Exception as e:
        print(f"Error analyzing directory: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_git_repository(args: argparse.Namespace) -> None:
    """
    Analyze a Git repository and generate report.
    
    Args:
        args: Parsed arguments
    """
    try:
        analyzer = GitAnalyzer(args.path)
        reporter = Reporter()
        
        if args.repo_info:
            # Show repository information
            repo_info = analyzer.get_repository_info()
            print("Repository Information:")
            print(f"  Path: {repo_info['path']}")
            print(f"  Active Branch: {repo_info['active_branch']}")
            print(f"  Total Commits: {repo_info['total_commits']}")
            print(f"  Last Commit: {repo_info['last_commit']['id']}")
            print(f"  Last Commit Message: {repo_info['last_commit']['message']}")
            print(f"  Last Commit Author: {repo_info['last_commit']['author']}")
            print(f"  Last Commit Date: {repo_info['last_commit']['date']}")
            return
        
        if args.commit_id_1 and args.commit_id_2:
            # Compare two commits
            print(f"Comparing commits: {args.commit_id_1} and {args.commit_id_2}")
            comparison = analyzer.compare_commits(args.commit_id_1, args.commit_id_2)
            
            if args.output_format == 'console':
                report = reporter.format_commit_comparison_report(comparison)
                print(report)
            elif args.output_format == 'json':
                # Convert comparison to dict for JSON export
                comparison_dict = {
                    'commit1': {
                        'id': comparison.commit1.commit_id,
                        'date': comparison.commit1.commit_date,
                        'author': comparison.commit1.author,
                        'message': comparison.commit1.message,
                        'stats': comparison.commit1.project_stats.__dict__
                    },
                    'commit2': {
                        'id': comparison.commit2.commit_id,
                        'date': comparison.commit2.commit_date,
                        'author': comparison.commit2.author,
                        'message': comparison.commit2.message,
                        'stats': comparison.commit2.project_stats.__dict__
                    },
                    'file_changes': {
                        'added': comparison.added_files,
                        'removed': comparison.removed_files,
                        'modified': comparison.modified_files
                    },
                    'loc_changes': comparison.loc_changes
                }
                reporter.export_json(comparison_dict, args.output_file)
                print(f"Comparison report exported to: {args.output_file}")
        
        elif args.start_date and args.end_date:
            # Analyze commits in time range
            print(f"Analyzing commits from {args.start_date} to {args.end_date}")
            commit_stats = analyzer.analyze_time_range(args.start_date, args.end_date)
            
            if args.output_format == 'console':
                print(f"Found {len(commit_stats)} commits in the specified time range:")
                for stats in commit_stats:
                    print(f"  {stats.commit_id}: {stats.author} - {stats.message[:50]}...")
                    print(f"    Files: {stats.project_stats.total_files}, "
                          f"Code Lines: {stats.project_stats.code_lines}")
            elif args.output_format == 'json':
                # Convert to list of dicts for JSON export
                stats_list = []
                for stats in commit_stats:
                    stats_list.append({
                        'commit_id': stats.commit_id,
                        'date': stats.commit_date,
                        'author': stats.author,
                        'message': stats.message,
                        'stats': stats.project_stats.__dict__
                    })
                reporter.export_json(stats_list, args.output_file)
                print(f"Time range analysis exported to: {args.output_file}")
        
        else:
            # Analyze current state
            print("Analyzing current repository state")
            current_commit = analyzer.repo.head.commit
            stats = analyzer.analyze_commit(current_commit.hexsha)
            
            if args.output_format == 'console':
                report = reporter.format_console_report(stats.project_stats, show_files=args.show_files)
                print(report)
            elif args.output_format == 'json':
                reporter.export_json(stats.__dict__, args.output_file)
                print(f"Report exported to: {args.output_file}")
            elif args.output_format == 'csv':
                reporter.export_csv(stats.project_stats, args.output_file)
                print(f"Report exported to: {args.output_file}")
            elif args.output_format == 'markdown':
                reporter.export_markdown(stats.project_stats, args.output_file)
                print(f"Report exported to: {args.output_file}")
            elif args.output_format == 'html':
                reporter.export_html(stats.project_stats, args.output_file)
                print(f"Report exported to: {args.output_file}")
    
    except Exception as e:
        print(f"Error analyzing Git repository: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """
    Main entry point for the CLOC tool.
    """
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Validate arguments
        validate_arguments(args)
        
        # Check if it's a Git repository
        git_dir = os.path.join(args.path, '.git')
        if os.path.exists(git_dir) or args.commit_id_1 or args.commit_id_2 or args.start_date or args.end_date or args.repo_info:
            analyze_git_repository(args)
        else:
            analyze_directory(args)
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()