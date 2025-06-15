import pandas as pd

# Load the challenge points
challenge_points = pd.read_excel('challenges_with_points.xlsx')

# Load the user solve records
user_solves = pd.read_excel('CTF_updated.xlsx')

# Merge the two DataFrames based on 'Title' (challenge title)
merged = user_solves.merge(challenge_points, left_on='Challenge', right_on='Title', how='left')

# Now group by 'User' and sum their points
user_points = merged.groupby('User')['Points'].sum().reset_index()

# Sort by highest points
user_points = user_points.sort_values(by='Points', ascending=False)

# Show the final points table
print(user_points)

# Save the result
user_points.to_excel('user_total_points.xlsx', index=False)
