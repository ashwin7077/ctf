import pandas as pd

# Read the Excel file
try:
    df = pd.read_excel('../Challenge_Solve_Counts.xlsx')  # Adjusted to assumed correct filename
    print("Challenge_Solves.xlsx read successfully.")
except Exception as e:
    print(f"Error reading Challenge_Solves.xlsx: {e}")
    raise

# Function to calculate points
def calculate_points(solves):
    if solves <= 1:
        return 500
    else:
        points = 500 - (solves - 1) * 50
        return max(points, 50)  # Ensure points don't go below 50

# Apply the calculation
df['Points'] = df['Solve count'].apply(calculate_points)

# Show the updated DataFrame
print(df)

# Save the result to a new Excel file
try:
    df.to_excel('challenges_with_points.xlsx', index=False)
    print("challenges_with_points.xlsx saved successfully.")
except Exception as e:
    print(f"Error saving challenges_with_points.xlsx: {e}")
    raise