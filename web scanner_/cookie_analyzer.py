from typing import List
from models import Finding, CookieSnapshot


def analyze_cookies(cookies: List[CookieSnapshot], is_https: bool) -> List[Finding]:
    """
    Analyze cookies for basic security attributes.
    Returns a list of Finding objects.
    """

    findings: List[Finding] = []

    if not cookies:
        findings.append(
            Finding(
                title="Cookies",
                status="absent",
                severity="Low",
                description="No cookies were set by the server.",
                remediation="No action required if the application does not rely on cookies.",
            )
        )
        return findings

    for cookie in cookies:
        cookie_name = cookie.name

        # 1. Secure flag
        if is_https:
            findings.append(
                Finding(
                    title=f"Cookie '{cookie_name}' - Secure Flag",
                    status="present" if cookie.secure else "missing",
                    severity="Medium",
                    description="Ensures the cookie is only sent over HTTPS connections.",
                    remediation="Set the Secure flag to prevent the cookie from being sent over HTTP.",
                )
            )

        # 2. HttpOnly flag
        findings.append(
            Finding(
                title=f"Cookie '{cookie_name}' - HttpOnly Flag",
                status="present" if cookie.httponly else "missing",
                severity="Medium",
                description="Prevents JavaScript from accessing the cookie.",
                remediation="Enable the HttpOnly flag to protect against client-side script access.",
            )
        )

        # 3. SameSite attribute
        findings.append(
            Finding(
                title=f"Cookie '{cookie_name}' - SameSite Attribute",
                status="present" if cookie.samesite else "missing",
                severity="Low",
                description="Controls whether cookies are sent with cross-site requests.",
                remediation="Set SameSite to 'Lax' or 'Strict' to reduce cross-site request risks.",
            )
        )

    return findings