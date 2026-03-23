import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("Crop_recommendation.csv")

# Select features
X = data[['temperature', 'humidity', 'rainfall']]

# Select label
y = data['label']

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Test the model
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# Save trained model
joblib.dump(model, "crop_model.pkl")

print("Model saved successfully!")

# Example weather input
sample = pd.DataFrame(
    [[30, 70, 120]],
    columns=['temperature', 'humidity', 'rainfall']
)

# Get probability for each crop
probabilities = model.predict_proba(sample)[0]

# Get crop names
crops = model.classes_

# Combine crop names and probabilities
crop_prob_list = list(zip(crops, probabilities))

# Sort by probability
crop_prob_list.sort(key=lambda x: x[1], reverse=True)

print("\nTop 3 Crop Recommendations:")

# Print top 3 crops
for crop, prob in crop_prob_list[:3]:
    print(f"{crop} : {round(prob*100,2)}%")