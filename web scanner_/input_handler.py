from urllib.parse import urlparse, urlunparse
import re

def validate_url(url: str) -> bool:
    """
    Validate the given URL.
    Returns True if valid (http/https and valid hostname), False otherwise.
    """
    try:
        # Ensure scheme temporarily for parsing if missing
        temp_url = url if url.startswith(("http://", "https://")) else "http://" + url
        parsed = urlparse(temp_url)
        host = parsed.netloc
        
        # 1. Hostname must exist and contain at least one dot
        # 2. Cannot start or end with a dot (e.g., ".com" or "google.")
        if not host or "." not in host or host.startswith(".") or host.endswith("."):
            return False
        
        # 3. Ensure hostname contains only valid characters (alphanumeric, dots, hyphens)
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            return False

        # 4. Scheme must be http or https if explicitly provided
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            return False

        return True
    except Exception:
        return False


def normalize_url(url: str) -> str:
    """
    Normalize URL by ensuring it has a scheme (defaults to http) and preserves path.
    Removes query parameters and fragments.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    # Rebuild URL: (scheme, netloc, path, params, query, fragment)
    normalized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
    )
    return normalized


def is_single_domain(url: str) -> bool:
    """
    Check if the URL is a single domain or base regional domain (2-3 parts).
    Returns True if considered single domain, False otherwise.
    """
    # Ensure scheme for correct parsing of the hostname
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
        
    parsed = urlparse(url)
    host = parsed.netloc

    if not host or "." not in host:
        return False

    # Split host by dots: ['blog', 'google', 'com'] or ['google', 'co', 'uk']
    parts = host.split(".")
    
    # Accept 2 parts (example.com) or 3 parts (google.co.uk / blog.example.com)
    return 2 <= len(parts) <= 3
