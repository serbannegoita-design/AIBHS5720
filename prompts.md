I want to build a Streamlit app, app.py, that explores correlations between health measures in nhanes_health.csv. Read the CSV first. Every numeric column except…

<!-- The starter text above was already present and is preserved. Conversation inputs follow in chronological order. -->

## Original request

Do not write any code yet. Point to nhanes_health.csv. The goal, is to select five features, any besides sex. All are numeric besides sex. The missing values can be imputed based on age. Use a heatmap warm color scale. Show n next to evvery r.  Use Python, Streamlit, pandas and seaborn (or plotly), one file called `app.py`, no other packages without asking. This is request **for a plan, not code:** the build order, how the filters feed every view, the command to run the app. aks about anything in my request that is unclear

## Clarification selections

1. Five features: **Selectable five (Recommended)** — Require exactly five numeric features; default to BMI, waist, systolic BP, HbA1c, and total cholesterol.
2. Filters and views: **Age + sex filters (Recommended)** — Both filters feed a sample-size summary, correlation heatmap, and filtered data table; sex is excluded from feature selection.
3. Imputation: **Age-band median (Recommended)** — Use medians within 10-year age bands from the full CSV, with the full-column median as fallback.
4. r and n: **Pairs used in r (Recommended)** — Count complete pairs after imputation; show the number of imputed cells separately for transparency.

## Documentation and implementation request

Add all of my inputs into prompts.md. Add the plan inti plan.md. THen yes, implement this plan.

## Final implementation request (verbatim)

PLEASE IMPLEMENT THIS PLAN:
# NHANES correlation explorer and project records

## Deliverables and build order

1. Create `prompts.md` containing your original request verbatim, your clarification selections, and your latest request verbatim, in chronological order.
2. Create `plan.md` containing this implementation plan.
3. Create `app.py` using Python, Streamlit, pandas, and seaborn. Use no additional package imports without asking.
4. Validate the app and report the results.

## Data preparation

- Load `nhanes_health.csv` relative to `app.py`; validate required columns and numeric values.
- Impute missing numeric measurements using full-dataset medians within decade age bands, falling back to the full-column median.
- Track filled cells. Leave missing ages unchanged, exclude those rows from age-filtered results, and report their count.
- Preserve the source CSV. Its current 4,433 records contain no missing values.

## Controls and shared data flow

- Require exactly five numeric features, excluding `sex`.
- Default to `bmi`, `waist_cm`, `systolic_bp`, `hba1c`, and `total_chol`.
- Provide an inclusive age-range slider and sex multiselect, initially including all records.
- Prepare imputation before filtering, then apply both filters to produce one shared dataset for every view.
- Show the filtered row count, imputed-cell count for selected features, correlation heatmap, and filtered table. Include age and sex as table context without duplicating selected columns.

## Correlation display and edge cases

- Calculate Pearson correlations for the selected features.
- Use seaborn’s warm `YlOrRd` heatmap scale, fixed from −1 to +1, with a labeled color bar.
- Annotate every cell with `r` and the complete-pair `n` used after imputation.
- Show undefined correlations as `r=N/A` with the actual `n`.
- Withhold analytical views until exactly five features are selected.
- Provide clear messages for empty filter results, invalid data, and missing files.

## Validation and launch

Check initial counts, feature-selection enforcement, synchronized filtering across every view, correlation pair counts, constant columns, and empty results. Validate imputation with temporary in-memory missing values without altering the CSV.

Run from `C:\Users\serba\Downloads\AIBHS 5720`:

```powershell
python -m streamlit run app.py
```

Assume dependencies are installed. Use Streamlit’s native chart display for the seaborn figure. The only application source file is `app.py`; `prompts.md` and `plan.md` are project documentation.

## Continuation request (verbatim)

Continue as above. 

## Age versus systolic_bp request (verbatim)

I cannot see the age versus systolic_bp. Can you make sure the app is able to display this.

## Verification request (verbatim)

Please fill out the table in part 4.verify and copy it into verification.md per instructions.

## Requirements and CSV path request (verbatim)

create  a `requirements.txt` listing every package `app.py` imports (e.g. `streamlit`, `pandas`, `seaborn`, `scipy`, and `plotly` if used). Check that `app.py` loads the CSV with the relative path `nhanes_health.csv`.

## Migration request (verbatim)

C:\Users\serba\OneDrive\Documents\GitHub\AIBHS5720

migrate the code and all the markdown files we created into the folder above.

