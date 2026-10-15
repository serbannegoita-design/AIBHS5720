import pandas as pd

df = pd.read_csv("nhanes_health.csv")
f = df[(df["sex"] == "Female") & (df["age"].between(00, 999))]
f["bmi"].corr(f["waist_cm"]), len(f)
print(f["age"].corr(f["systolic_bp"]), len(f))