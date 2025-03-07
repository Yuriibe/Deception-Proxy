import re
from urllib.parse import urlparse, parse_qs, unquote
import os


class FakeDataService:

    def __init__(self):
        # Regex to match common file/path parameters or direct paths
        self.pathRegex = re.compile(r"(?i)(?:file=|path=|doc=|/)([\w\-.\/\\]+)")

    def extract_requested_file(self, url: str):
        """Extracts the last two parts of a file path for path traversal detection."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Try extracting file from query parameters first
        for param in ["file", "path", "doc"]:  # Common file params
            if param in query_params:
                raw_path = unquote(query_params[param][0])  # Decode any URL encoding
                print(f"🔍 Extracted from query parameter '{param}': {raw_path}")
                return self.sanitize_path(raw_path)

        # Extract last two parts of the path
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 2:
            extracted_path = "/" + "/".join(path_parts[-2:])  # Keep last 2 parts (e.g., /etc/passwd)
        elif path_parts:
            extracted_path = "/" + path_parts[-1]  # If only one part exists, return it
        else:
            extracted_path = None

        if extracted_path:
            print(f"🔍 Extracted from path: {extracted_path}")
            return self.sanitize_path(extracted_path)

        print("⚠️ No file detected in URL")
        return None  # No file detected

    def sanitize_path(self, file_path: str):
        """Sanitize path for consistent detection format (not prevention)."""
        sanitized = os.path.normpath(unquote(file_path)).lstrip(os.sep)  # Normalize path
        return "/" + "/".join(sanitized.split(os.sep)[-2:])  # Keep last 2 parts

    def getFakeData(self, attack_type: str):
        """Returns predefined fake responses based on the attack type."""
        return None  # Placeholder, can return fake data for testing

    def getMatchingPathTraversalFile(self, requestedFile: str):
        """Simulates responding with a fake file based on detected traversal."""
        if not requestedFile:
            return "Invalid file request"

        # Simulate fake responses directory
        filePath = os.path.join('fakeResponses/pathTraversal', requestedFile.lstrip("/"))

        if os.path.isfile(filePath):
            with open(filePath, "r", encoding="utf-8") as f:
                return f.read()
        return "File not found"

    def getMatchingPathTraversalPath(self, url: str):
        return self.extract_requested_file(url)
