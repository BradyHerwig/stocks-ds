# Project conventions (stocks-ds)

## Notebooks-first workflow

For this project, use **Jupyter notebooks** (`.ipynb`) for all analysis and project-facing code:

- Data acquisition, EDA, feature engineering, modeling, and reporting live in `notebooks/`
- Do **not** create notebook-style `.py` scripts in `notebooks/` (no `# %%` cell scripts)
- Prefer numbered notebooks: `00_data_acquisition.ipynb`, `01_eda.ipynb`, `02_feature_engineering.ipynb`, etc.

## Documentation style

- The author writes all markdown explanations manually — do **not** add narrative markdown cells or explanatory paragraphs
- Keep notebook changes to code and minimal structural markdown (titles/section headers only if needed)
- Leave space between sections so the author can insert their own write-ups later

## What stays as Python modules

Reusable library code belongs in `src/stocks/` (loaders, features, config, utils). Notebooks import from there; they are not a replacement for the package.

CLI utilities (e.g. `scripts/download_data.py`) are fine when a one-off command is more practical than a notebook cell.