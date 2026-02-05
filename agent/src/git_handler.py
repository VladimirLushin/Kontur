"""
Module for handling Git repository operations
"""
import os
import tempfile
import shutil
from typing import Optional
import git


class GitHandler:
    """Handles cloning and managing Git repositories"""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.username = username
        self.password = password
    
    def clone_repository(self, repo_url: str, local_path: Optional[str] = None) -> str:
        """
        Clone a Git repository to a local directory
        
        Args:
            repo_url: URL of the Git repository to clone
            local_path: Local path to clone to (optional, creates temporary directory if not provided)
            
        Returns:
            Path to the cloned repository
        """
        if local_path is None:
            temp_dir = tempfile.mkdtemp()
            local_path = temp_dir
        
        # Add credentials to URL if provided
        if self.username and self.password:
            # Parse the URL and add credentials
            if repo_url.startswith("https://"):
                repo_url_with_auth = repo_url.replace(
                    "https://", f"https://{self.username}:{self.password}@"
                )
            elif repo_url.startswith("http://"):
                repo_url_with_auth = repo_url.replace(
                    "http://", f"http://{self.username}:{self.password}@"
                )
            else:
                repo_url_with_auth = repo_url
        else:
            repo_url_with_auth = repo_url
        
        try:
            git.Repo.clone_from(repo_url_with_auth, local_path)
            return local_path
        except git.exc.GitCommandError as e:
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def cleanup(self, repo_path: str):
        """Clean up the cloned repository directory"""
        if os.path.exists(repo_path) and tempfile.tempdir in repo_path:
            shutil.rmtree(repo_path)