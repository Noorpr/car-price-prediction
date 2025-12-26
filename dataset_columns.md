# Cleaned Cars Dataset — Column Descriptions

This document describes the final columns of `cleaned_cars_data.csv`. It explains each column's meaning, data type, cleaning/normalization steps applied, and example values. At the end you'll find practical analysis and modeling use cases for this dataset.

## Columns

- **Model_name**: Full model string scraped from the listing.
	- Type: string
	- Notes: Original raw model description as appeared on the listing (contains model trims, submodels, sometimes year). Used as the canonical text field for display or further NLP.
	- Example: "Toyota Corolla 2016 GLI"

- **Year_model**: Manufactured/model year extracted from `Model_name` via regex matching `(19|20)\d{2}`.
	- Type: integer
	- Notes: Extracted and converted to `int64`. Used for age-based analyses and depreciation calculations. Rows without a matched year were dropped during final cleaning.
	- Example: `2016`

- **Manufacturer**: Brand or maker of the vehicle.
	- Type: categorical (string / pandas `category`)
	- Notes: Normalized from the listing; useful for grouping, one-hot encoding, and brand-level comparisons.
	- Example: `Toyota`

- **Car_name**: Short model name derived by removing `Year_model` and `Manufacturer` tokens from `Model_name`.
	- Type: string
	- Notes: Intended to capture the model/trim (e.g., "Corolla GLI"). Created to give a compact model identifier for display and grouping.
	- Example: `Corolla GLI`

- **Type**: Listing type/category.
	- Type: categorical
	- Notes: Converted to pandas `category`. Use for filtering or to control for seller-type effects on price.
	- Example: `أوتوماتيك`

- **Condition**: Vehicle condition descriptor.
	- Type: categorical
	- Notes: Converted to pandas `category`. Useful as a predictor of price and required maintenance.
	- Example: `مستعملة`

- **Distance**: Odometer reading (distance driven), normalized to integer kilometers.
	- Type: integer (`int64`)
	- Cleaning: Empty values filled with `0 كم` earlier, commas removed, Arabic "كم" suffix removed, then cast to integer.
	- Notes: Use as a numeric predictor for depreciation and maintenance risk. Check for unrealistic zeros or outliers before modeling.
	- Example: `85000`

- **Color**: Exterior color of the vehicle.
	- Type: string (filled mode where missing)
	- Cleaning: Missing values filled with the column mode. Descriptive text kept as-is (e.g., localized color names).
	- Notes: Useful for simple filtering and for models if color correlates with price in the market.
	- Example: `White`

- **Body_type**: Body style (e.g., Sedan, Hatchback, SUV).
	- Type: string / categorical
	- Notes: Helpful for segmentation and feature engineering (one-hot or embeddings for model input).
	- Example: `Sedan`

- **Engine_cc**: Engine displacement specification (cc).
	- Type: string or numeric depending on original formatting
	- Notes: May contain non-numeric characters in raw scraped text. You may convert to numeric (int) after cleaning (remove "cc" and commas) if needed for modeling.
	- Example: `1600`

- **Price**: Listing price normalized to integer (local currency).
	- Type: integer
	- Cleaning: Commas removed, currency label `ج.م.` removed, then cast to integer.
	- Notes: Target variable for price modeling and the main economic variable for analysis. Verify currency and remove extreme outliers as appropriate.
	- Example: `175000`

## Notes on final dataset

- Rows with missing values in required columns were dropped before final save.
- `Type` and `Condition` are stored as pandas `category` to save memory and speed grouping operations.
- Distances are in kilometers and Price is in local currency (Egyptian pounds). Confirm currency semantics before combining with external datasets.

## Use Cases

- **Price prediction (regression)**: Build models that predict `Price` from features such as `Year_model`, `Distance`, `Manufacturer`, `Engine_cc`, `Condition`, and `Body_type`.

- **Depreciation analysis**: Estimate how `Price` decays with age (`Year_model`) and mileage (`Distance`) for different `Manufacturer` and `Body_type` groups.

- **Market segmentation & clustering**: Use clustering (k-means, hierarchical, or GMM) on numeric features and encoded categorical features to identify buyer segments or typical car bundles (e.g., low-mileage luxury vs. high-mileage economy cars).

- **Anomaly detection / data quality checks**: Flag listings with implausible combinations (e.g., very low `Distance` but very old `Year_model`, or prices far outside the brand/model typical range) for manual review or automated filtering.

- **Inventory recommendation & matching**: For dealers, match supply to demand by recommending price changes or promotions based on comparable listings (similar `Manufacturer`, `Year_model`, `Distance`).

- **Feature engineering for downstream models**: Create derived features such as `Age = current_year - Year_model`, `km_per_year = Distance / Age` (handle Age=0), or brand-level median price for model-level predictors.

- **Visualization & reporting**: Produce dashboards and charts (price distribution, median price by `Manufacturer`, scatterplots price vs. distance) to support market insights and business decisions.

- **Search & filter powering a UI**: Use cleaned fields like `Car_name`, `Manufacturer`, `Price`, and `Distance` to implement efficient search and faceted filters on a classifieds site or internal inventory tool.

## Recommended next steps for users

- Validate the `Engine_cc` column formatting and convert to numeric if you plan to use it as a continuous predictor.
- Inspect `Price` and `Distance` distributions and remove top/bottom outliers before training models.
- If combining with external data (e.g., region, exchange rates), normalize currency and map any region-specific labels.

---

If you'd like, I can also (a) add a small example notebook cell showing how to load `cleaned_cars_data.csv` and compute a baseline price model, or (b) convert `Engine_cc` to numeric and add a brief exploratory plot. Which would you prefer?

