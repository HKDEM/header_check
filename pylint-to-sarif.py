#!/usr/bin/env python3
"""
Run pylint on a target file or folder and convert results to SARIF v2.1.0.

This script is fully Pylint-compliant and type-annotated.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any

# Constants
PYLINT_INFO_URL = "https://pylint.pycqa.org/"
SARIF_SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"


def run_pylint(target: str) -> List[Dict[str, Any]]:
    """Run pylint in JSON mode and return parsed output.

    Args:
        target: Path to a Python file or folder.

    Returns:
        List of Pylint issue dictionaries.
    """
    result = subprocess.run(
        ["pylint", "--output-format=json", target],
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 32):
        print("Error running pylint:", result.stderr, file=sys.stderr)

    try:
        return json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return []


def convert_to_sarif(pylint_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert Pylint JSON results to SARIF v2.1.0.

    Args:
        pylint_results: List of Pylint issue dictionaries.

    Returns:
        SARIF-compliant dictionary.
    """
    sarif: Dict[str, Any] = {
        "version": "2.1.0",
        "$schema": SARIF_SCHEMA,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "pylint",
                        "informationUri": PYLINT_INFO_URL,
                        "rules": [],
                    }
                },
                "results": [],
            }
        ],
    }

    rules_seen: Dict[str, Dict[str, Any]] = {}
    results: List[Dict[str, Any]] = []

    for issue in pylint_results:
        rule_id = issue.get("symbol", issue.get("message-id", "unknown"))
        message = issue.get("message", "")
        path = issue.get("path", "")
        line = issue.get("line", 1)

        if rule_id not in rules_seen:
            rules_seen[rule_id] = {
                "id": rule_id,
                "shortDescription": {"text": message or rule_id},
                "helpUri": f"{PYLINT_INFO_URL}en/latest/technical_reference/features.html",
                "properties": {"category": issue.get("type", "convention")},
            }

        results.append(
            {
                "ruleId": rule_id,
                "message": {"text": message},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": path},
                            "region": {"startLine": line},
                        }
                    }
                ],
            }
        )

    sarif["runs"][0]["tool"]["driver"]["rules"] = list(rules_seen.values())
    sarif["runs"][0]["results"] = results

    return sarif


def main() -> None:
    """Main entry point for pylint-to-sarif."""
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
