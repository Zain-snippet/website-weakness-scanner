from typing import List
from bs4 import Tag
from models import Finding


CSRF_KEYWORDS = ("csrf", "token", "auth", "nonce")


def analyze_forms(forms: List[Tag]) -> List[Finding]:
    """
    Analyze HTML forms for basic security hygiene.
    Returns a list of Finding objects.
    """

    findings: List[Finding] = []

    if not forms:
        findings.append(
            Finding(
                title="Forms",
                status="absent",
                severity="Low",
                description=(
                    "No HTML forms were detected in the page source. "
                    "This may be due to JavaScript-rendered forms."
                ),
                remediation=(
                    "If the application uses forms, ensure they are protected "
                    "against CSRF attacks."
                ),
            )
        )
        return findings

    for index, form in enumerate(forms, start=1):
        method = form.get("method", "GET").upper()
        inputs = form.find_all("input")

        has_password = False
        has_csrf_token = False

        for input_tag in inputs:
            input_type = (input_tag.get("type") or "").lower()
            input_name = (input_tag.get("name") or "").lower()

            if input_type == "password":
                has_password = True

            if input_type == "hidden":
                for keyword in CSRF_KEYWORDS:
                    if keyword in input_name:
                        has_csrf_token = True
                        break

        # 1. Method check
        findings.append(
            Finding(
                title=f"Form {index} - HTTP Method",
                status="POST" if method == "POST" else "GET",
                severity="Medium" if method != "POST" else "Low",
                description=(
                    "GET forms expose submitted data in URLs, logs, and browser history."
                ),
                remediation=(
                    "Use POST for forms that submit sensitive data."
                ),
            )
        )

        # 2. Password field safety
        if has_password:
            findings.append(
                Finding(
                    title=f"Form {index} - Password Field",
                    status="present",
                    severity="Low",
                    description=(
                        "The form contains a password input field."
                    ),
                    remediation=(
                        "Ensure the form is protected with HTTPS and CSRF tokens."
                    ),
                )
            )

        # 3. CSRF token presence
        findings.append(
            Finding(
                title=f"Form {index} - CSRF Protection",
                status="present" if has_csrf_token else "missing",
                severity="Medium",
                description=(
                    "CSRF tokens help prevent unauthorized cross-site requests."
                ),
                remediation=(
                    "Include a unique, unpredictable CSRF token in the form."
                ),
            )
        )

    return findings