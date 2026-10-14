
import joblib
import pandas as pd
from pathlib import Path

print("Loading model and preprocessor...")

model = joblib.load("random_forest_model.pkl")
preprocessor = joblib.load("preprocessor.pkl")

print("Model loaded successfully.")
print("Preprocessor loaded successfully.")

# Locate the dataset
dataset_path = Path("aprrentissage/read.csv")

if not dataset_path.exists():
    print(f"\nDataset not found: {dataset_path}")
    raise SystemExit(1)

print("\nLoading one real dataset record...")

# Read only the columns required by the preprocessor
expected_columns = list(preprocessor.feature_names_in_)
data = pd.read_csv(
    dataset_path,
    usecols=lambda column: column in expected_columns,
    nrows=100
)

missing = set(expected_columns) - set(data.columns)

if missing:
    print("Missing columns:", missing)
    raise SystemExit(1)

# Choose a complete row if possible
data = data[expected_columns].dropna()

if data.empty:
    print("No complete records found in the first 100 rows.")
    print("We need to inspect the dataset before testing.")
    raise SystemExit(1)

sample_data = data.iloc[[0]].copy()

# Convert commit_date to the numeric representation
# expected by the saved numeric preprocessing pipeline.
if "commit_date" in sample_data.columns:
    dates = pd.to_datetime(sample_data["commit_date"], errors="coerce")
    if dates.notna().all():
        sample_data["commit_date"] = (
            dates.astype("int64") / 10**9
        )

print("\nTransforming the sample record...")

try:
    processed_data = preprocessor.transform(sample_data)
    prediction = model.predict(processed_data)

    print("\nTest completed successfully!")
    print("Predicted class:", prediction[0])

except Exception as error:
    print("\nTest could not complete.")
    print("Error:", error)
    raise SystemExit(1)
