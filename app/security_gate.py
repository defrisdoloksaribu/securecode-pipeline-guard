
import json
import sys
from pathlib import Path


def load_findings(report):
    # Support the custom report format.
    if isinstance(report.get("findings"), list):
        return report["findings"]

    # Support Bandit's native JSON report.
    if isinstance(report.get("results"), list):
        findings = []

        for item in report["results"]:
            findings.append({
                "tool": "Bandit",
                "severity": item.get(
                    "issue_severity", "LOW"
                ).upper(),
                "message": item.get(
                    "issue_text", "No details provided"
                ),
            })

        return findings

    raise ValueError("Unsupported security report format")


def evaluate_report(report_path):
    path = Path(report_path)

    if not path.is_file():
        print(f"ERROR: Report not found: {path}")
        return 2

    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            raise ValueError("Report must be a JSON object")

        findings = load_findings(report)

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"ERROR: Cannot read report: {error}")
        return 2

    blocking = [
        item for item in findings
        if isinstance(item, dict)
        and str(item.get("severity", "")).upper()
        in {"HIGH", "CRITICAL"}
    ]

    print(f"Report: {path}")
    print(f"Total findings: {len(findings)}")
    print(f"Blocking findings: {len(blocking)}")

    for item in blocking:
        print(
            f"- [{item['severity']}] "
            f"{item.get('tool', 'unknown')}: "
            f"{item.get('message', 'No details provided')}"
        )

    if blocking:
        print("SECURITY GATE: FAILED")
        return 1

    print("SECURITY GATE: PASSED")
    return 0


if __name__ == "__main__":
    report_file = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "reports/security-report.json"
    )
    raise SystemExit(evaluate_report(report_file))
