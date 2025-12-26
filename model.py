import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")

# Strip spaces and remove hidden characters
data.columns = data.columns.str.strip()

print("Columns in CSV:", data.columns)  # Debug line

# Select features and target
X = data[['amount', 'frequency']]
y = data['is_fraud']

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "fraud_model.pkl")

print("✅ Fraud detection model trained and saved")

