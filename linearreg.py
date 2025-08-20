import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Step 1: Load CSV file
df = pd.read_csv("student_scores.csv")

# Step 2: Choose independent (X) and dependent (y) variables
X = df[['Hours']]  # Independent variable(s)
y = df['Scores']   # Dependent variable

# Step 3: Split into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Fit linear regression model on training data
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Evaluate model on test data
y_pred = model.predict(X_test)

print("Intercept:", model.intercept_)
print("Coefficient(s):", model.coef_)
print("Train R² Score:", model.score(X_train, y_train))
print("Test R² Score:", r2_score(y_test, y_pred))
print("Test Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Step 6: Plot regression line
plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, model.predict(X), color='red', label='Regression line')
plt.xlabel("Hours Studied")
plt.ylabel("Scores")
plt.legend()
plt.savefig("assignment4_plot.png")   # Save plot (useful for WSL)
print("Plot saved as regression_plot.png")

# Step 7: Prediction function
def predict_score(hour):
    """Predict the score based on hours studied."""
    return model.predict(pd.DataFrame({'Hours': [hour]}))

# Step 8: Interactive loop
while True:
    hour = input("Enter hours studied (or 'exit' to quit): ").strip()
    if hour.lower() == "exit":
        print("quitting, bye!")
        break
    try:
        hour = float(hour)
        predicted_score = predict_score(hour)
        print(f"Predicted score for {hour} hours: {predicted_score[0]:.2f}")
    except ValueError:
        print("Invalid input, please enter a number or 'exit'.")
