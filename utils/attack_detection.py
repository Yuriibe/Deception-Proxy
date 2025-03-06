import re
import urllib.parse
import os

SQLI_REGEX = re.compile(
    r"(?i)(\b(?:or|and)\b\s+\d+=\d+|[\'\";`]\s*(?:or|and|union|select|insert|delete|update|drop|exec|--)|/\*.*?\*/)")
XSS_REGEX = re.compile(
    r"(?i)(<script.*?>.*?</script>|javascript:|on\w+\s*=|document\.(?:cookie|location|write)|eval\s*\(|&#\d+;|&#x[0-9a-f]+)")
PathTraversal_REGEX = re.compile(
    r"(?:\.\./|\.\.\\|%2e%2e%2f|%252e%252e%252f|%2e%2e%5c|%252e%252e%5c|"
    r"/etc/(passwd|shadow|group|hosts|hostname|resolv.conf)|"
    r"/proc/self/environ|/var/log|/root|/home/\w+/\.ssh/authorized_keys)"
)

RCE_REGEX = re.compile(
    r"(?i)(;|\|\||&&|\$\(|\b(?:exec|system|eval|popen|passthru|shell_exec|proc_open|pcntl_exec|wget|curl|nc|bash|sh|python|perl|ruby|php)\b)")


async def sqli_detection(url: str):
    return SQLI_REGEX.search(url) is not None


async def xss_detection(url: str):
    return XSS_REGEX.search(url) is not None


async def path_traversal_detection(url: str, base_directory="/var/www/html") -> bool:
    # Extract path component from the URL
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path  # Get only the path component (ignoring scheme, host, etc.)

    # Decode the URL path twice
    decoded_path = urllib.parse.unquote(path)
    double_decoded_path = urllib.parse.unquote(decoded_path)

    # Normalize the path
    sanitized_path = os.path.normpath(double_decoded_path).lstrip(os.sep)
    normalized_path = os.path.normpath(os.path.join(base_directory, sanitized_path))

    real_normalized_path = os.path.realpath(normalized_path)

    print(f"Original URL: {url}")
    print(f"Extracted Path: {path}")
    print(f"Decoded Path: {double_decoded_path}")
    print(f"Sanitized Path: {sanitized_path}")
    print(f"Normalized Path: {normalized_path}")
    print(f"Real Normalized Path: {real_normalized_path}")

    # Check for traversal patterns
    is_traversal_attempt = PathTraversal_REGEX.search(double_decoded_path) is not None

    # Ensure path is within the allowed base directory
    is_outside_base = not real_normalized_path.startswith(os.path.realpath(base_directory))

    return is_traversal_attempt or is_outside_base


async def rce_detection(url: str):
    return RCE_REGEX.search(url) is not None
