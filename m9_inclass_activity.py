# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.24.2",
#     "matplotlib>=3.8,<3.11",
#     "pandas==3.0.5",
#     "seaborn>=0.13,<0.14",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    return mo, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Blood Pressure Screening

    A community health clinic ran a screening day for 200 adults (a simulated dataset, so some patterns are stronger than they would be in real screening data). Each row is one participant, with these columns:
    - the participant's age in years
    - height in centimeters
    - weekly exercise in minutes
    - average hours of sleep per night
    - systolic blood pressure in mmHg, the average of three clinic readings
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Screening Data

    **Instructions:** Load `bp_screening.csv` into a DataFrame and display it.
    """)
    return


@app.cell
def _(pd):
    # Your code here
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Age vs. Blood Pressure: Correlation

    **Instructions:** Calculate the correlation coefficient between age and systolic blood pressure.
    """)
    return


@app.cell
def _(df):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Age vs. Blood Pressure: Scatter Plot

    **Instructions:** Create a scatter plot of age and systolic blood pressure.
    """)
    return


@app.cell
def _(df, sns):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Height vs. Blood Pressure: Scatter Plot

    **Instructions:** Create a scatter plot of height and systolic blood pressure.
    """)
    return


@app.cell
def _(df, sns):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Height vs. Blood Pressure: Correlation

    **Instructions:** Calculate the correlation coefficient between height and systolic blood pressure.
    """)
    return


@app.cell
def _(df):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise vs. Blood Pressure: Scatter Plot

    **Instructions:** Create a scatter plot of weekly exercise and systolic blood pressure.
    """)
    return


@app.cell
def _(df, sns):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise vs. Blood Pressure: Correlation

    **Instructions:** Calculate the correlation coefficient between weekly exercise and systolic blood pressure.
    """)
    return


@app.cell
def _(df):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Sleep vs. Blood Pressure: Correlation

    **Instructions:** Calculate the correlation coefficient between hours of sleep and systolic blood pressure.
    """)
    return


@app.cell
def _(df):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Sleep vs. Blood Pressure: Scatter Plot

    **Instructions:** Create a scatter plot of hours of sleep and systolic blood pressure.
    """)
    return


@app.cell
def _(df, sns):
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Correlation Matrix

    **Instructions:** Select every column except `sleep_hours`, because its pattern is non-linear and a correlation matrix only describes straight line relationships. Calculate a correlation matrix of the rest, store it as `correlations` and display it.
    """)
    return


@app.cell
def _(df):
    # Your code here
    return (correlations,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Correlation Heatmap

    **Instructions:** Create a heatmap of the correlation matrix. Write the coefficient inside each square and make the colors run from -1 to 1.
    """)
    return


@app.cell
def _(correlations, plt, sns):
    # Your code here
    return


if __name__ == "__main__":
    app.run()
