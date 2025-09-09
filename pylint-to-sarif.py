#!/usr/bin/env python3
import json
import subprocess
import sys
import uuid
from pathlib import Path

def run_pylint(target):
    """Run pylint in JSON mode and return parsed output."""
    result = subprocess.run(
        ["pylint", "--output-format=json", target],
        capture_output=True,
        text=True
    )
    if result.returncode not in (0, 32):  
        # 32 = usage error in pylint, others may indicate lint issues
        print("Error running pylint:", result.stderr, file=sys.stderr)
    try:
        return json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return []

def convert_to_sarif(pylint_results):
    """Convert pylint JSON results to SARIF v2.1.0."""
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "pylint",
                        "informationUri": "https://pylint.pycqa.org/",
                        "rules": []
                    }
                },
                "results": []
            }
        ]
    }

    rules_seen = {}
    results = []

    for issue in pylint_results:
        rule_id = issue.get("symbol", issue.get("message-id"))
        message = issue.get("message", "")
        path = issue.get("path", "")
        line = issue.get("line", 1)

        # Register rule if not already added
        if rule_id not in rules_seen:
            rules_seen[rule_id] = {
                "id": rule_id,
                "shortDescription": {"text": issue.get("message", rule_id)},
                "helpUri": "https://pylint.pycqa.org/en/latest/technical_reference/features.html",
                "properties": {"category": issue.get("type", "convention")}
            }

        results.append({
            "ruleId": rule_id,
            "message": {"text": message},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": path},
                        "region": {"startLine": line}
                    }
                }
            ]
        })

    sarif["runs"][0]["tool"]["driver"]["rules"] = list(rules_seen.values())
    sarif["runs"][0]["results"] = results

    return sarif

def main():
    if len(sys.argv) < 3:
        print("Usage: python pylint-to-sarif.py <target> <output.sarif>")
        sys.exit(1)

    target = sys.argv[1]
    output_file = Path(sys.argv[2])

    pylint_results = run_pylint(target)
    sarif = convert_to_sarif(pylint_results)

    output_file.write_text(json.dumps(sarif, indent=2))
    print(f"SARIF report written to {output_file}")

if __name__ == "__main__":
    main()
