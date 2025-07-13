"""
Git repository analyzer module.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

import git
from git import Repo, Commit, Tree, Blob

from .counter import CodeCounter, ProjectStats, FileStats
from .utils import get_relative_path


@dataclass
class CommitStats:
    """Statistics for a specific commit."""
    commit_id: str
    commit_date: datetime
    author: str
    message: str
    project_stats: ProjectStats


@dataclass
class CommitComparison:
    """Comparison between two commits."""
    commit1: CommitStats
    commit2: CommitStats
    added_files: List[str]
    removed_files: List[str]
    modified_files: List[str]
    loc_changes: Dict[str, int]  # file_path -> loc_change


class GitAnalyzer:
    """Analyzer for Git repositories."""
    
    def __init__(self, repo_path: str):
        """
        Initialize the GitAnalyzer.
        
        Args:
            repo_path: Path to the Git repository
        """
        self.repo_path = os.path.abspath(repo_path)
        self.repo = Repo(self.repo_path)
        self.counter = CodeCounter()
        
        if not self.repo.git_dir:
            raise ValueError(f"Not a valid Git repository: {repo_path}")
    
    def get_commit(self, commit_id: str) -> Commit:
        """
        Get a specific commit by ID.
        
        Args:
            commit_id: Commit hash or reference
            
        Returns:
            Git commit object
        """
        try:
            return self.repo.commit(commit_id)
        except git.BadName:
            raise ValueError(f"Invalid commit ID: {commit_id}")
    
    def get_commits_in_range(self, start_date: str, end_date: str) -> List[Commit]:
        """
        Get commits within a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of commits in the date range
        """
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date format should be YYYY-MM-DD")
        
        commits = []
        for commit in self.repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date)
            if start_dt <= commit_date <= end_dt:
                commits.append(commit)
        
        return commits
    
    def get_file_content_at_commit(self, file_path: str, commit: Commit) -> Optional[str]:
        """
        Get file content at a specific commit.
        
        Args:
            file_path: Path to the file (relative to repo root)
            commit: Git commit object
            
        Returns:
            File content as string or None if file doesn't exist
        """
        try:
            tree = commit.tree
            blob = tree[file_path]
            return blob.data_stream.read().decode('utf-8', errors='ignore')
        except (KeyError, AttributeError, UnicodeDecodeError):
            return None
    
    def get_files_at_commit(self, commit: Commit) -> List[str]:
        """
        Get all files in the repository at a specific commit.
        
        Args:
            commit: Git commit object
            
        Returns:
            List of file paths
        """
        files = []
        
        def traverse_tree(tree: Tree, prefix: str = ""):
            for item in tree:
                if isinstance(item, Blob):
                    file_path = os.path.join(prefix, item.name) if prefix else item.name
                    files.append(file_path)
                elif isinstance(item, Tree):
                    new_prefix = os.path.join(prefix, item.name) if prefix else item.name
                    traverse_tree(item, new_prefix)
        
        traverse_tree(commit.tree)
        return files
    
    def analyze_commit(self, commit_id: str) -> CommitStats:
        """
        Analyze a specific commit and return statistics.
        
        Args:
            commit_id: Commit hash or reference
            
        Returns:
            CommitStats object
        """
        commit = self.get_commit(commit_id)
        files = self.get_files_at_commit(commit)
        
        # Create temporary files to analyze
        temp_files = []
        file_contents = {}
        
        try:
            for file_path in files:
                content = self.get_file_content_at_commit(file_path, commit)
                if content is not None:
                    # Create temporary file
                    temp_file_path = os.path.join(self.repo_path, f"temp_{commit_id}_{file_path.replace('/', '_')}")
                    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                    
                    with open(temp_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    temp_files.append(temp_file_path)
                    file_contents[temp_file_path] = content
            
            # Analyze the temporary files
            project_stats = self.counter.count_files(temp_files)
            
            return CommitStats(
                commit_id=commit_id,
                commit_date=datetime.fromtimestamp(commit.committed_date),
                author=commit.author.name,
                message=commit.message.strip(),
                project_stats=project_stats
            )
        
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except OSError:
                    pass
    
    def compare_commits(self, commit_id1: str, commit_id2: str) -> CommitComparison:
        """
        Compare two commits and return differences.
        
        Args:
            commit_id1: First commit hash or reference
            commit_id2: Second commit hash or reference
            
        Returns:
            CommitComparison object
        """
        commit1 = self.get_commit(commit_id1)
        commit2 = self.get_commit(commit_id2)
        
        # Get file differences
        diff = commit1.diff(commit2)
        
        added_files = []
        removed_files = []
        modified_files = []
        
        for change in diff:
            if change.change_type == 'A':  # Added
                added_files.append(change.a_path)
            elif change.change_type == 'D':  # Deleted
                removed_files.append(change.a_path)
            elif change.change_type == 'M':  # Modified
                modified_files.append(change.a_path)
            elif change.change_type == 'R':  # Renamed
                removed_files.append(change.a_path)
                added_files.append(change.b_path)
        
        # Analyze both commits
        stats1 = self.analyze_commit(commit_id1)
        stats2 = self.analyze_commit(commit_id2)
        
        # Calculate LOC changes for modified files
        loc_changes = {}
        for file_path in modified_files:
            content1 = self.get_file_content_at_commit(file_path, commit1)
            content2 = self.get_file_content_at_commit(file_path, commit2)
            
            if content1 is not None and content2 is not None:
                # Create temporary files for comparison
                temp_file1 = os.path.join(self.repo_path, f"temp_comp1_{file_path.replace('/', '_')}")
                temp_file2 = os.path.join(self.repo_path, f"temp_comp2_{file_path.replace('/', '_')}")
                
                try:
                    os.makedirs(os.path.dirname(temp_file1), exist_ok=True)
                    os.makedirs(os.path.dirname(temp_file2), exist_ok=True)
                    
                    with open(temp_file1, 'w', encoding='utf-8') as f:
                        f.write(content1)
                    with open(temp_file2, 'w', encoding='utf-8') as f:
                        f.write(content2)
                    
                    stats1_file = self.counter.count_file(temp_file1)
                    stats2_file = self.counter.count_file(temp_file2)
                    
                    if stats1_file and stats2_file:
                        loc_change = stats2_file.code_lines - stats1_file.code_lines
                        loc_changes[file_path] = loc_change
                
                finally:
                    # Clean up
                    for temp_file in [temp_file1, temp_file2]:
                        try:
                            os.remove(temp_file)
                        except OSError:
                            pass
        
        return CommitComparison(
            commit1=stats1,
            commit2=stats2,
            added_files=added_files,
            removed_files=removed_files,
            modified_files=modified_files,
            loc_changes=loc_changes
        )
    
    def analyze_time_range(self, start_date: str, end_date: str) -> List[CommitStats]:
        """
        Analyze all commits in a time range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of CommitStats objects
        """
        commits = self.get_commits_in_range(start_date, end_date)
        commit_stats = []
        
        for commit in commits:
            try:
                stats = self.analyze_commit(commit.hexsha)
                commit_stats.append(stats)
            except Exception as e:
                print(f"Warning: Could not analyze commit {commit.hexsha}: {e}")
        
        return commit_stats
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get basic information about the repository.
        
        Returns:
            Dictionary with repository information
        """
        return {
            'path': self.repo_path,
            'active_branch': self.repo.active_branch.name,
            'remote_urls': [remote.url for remote in self.repo.remotes],
            'total_commits': len(list(self.repo.iter_commits())),
            'last_commit': {
                'id': self.repo.head.commit.hexsha,
                'message': self.repo.head.commit.message.strip(),
                'author': self.repo.head.commit.author.name,
                'date': datetime.fromtimestamp(self.repo.head.commit.committed_date)
            }
        }