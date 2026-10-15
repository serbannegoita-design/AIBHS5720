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

## Implementation and validation notes

- Follow-up: include `age` in the default five features in place of `total_chol`. Add an “Include age and systolic_bp” preset button for existing selections and a dedicated age-versus-systolic_bp scatterplot with age-specific means and Pearson r beside complete-pair n. Both views use the shared filtered, imputed data. The dedicated comparison remains visible with any valid selection of five heatmap features.

- Created a project-local `.venv` with the approved Streamlit, pandas, and seaborn packages and their required dependencies. No additional third-party packages are imported by `app.py`.
- On this machine, `python` is not on PATH. Launch directly from the project folder with:

  ```powershell
  .\.venv\Scripts\python.exe -m streamlit run app.py
  ```

- Streamlit interaction checks passed for initial counts, both filters, alternate five-feature selections, empty results, and invalid selection counts. Female participants aged 40–59 produce 750 filtered records.
- Numerical checks passed for Pearson coefficients, complete-pair counts, decade-band imputation, overall-median fallback, missing-age exclusions, unfillable values, and undefined correlations. The heatmap includes n even in undefined cells and fixes its scale to −1 through +1.
- Invalid-file and invalid-data checks passed. A before/after SHA-256 comparison confirmed that `nhanes_health.csv` was unchanged.
