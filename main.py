import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = ROOT / "python"

steps = [  # workflow inspired by the 7-step calibration approach of Aix et al. (2023)
    "1_prepare_data.py",
    "2_analysis.py",
    "3_validation.py",
    "4_export_results.py"
]

for step in steps:
    print(f"\nRunning {step}...")

    result = subprocess.run(
        [sys.executable, str(PYTHON / step)]
    )

    if result.returncode != 0:
        raise SystemExit(f"Stopped at {step}")

print("\nAnalysis complete.")
