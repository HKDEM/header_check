"""
Run pylint on a target Python file or folder and convert the results to SARIF v2.1.0.

This script is fully Pylint-compliant and type-annotated.
This script is fully Pylint-compliant, type-annotated, and generates SARIF even if Pylint
finds warnings or errors.
"""

import json
@@ -29,7 +30,7 @@ def run_pylint(target: str) -> List[Dict[str, Any]]:
        ["pylint", "--output-format=json", target],
        capture_output=True,
        text=True,
        check=True,
        check=False,  # allow non-zero exit codes
    )
