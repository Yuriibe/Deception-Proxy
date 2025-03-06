import re
from urllib.parse import urlparse, parse_qs, unquote
import os


class FakeDataService:

    def __init__(self):
        self.pathRegex = re.compile(r"(?i)(?:file=|path=|doc=|/)([\w\-.\/\\]+)")

    def extract_requested_file(self, url: str):
        # Parse URL & query parameters
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Check if the filename is directly in the URL path
        match = self.pathRegex.search(parsed_url.path)
        if match:
            raw_path = unquote(match.group(1))  # Decode URL encoding

            return self.sanitize_path(raw_path)  # Sanitize output

        # Check query parameters for file-like patterns
        for param in ["file", "path", "doc"]:
            if param in query_params:
                raw_path = unquote(query_params[param][0])

                return self.sanitize_path(raw_path)

        return None  # No file detected

    def sanitize_path(self, file_path: str):

        # Strip leading `/../` or `../` to prevent escaping root
        while file_path.startswith("../") or file_path.startswith("/../"):
            file_path = file_path[3:]

        # Ensure output starts with `/`
        return f"/{file_path.lstrip('/')}"

    def getFakeData(self, attack_type: str):
        return None

    def getMatchingPathTraversalFile(self, requestedFile: str):
        if not requestedFile:
            return "Invalid file request"
        filePath = 'fakeResponses/pathTraversal/' + requestedFile
        if os.path.isfile(filePath):
            with open(filePath) as f:
                return f.read()

    def getMatchingPathTraversalPath(self, url: str):
        return self.extract_requested_file(url)
