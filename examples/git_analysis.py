#!/usr/bin/env python3
"""
Git analysis example for CLOC tool.
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cloc.git_analyzer import GitAnalyzer
from cloc.reporter import Reporter


def main():
    """Demonstrate Git analysis features of CLOC tool."""
    
    # Check if we're in a Git repository
    if not os.path.exists('.git'):
        print("This example requires a Git repository.")
        print("Please run this script from a Git repository directory.")
        return
    
    try:
        # Initialize the analyzer and reporter
        analyzer = GitAnalyzer('.')
        reporter = Reporter()
        
        # Example 1: Get repository information
        print("=== Example 1: Repository Information ===")
        repo_info = analyzer.get_repository_info()
        print(f"Repository Path: {repo_info['path']}")
        print(f"Active Branch: {repo_info['active_branch']}")
        print(f"Total Commits: {repo_info['total_commits']}")
        print(f"Last Commit: {repo_info['last_commit']['id']}")
        print(f"Last Commit Message: {repo_info['last_commit']['message']}")
        print(f"Last Commit Author: {repo_info['last_commit']['author']}")
        print(f"Last Commit Date: {repo_info['last_commit']['date']}")
        
        # Example 2: Analyze current state
        print("\n=== Example 2: Current Repository State ===")
        current_commit = analyzer.repo.head.commit
        stats = analyzer.analyze_commit(current_commit.hexsha)
        
        print(f"Current Commit: {stats.commit_id}")
        print(f"Author: {stats.author}")
        print(f"Message: {stats.message}")
        print(f"Date: {stats.commit_date}")
        print(f"Files: {stats.project_stats.total_files}")
        print(f"Code Lines: {stats.project_stats.code_lines}")
        print(f"Comment Lines: {stats.project_stats.comment_lines}")
        print(f"Blank Lines: {stats.project_stats.blank_lines}")
        
        # Example 3: Compare with previous commit
        print("\n=== Example 3: Compare with Previous Commit ===")
        try:
            # Get the previous commit
            commits = list(analyzer.repo.iter_commits())
            if len(commits) > 1:
                current_commit_id = commits[0].hexsha
                previous_commit_id = commits[1].hexsha
                
                comparison = analyzer.compare_commits(previous_commit_id, current_commit_id)
                
                print(f"Comparing {previous_commit_id[:8]} with {current_commit_id[:8]}")
                print(f"Added files: {len(comparison.added_files)}")
                print(f"Removed files: {len(comparison.removed_files)}")
                print(f"Modified files: {len(comparison.modified_files)}")
                
                if comparison.loc_changes:
                    print("\nLOC changes in modified files:")
                    for file_path, loc_change in comparison.loc_changes.items():
                        change_sign = "+" if loc_change >= 0 else ""
                        print(f"  {file_path}: {change_sign}{loc_change}")
                
                # Export comparison report
                reporter.export_json({
                    'comparison': {
                        'commit1': comparison.commit1.commit_id,
                        'commit2': comparison.commit2.commit_id,
                        'added_files': comparison.added_files,
                        'removed_files': comparison.removed_files,
                        'modified_files': comparison.modified_files,
                        'loc_changes': comparison.loc_changes
                    }
                }, 'git_comparison.json')
                print("\nComparison exported to: git_comparison.json")
            else:
                print("Not enough commits for comparison.")
                
        except Exception as e:
            print(f"Error during comparison: {e}")
        
        # Example 4: Analyze recent commits
        print("\n=== Example 4: Recent Commits Analysis ===")
        try:
            # Get last 5 commits
            recent_commits = list(analyzer.repo.iter_commits(max_count=5))
            
            print("Recent commits analysis:")
            for i, commit in enumerate(recent_commits):
                try:
                    stats = analyzer.analyze_commit(commit.hexsha)
                    print(f"  {i+1}. {commit.hexsha[:8]}: {stats.author} - {stats.message[:50]}...")
                    print(f"     Files: {stats.project_stats.total_files}, "
                          f"Code: {stats.project_stats.code_lines}, "
                          f"Comments: {stats.project_stats.comment_lines}")
                except Exception as e:
                    print(f"  {i+1}. {commit.hexsha[:8]}: Error analyzing - {e}")
                    
        except Exception as e:
            print(f"Error analyzing recent commits: {e}")
        
        # Example 5: Export current state to different formats
        print("\n=== Example 5: Export Current State ===")
        try:
            current_stats = analyzer.analyze_commit(analyzer.repo.head.commit.hexsha)
            
            # Export to different formats
            reporter.export_json(current_stats.__dict__, 'git_current_state.json')
            reporter.export_csv(current_stats.project_stats, 'git_current_state.csv')
            reporter.export_markdown(current_stats.project_stats, 'git_current_state.md')
            reporter.export_html(current_stats.project_stats, 'git_current_state.html')
            
            print("Current state exported to:")
            print("  - git_current_state.json")
            print("  - git_current_state.csv")
            print("  - git_current_state.md")
            print("  - git_current_state.html")
            
        except Exception as e:
            print(f"Error exporting current state: {e}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()