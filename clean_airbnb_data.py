import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent

ROME_PATH = BASE_DIR / "data" / "extracted" / "rome" / "rome_listings_detailed.csv"
FLORENCE_PATH = BASE_DIR / "data" / "extracted" / "florence" / "florence_listings_detailed.csv"
MILAN_PATH = BASE_DIR / "data" / "extracted" / "milan" / "milan_listings_detailed.csv"

CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = CLEANED_DIR / "italy_airbnb_listings_cleaned.csv"

# Load data
rome = pd.read_csv(ROME_PATH, low_memory=False)
florence = pd.read_csv(FLORENCE_PATH, low_memory=False)
milan = pd.read_csv(MILAN_PATH, low_memory=False)

# Add city column
rome["city"] = "Rome"
florence["city"] = "Florence"
milan["city"] = "Milan"

# Combine datasets
airbnb = pd.concat([rome, florence, milan], ignore_index=True)

print("Combined dataset shape:", airbnb.shape)
print("Columns:")
print(airbnb.columns.tolist())

# Keep useful columns
columns_to_keep = [
    "id",
    "listing_url",
    "name",
    "city",
    "host_id",
    "host_name",
    "host_is_superhost",
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "bedrooms",
    "beds",
    "price",
    "minimum_nights",
    "availability_365",
    "number_of_reviews",
    "number_of_reviews_ltm",
    "reviews_per_month",
    "review_scores_rating",
    "review_scores_location",
    "review_scores_value",
    "calculated_host_listings_count"
]

airbnb = airbnb[columns_to_keep]

# Clean price column
airbnb["price"] = (
    airbnb["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("€", "", regex=False)
    .str.replace(",", "", regex=False)
)

airbnb["price"] = pd.to_numeric(airbnb["price"], errors="coerce")

# Remove bad rows
airbnb = airbnb.dropna(subset=["price", "availability_365", "accommodates"])

airbnb = airbnb[
    (airbnb["price"] > 0) &
    (airbnb["price"] <= 1000) &
    (airbnb["availability_365"] >= 0) &
    (airbnb["availability_365"] <= 365) &
    (airbnb["accommodates"] >= 1)
]

# Fill missing review values
airbnb["reviews_per_month"] = airbnb["reviews_per_month"].fillna(0)
airbnb["number_of_reviews_ltm"] = airbnb["number_of_reviews_ltm"].fillna(0)

# Create calculated fields
airbnb["availability_rate"] = airbnb["availability_365"] / 365
airbnb["occupancy_proxy"] = 1 - airbnb["availability_rate"]
airbnb["estimated_booked_nights"] = 365 - airbnb["availability_365"]
airbnb["estimated_annual_revenue"] = airbnb["price"] * airbnb["estimated_booked_nights"]
airbnb["price_per_guest"] = airbnb["price"] / airbnb["accommodates"]

airbnb["price_per_bedroom"] = airbnb["price"] / airbnb["bedrooms"]
airbnb.loc[
    airbnb["bedrooms"].isna() | (airbnb["bedrooms"] <= 0),
    "price_per_bedroom"
] = None

# Rename neighborhood column
airbnb = airbnb.rename(columns={
    "neighbourhood_cleansed": "neighborhood"
})

# Save cleaned data
airbnb.to_csv(OUTPUT_PATH, index=False)

print("Cleaned dataset shape:", airbnb.shape)
print(f"Cleaned file saved to: {OUTPUT_PATH}")

# Create city-level summary
city_summary = airbnb.groupby("city").agg(
    total_listings=("id", "count"),
    avg_price=("price", "mean"),
    median_price=("price", "median"),
    avg_availability_rate=("availability_rate", "mean"),
    avg_occupancy_proxy=("occupancy_proxy", "mean"),
    avg_estimated_annual_revenue=("estimated_annual_revenue", "mean"),
    avg_recent_reviews=("number_of_reviews_ltm", "mean"),
    avg_reviews_per_month=("reviews_per_month", "mean"),
    avg_rating=("review_scores_rating", "mean")
).reset_index()

city_summary.to_csv(CLEANED_DIR / "italy_airbnb_city_summary.csv", index=False)

# Create neighborhood-level summary
neighborhood_summary = airbnb.groupby(["city", "neighborhood"]).agg(
    total_listings=("id", "count"),
    avg_price=("price", "mean"),
    median_price=("price", "median"),
    avg_availability_rate=("availability_rate", "mean"),
    avg_occupancy_proxy=("occupancy_proxy", "mean"),
    avg_estimated_annual_revenue=("estimated_annual_revenue", "mean"),
    avg_recent_reviews=("number_of_reviews_ltm", "mean"),
    avg_reviews_per_month=("reviews_per_month", "mean"),
    avg_rating=("review_scores_rating", "mean"),
    avg_price_per_guest=("price_per_guest", "mean")
).reset_index()

# Keep neighborhoods with enough listings to be meaningful
neighborhood_summary = neighborhood_summary[
    neighborhood_summary["total_listings"] >= 20
].copy()

# Make sure scoring columns are numeric
score_cols = [
    "avg_price",
    "avg_recent_reviews",
    "avg_estimated_annual_revenue",
    "avg_rating",
    "total_listings"
]

for col in score_cols:
    neighborhood_summary[col] = pd.to_numeric(neighborhood_summary[col], errors="coerce")

# Fill missing values so the score does not become NaN
neighborhood_summary["avg_price"] = neighborhood_summary["avg_price"].fillna(
    neighborhood_summary["avg_price"].median()
)

neighborhood_summary["avg_recent_reviews"] = neighborhood_summary["avg_recent_reviews"].fillna(
    neighborhood_summary["avg_recent_reviews"].median()
)

neighborhood_summary["avg_estimated_annual_revenue"] = neighborhood_summary["avg_estimated_annual_revenue"].fillna(
    neighborhood_summary["avg_estimated_annual_revenue"].median()
)

neighborhood_summary["total_listings"] = neighborhood_summary["total_listings"].fillna(
    neighborhood_summary["total_listings"].median()
)

# If ratings are missing, use a neutral rating
if neighborhood_summary["avg_rating"].isna().all():
    neighborhood_summary["avg_rating"] = 4.5
else:
    neighborhood_summary["avg_rating"] = neighborhood_summary["avg_rating"].fillna(
        neighborhood_summary["avg_rating"].median()
    )

# Normalize values from 0 to 100
def normalize(series):
    min_val = series.min()
    max_val = series.max()

    if pd.isna(min_val) or pd.isna(max_val):
        return pd.Series([50] * len(series), index=series.index)

    if max_val == min_val:
        return pd.Series([50] * len(series), index=series.index)

    return ((series - min_val) / (max_val - min_val)) * 100

# Create component scores
neighborhood_summary["pricing_score"] = normalize(neighborhood_summary["avg_price"])
neighborhood_summary["demand_score"] = normalize(neighborhood_summary["avg_recent_reviews"])
neighborhood_summary["revenue_score"] = normalize(neighborhood_summary["avg_estimated_annual_revenue"])
neighborhood_summary["rating_score"] = normalize(neighborhood_summary["avg_rating"])

# Lower competition is better, so reverse total listings
neighborhood_summary["competition_score"] = 100 - normalize(neighborhood_summary["total_listings"])

# Final weighted market opportunity score
neighborhood_summary["market_opportunity_score"] = (
    0.25 * neighborhood_summary["pricing_score"] +
    0.25 * neighborhood_summary["demand_score"] +
    0.20 * neighborhood_summary["revenue_score"] +
    0.15 * neighborhood_summary["rating_score"] +
    0.15 * neighborhood_summary["competition_score"]
).round(2)

# Save updated neighborhood summary
neighborhood_summary.to_csv(CLEANED_DIR / "italy_airbnb_neighborhood_summary.csv", index=False)

print("City summary saved.")
print("Neighborhood summary saved with market opportunity score.")
print(neighborhood_summary[["city", "neighborhood", "market_opportunity_score"]].head(10))
print(neighborhood_summary["market_opportunity_score"].describe())