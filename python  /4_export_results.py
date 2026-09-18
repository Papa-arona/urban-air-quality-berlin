import pandas as pd

import config


print("Exporting results...")

validation = pd.read_csv(
    config.VALIDATION
)

validation.to_csv(
    config.PROCESSED / "final_results.csv",
    index=False
)

print("\nFigures:")

for file in sorted(
    config.FIGURES.glob("*.png")
):
    print(file.name)

print("\nFinal results saved to:")
print(config.PROCESSED / "final_results.csv")

print("\nExport complete.")
