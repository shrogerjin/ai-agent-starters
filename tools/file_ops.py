"""File operations tool for AI agent."""
import os
import json
from typing import List, Optional


class FileOpsTool:
    """File system operations for agents."""

    def read(self, path: str) -> str:
        """Read file contents."""
        if not os.path.exists(path):
            return f"File not found: {path}"
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {path}: {e}"

    def write(self, path: str, content: str) -> str:
        """Write content to file."""
        try:
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return f"Written to {path}"
        except Exception as e:
            return f"Error writing {path}: {e}"

    def list_dir(self, path: str = ".") -> List[str]:
        """List directory contents."""
        try:
            return os.listdir(path)
        except Exception as e:
            return [f"Error: {e}"]

    def exists(self, path: str) -> bool:
        """Check if path exists."""
        return os.path.exists(path)

    def json_read(self, path: str) -> dict:
        """Read and parse JSON file."""
        content = self.read(path)
        if content.startswith("Error"):
            return {"error": content}
        try:
            return json.loads(content)
        except:
            return {"error": "Invalid JSON"}
