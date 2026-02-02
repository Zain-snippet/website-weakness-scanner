from typing import List
from models import Finding


SEVERITY_ORDER = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}


def generate_text_report(findings: List[Finding]) -> str:
    """
    Generate a clean, human-readable CLI report from findings.
    """

    if not findings:
        return "No findings to report."

    # Sort findings by severity (High → Low)
    sorted_findings = sorted(
        findings,
        key=lambda f: SEVERITY_ORDER.get(f.severity, 0),
        reverse=True
    )

    lines = []
    lines.append("=" * 60)
    lines.append("SMART WEB APP WEAKNESS FINDER REPORT")
    lines.append("=" * 60)
    lines.append(f"Total Findings: {len(sorted_findings)}")
    lines.append("")

    for finding in sorted_findings:
        lines.append(f"[{finding.severity.upper()}] {finding.title}")
        lines.append(f"Status      : {finding.status}")
        lines.append(f"Why it matters:")
        lines.append(f"  {finding.description}")
        lines.append(f"Remediation : {finding.remediation}")
        lines.append("-" * 60)

    return "\n".join(lines)