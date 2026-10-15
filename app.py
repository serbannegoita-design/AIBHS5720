"""Run with: python -m streamlit run app.py."""

from pathlib import Path
from threading import RLock

import pandas as pd
import seaborn as sns
import streamlit as st


NUMERIC_COLUMNS = [
    "age", "bmi", "waist_cm", "systolic_bp", "diastolic_bp", "hba1c",
    "total_chol", "hdl_chol", "sleep_hours", "sedentary_minutes",
]
DEFAULT_FEATURES = ["age", "bmi", "waist_cm", "systolic_bp", "hba1c"]
DATA_PATH = Path(__file__).resolve().with_name("nhanes_health.csv")


def load_data(path=DATA_PATH):
    """Validate the CSV without treating invalid measurements as missing."""
    data = pd.read_csv(path)
    missing = set(NUMERIC_COLUMNS + ["sex"]) - set(data.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    if data.empty:
        raise ValueError("The CSV contains no participant rows.")
    for column in NUMERIC_COLUMNS:
        try:
            data[column] = pd.to_numeric(data[column], errors="raise")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Column '{column}' contains nonnumeric values.") from exc
        if data[column].isin([float("inf"), float("-inf")]).any():
            raise ValueError(f"Column '{column}' contains infinite values.")
    if data["age"].notna().sum() == 0:
        raise ValueError("No observed ages are available for filtering.")
    invalid_sex = data["sex"].isna() | ~data["sex"].isin(["Female", "Male"])
    if invalid_sex.any():
        raise ValueError("Column 'sex' must contain Female or Male for every row.")
    return data


def prepare_data(data):
    """Learn medians once from all rows; never impute age itself."""
    prepared = data.copy()
    bands = data["age"] // 10
    for column in NUMERIC_COLUMNS:
        if column == "age":
            continue
        band_medians = data[column].groupby(bands).transform("median")
        prepared[column] = data[column].fillna(band_medians).fillna(data[column].median())
    filled = data[NUMERIC_COLUMNS].isna() & prepared[NUMERIC_COLUMNS].notna()
    return prepared, filled


def filter_data(data, ages, sexes):
    return data.loc[data["age"].between(*ages) & data["sex"].isin(sexes)].copy()


def correlation_tables(data, features):
    values = data[features]
    correlations = values.corr(method="pearson", min_periods=2)
    observed = values.notna().astype("int64")
    counts = observed.T.dot(observed)
    return correlations, counts


def heatmap(correlations, counts):
    # Annotate manually so undefined (masked) cells still display their n.
    ax = sns.heatmap(
        correlations, cmap="YlOrRd", vmin=-1, vmax=1, square=True,
        linewidths=0.5, cbar_kws={"label": "Pearson r", "ticks": [-1, -0.5, 0, 0.5, 1]},
    )
    figure = ax.figure
    figure.set_size_inches(11, 8)
    ax.set_facecolor("#eeeeee")
    for row in range(len(correlations)):
        for column in range(len(correlations.columns)):
            r = correlations.iat[row, column]
            label = f"r={r:.2f}" if pd.notna(r) else "r=N/A"
            color = "white" if pd.notna(r) and r > 0.3 else "black"
            ax.text(column + 0.5, row + 0.5,
                    f"{label}\nn={counts.iat[row, column]:,}",
                    ha="center", va="center", color=color, fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    figure.tight_layout()
    return figure


@st.cache_resource
def plotting_lock():
    return RLock()


def main():
    st.set_page_config(page_title="NHANES correlation explorer", layout="wide")
    st.title("NHANES correlation explorer")
    st.write("Explore five numeric measures from nhanes_health.csv. Each row is one participant.")
    st.caption("Age 80 represents 80 or older. Correlations describe this sample; they do not establish causation.")
    try:
        original = load_data()
        prepared, filled = prepare_data(original)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        st.error(f"Unable to load nhanes_health.csv: {exc}")
        st.stop()

    missing_ages = int(original["age"].isna().sum())
    st.caption(
        "Missing measurements use full-dataset medians within 10-year age bands, "
        "then the full-column median. Age is never imputed. "
        f"Rows excluded for missing age: {missing_ages:,}."
    )
    with st.sidebar:
        st.header("Features and filters")
        if "features" not in st.session_state:
            st.session_state["features"] = DEFAULT_FEATURES.copy()
        if st.button("Include age and systolic_bp"):
            st.session_state["features"] = DEFAULT_FEATURES.copy()
        features = st.multiselect("Select exactly five numeric features", NUMERIC_COLUMNS,
                                  key="features")
        minimum = float(prepared["age"].min())
        maximum = float(prepared["age"].max())
        if minimum == maximum:
            ages = (minimum, maximum)
            st.caption(f"All observed ages: {minimum:g}")
        else:
            ages = st.slider("Age range (inclusive)", min_value=minimum,
                             max_value=maximum, value=(minimum, maximum),
                             step=1.0, key="ages")
        sexes = st.multiselect("Sex", ["Female", "Male"],
                              default=["Female", "Male"], key="sexes")

    if len(features) != 5:
        st.info(f"Select exactly five numeric features to view results (currently {len(features)}).")
        st.stop()
    filtered = filter_data(prepared, ages, sexes)
    if filtered.empty:
        st.info("No participants match these filters. Adjust the age range or select a sex.")
        st.stop()

    first, second = st.columns(2)
    first.metric("Filtered participants", f"{len(filtered):,}")
    second.metric("Imputed cells in selected features",
                  f"{int(filled.loc[filtered.index, features].sum().sum()):,}")
    unresolved = int(filtered[features].isna().sum().sum())
    if unresolved:
        st.warning(f"{unresolved:,} selected cells remain missing; pair counts can differ.")

    st.subheader("Age versus systolic_bp")
    pairs = filtered[["age", "systolic_bp"]].dropna()
    pair_r = pairs.corr(method="pearson", min_periods=2).loc["age", "systolic_bp"]
    r_label = f"{pair_r:.3f}" if pd.notna(pair_r) else "N/A"
    st.write(f"Pearson r={r_label} | n={len(pairs):,}")
    if pairs.empty:
        st.info("No complete age and systolic_bp pairs are available for these filters.")
    else:
        with plotting_lock():
            grid = sns.relplot(data=pairs, x="age", y="systolic_bp", kind="scatter",
                               color="#cc4c02", alpha=0.3, s=24, height=4, aspect=2)
            means = pairs.groupby("age", as_index=False)["systolic_bp"].mean()
            sns.lineplot(data=means, x="age", y="systolic_bp", ax=grid.ax,
                         color="#7f0000", linewidth=2, label="Mean at each age")
            grid.set_axis_labels("Age (years; 80 means 80+)", "Systolic blood pressure (mmHg)")
            st.pyplot(grid.figure, clear_figure=True)
        st.caption("Points show participants; the line shows mean systolic_bp at each age. Both filters apply.")

    correlations, counts = correlation_tables(filtered, features)
    st.subheader("Pearson correlation heatmap")
    st.caption("Each n counts complete pairs used after imputation. Gray cells have undefined r. Colors stay fixed from −1 to +1.")
    with plotting_lock():
        figure = heatmap(correlations, counts)
        st.pyplot(figure, clear_figure=True)
    st.caption("A correlation near zero can still hide a nonlinear relationship.")
    st.subheader("Filtered participant data")
    columns = list(dict.fromkeys(["age", "sex"] + features))
    st.dataframe(filtered[columns], hide_index=True)
    st.caption("This table contains the same filtered, imputed records used for the heatmap.")


if __name__ == "__main__":
    main()
