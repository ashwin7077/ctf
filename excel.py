import pandas as pd
import json

# Load existing Excel file
df = pd.read_excel("output.xlsx", dtype={'id': str})

# Load members from JSON with correct encoding
with open("members.json", "r", encoding="utf-8") as f:
    members = json.load(f)

# Extract existing user IDs from Excel
existing_ids = set(df['id'].astype(str))

# Loop through each member in JSON
new_rows = []
for member in members:
    user_id = member.get("userId")
    username = member.get("username")

    # Skip if ID is unknown or already exists
    if not user_id or user_id == "Unknown" or user_id in existing_ids:
        continue

    # Add new user
    new_rows.append({"id": user_id, "display_name": username})
    print(f"Added: {username} ({user_id})")

# Append new entries if any
if new_rows:
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)

# Save the updated Excel file
df.to_excel("output.xlsx", index=False)
print("Updated output.xlsx with new users.")
