from typing import List, Dict
from models import Finding


def analyze_security_headers(headers: Dict[str, str], is_https: bool) -> List[Finding]:
    """
    Analyze HTTP response headers for presence of basic security headers.
    Returns a list of Finding objects.
    """

    findings: List[Finding] = []

    # Normalize headers for case-insensitive lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    def header_present(header_name: str) -> bool:
        return header_name.lower() in normalized_headers

    # 1. Content-Security-Policy
    findings.append(
        Finding(
            title="Content-Security-Policy",
            status="present" if header_present("Content-Security-Policy") else "missing",
            severity="Medium",
            description=(
                "Controls which resources the browser is allowed to load."
            ),
            remediation=(
                "Define a Content-Security-Policy header to restrict allowed resources."
            ),
        )
    )

    # 2. X-Frame-Options
    findings.append(
        Finding(
            title="X-Frame-Options",
            status="present" if header_present("X-Frame-Options") else "missing",
            severity="Low",
            description=(
                "Prevents the page from being embedded in frames or iframes."
            ),
            remediation=(
                "Add the X-Frame-Options header to control iframe embedding."
            ),
        )
    )

    # 3. X-Content-Type-Options
    findings.append(
        Finding(
            title="X-Content-Type-Options",
            status="present" if header_present("X-Content-Type-Options") else "missing",
            severity="Low",
            description=(
                "Prevents browsers from MIME-sniffing a response away from the declared content type."
            ),
            remediation=(
                "Set X-Content-Type-Options to 'nosniff'."
            ),
        )
    )

    # 4. Referrer-Policy
    findings.append(
        Finding(
            title="Referrer-Policy",
            status="present" if header_present("Referrer-Policy") else "missing",
            severity="Low",
            description=(
                "Controls how much referrer information is included with requests."
            ),
            remediation=(
                "Define a Referrer-Policy to limit information leakage."
            ),
        )
    )

    # 5. Strict-Transport-Security (HTTPS only)
    if is_https:
        findings.append(
            Finding(
                title="Strict-Transport-Security",
                status="present" if header_present("Strict-Transport-Security") else "missing",
                severity="Medium",
                description=(
                    "Forces browsers to interact with the site only over HTTPS."
                ),
                remediation=(
                    "Enable Strict-Transport-Security to enforce HTTPS connections."
                ),
            )
        )

    return findings