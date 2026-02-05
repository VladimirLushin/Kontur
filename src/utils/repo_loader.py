"""Repository loader utility for cloning and accessing remote repositories."""
import os
import tempfile
import git
from typing import Optional
from urllib.parse import urlparse


class RepoLoader:
    """Load repositories from various sources."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.username = username
        self.password = password
    
    def clone_repo(self, repo_url: str) -> str:
        """Clone a repository to a temporary directory and return the path."""
        parsed_url = urlparse(repo_url)
        
        # Add credentials to URL if provided
        if self.username and self.password:
            scheme, netloc = parsed_url.scheme, parsed_url.netloc
            new_netloc = f"{self.username}:{self.password}@{netloc}"
            repo_url_with_auth = repo_url.replace(f"{scheme}://{netloc}", f"{scheme}://{new_netloc}")
        else:
            repo_url_with_auth = repo_url
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Clone the repository
            git.Repo.clone_from(repo_url_with_auth, temp_dir)
            return temp_dir
        except Exception as e:
            raise Exception(f"Failed to clone repository: {e}")
    
    def get_java_files(self, repo_path: str) -> list:
        """Get all Java files in the repository."""
        java_files = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))
        return java_files
    
    def get_repo_info(self, repo_path: str) -> dict:
        """Get information about the repository."""
        try:
            repo = git.Repo(repo_path)
            
            # Get repository information
            info = {
                'path': repo_path,
                'is_dirty': repo.is_dirty(),
                'active_branch': repo.active_branch.name if repo.active_branch else None,
                'remotes': [remote.name for remote in repo.remotes],
                'commits_count': len(list(repo.iter_commits())),
                'last_commit': {
                    'hexsha': repo.head.commit.hexsha,
                    'message': repo.head.commit.message.strip(),
                    'author': repo.head.commit.author.name,
                    'date': repo.head.commit.committed_date,
                } if repo.head.commit else None
            }
            
            return info
        except Exception as e:
            raise Exception(f"Failed to get repository info: {e}")