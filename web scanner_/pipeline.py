from typing import List
from models import Finding
from input_handler import validate_url, normalize_url, is_single_domain
from http_client import send_request
from html_parser import parse_html, extract_forms
from header_analyzer import analyze_security_headers
from cookie_analyzer import analyze_cookies
from form_analyzer import analyze_forms
from reporter import generate_text_report


def run_scan(url: str) -> str:
    """
    Orchestrates the full scan pipeline and returns a human-readable report.
    Ensures HTTPS flag reflects the final URL after redirects.
    """

    # ==============================
    # 1. INPUT VALIDATION
    # ==============================
    if not validate_url(url):
        return f"[ERROR] Invalid URL provided: {url}"

    normalized_url = normalize_url(url)

    # Single-domain check is informational, not fatal
    if not is_single_domain(normalized_url):
        print(f"[INFO] Target appears to be a multi-level domain: {normalized_url}")

    # ==============================
    # 2. HTTP REQUEST
    # ==============================
    try:
        response = send_request(normalized_url)
    except Exception as e:
        return f"[ERROR] Request failed due to unexpected error: {str(e)}"

    if response is None:
        return f"[ERROR] Unable to fetch response from {normalized_url}"

    # ==============================
    # 2a. ENSURE HTTPS FLAG MATCHES FINAL URL
    # ==============================
    response.is_https = response.final_url.startswith("https://")
    canonical_url = response.final_url  # use final URL for all analysis

    # ==============================
    # 3. ANALYSIS PHASE (RESILIENT)
    # ==============================
    all_findings: List[Finding] = []

    # ---- Header Analysis (always runs)
    try:
        header_findings = analyze_security_headers(
            response.headers,
            response.is_https
        )
        all_findings.extend(header_findings)
    except Exception as e:
        all_findings.append(
            Finding(
                title="Header Analysis",
                status="error",
                severity="Low",
                description=f"Header analysis failed: {str(e)}",
                remediation="Inspect response headers manually."
            )
        )

    # ---- Cookie Analysis (always runs)
    try:
        cookie_findings = analyze_cookies(
            response.cookies,
            response.is_https
        )
        all_findings.extend(cookie_findings)
    except Exception as e:
        all_findings.append(
            Finding(
                title="Cookie Analysis",
                status="error",
                severity="Low",
                description=f"Cookie analysis failed: {str(e)}",
                remediation="Inspect cookies manually."
            )
        )

    # ---- HTML Parsing + Form Analysis (conditional)
    try:
        if response.body:
            dom = parse_html(response.body)
            forms = extract_forms(dom)
            form_findings = analyze_forms(forms)
            all_findings.extend(form_findings)
        else:
            all_findings.append(
                Finding(
                    title="HTML Content",
                    status="missing",
                    severity="Low",
                    description="No HTML body was returned by the server.",
                    remediation="Ensure the endpoint serves HTML content."
                )
            )
    except Exception as e:
        all_findings.append(
            Finding(
                title="Form Analysis",
                status="error",
                severity="Low",
                description=f"Form analysis could not be completed: {str(e)}",
                remediation="Manually inspect forms if applicable."
            )
        )

    # ==============================
    # 4. REPORT GENERATION
    # ==============================
    report = generate_text_report(all_findings)

    # Optional contextual footer (non-intrusive)
    report += (
        f"\n\nScanned URL      : {normalized_url}"
        f"\nFinal Destination: {canonical_url}"
    )

    return report