import re
import urllib.parse

SQLI_REGEX = re.compile(r"(?i)(\b(?:or|and)\b\s+\d+=\d+|[\'\";`]\s*(?:or|and|union|select|insert|delete|update|drop|exec|--)|/\*.*?\*/)")
XSS_REGEX = re.compile(r"(?i)(<script.*?>.*?</script>|javascript:|on\w+\s*=|document\.(?:cookie|location|write)|eval\s*\(|&#\d+;|&#x[0-9a-f]+)")
PathTraversal_REGEX = re.compile(r"(\.\./|\.\.\\|%2e%2e%2f|%252e%252e%252f|%2e%2e%5c|%252e%252e%5c)")
RCE_REGEX = re.compile(r"(?i)(;|\|\||&&|\$\(|\b(?:exec|system|eval|popen|passthru|shell_exec|proc_open|pcntl_exec|wget|curl|nc|bash|sh|python|perl|ruby|php)\b)")
async def sqli_detection(url: str):
    return SQLI_REGEX.search(url) is not None

async def xss_detection(url: str):
    return XSS_REGEX.search(url) is not None

async def path_traversal_detection(url: str):
    return PathTraversal_REGEX.search(url) is not None

async def rce_detection(url: str):
    return RCE_REGEX.search(url) is not None
