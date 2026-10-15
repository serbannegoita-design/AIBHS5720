# Part 4: Verification

Verified on October 15, 2026 using Pearson correlation and the full age range (20–80). Sex filters were set as specified in each row. Age 80 represents 80 or older.

| # | Check | App shows | pandas gives | Match? |
|---|---|---|---|---|
| 1 | r for `age` vs `systolic_bp`, all participants | r = 0.463, n = 4,433 | r = 0.462695060816, n = 4,433 | Yes, at displayed precision |
| 2 | r for `bmi` vs `waist_cm`, all participants | r = 0.90, n = 4,433 | r = 0.902588775861, n = 4,433 | Yes, at displayed precision |
| 3 | r for `waist_cm` vs `hdl_chol`, all participants | r = −0.33, n = 4,433 | r = −0.334986876312, n = 4,433 | Yes, at displayed precision |
| 4 | r and n for `age` vs `systolic_bp`, **Female only** | r = 0.555, n = 2,263 | r = 0.555342554061, n = 2,263 | Yes, at displayed precision |
| 5 | r and n for `age` vs `systolic_bp`, **Male only** | r = 0.351, n = 2,170 | r = 0.350697864687, n = 2,170 | Yes, at displayed precision |
| 6 | With the filter set to Female, does the heatmap's `age`/`systolic_bp` square match row 4? | Heatmap: r = 0.56, n = 2,263; row 4 scatterplot: r = 0.555, n = 2,263 | r = 0.555342554061, n = 2,263 | Yes; the heatmap uses two decimals and the scatterplot uses three |

## How these results were obtained

The agent read the app's displayed text and rendered heatmap annotations through Streamlit's test runner. The five selected heatmap features were `age`, `bmi`, `waist_cm`, `systolic_bp`, and `hdl_chol`.

A separate Python process loaded `nhanes_health.csv` directly with pandas, without importing the app or using its preparation, filtering, or correlation functions. Each pandas n counts complete pairs. The CSV has no missing cells, so imputation does not change these results. The rendered heatmap color limits were also checked as −1 and +1.

These are agent-run checks. The exercise explicitly asks the student to perform the pandas verification independently; this document does not claim that the student has completed that step.

## Pandas code for independent reproduction

```python
import pandas as pd

df = pd.read_csv("nhanes_health.csv")
checks = [
    (1, df, "age", "systolic_bp"),
    (2, df, "bmi", "waist_cm"),
    (3, df, "waist_cm", "hdl_chol"),
    (4, df.loc[df["sex"].eq("Female")], "age", "systolic_bp"),
    (5, df.loc[df["sex"].eq("Male")], "age", "systolic_bp"),
    (6, df.loc[df["sex"].eq("Female")], "age", "systolic_bp"),
]
for number, subset, x, y in checks:
    pairs = subset[[x, y]].dropna()
    print(number, pairs[x].corr(pairs[y], method="pearson"), len(pairs))
```
