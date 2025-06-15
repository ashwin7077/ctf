import pandas as pd
import os
import re

# Function to sanitize directory names
def sanitize_dirname(name):
    # Convert name to string to handle numeric values
    name = str(name)
    # Replace invalid characters with underscore
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', name)

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Read Excel files with error handling
try:
    solved_df = pd.read_excel('CTF_updated.xlsx')
    print("CTF_updated.xlsx read successfully.")
except Exception as e:
    print(f"Error reading CTF_updated.xlsx: {e}")
    raise
try:
    challenges_df = pd.read_excel('challenges_with_points.xlsx')
    print("challenges_with_points.xlsx read successfully.")
except Exception as e:
    print(f"Error reading challenges_with_points.xlsx: {e}")
    raise

# Create web directory if it doesn't exist
os.makedirs('user', exist_ok=True)

# Get unique users
users = solved_df['User'].unique()

for user in users:
    # Sanitize user name for directory creation
    safe_user = sanitize_dirname(user)  # Now handles integer user IDs
    user_dir = f'user/{safe_user}'
    try:
        os.makedirs(user_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory for user '{user}': {e}")
        continue
    
    # Filter solved challenges for this user
    user_solved = solved_df[solved_df['User'] == user][['Challenge', 'Solved time']]
    
    # Get all challenge titles
    all_challenges = challenges_df['Title'].tolist()
    
    # Find unsolved challenges
    solved_challenges = user_solved['Challenge'].tolist()
    unsolved_challenges = [challenge for challenge in all_challenges if challenge not in solved_challenges]
    
    # Get points for challenges
    challenge_points = dict(zip(challenges_df['Title'], challenges_df['Points']))
    
    # Generate HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTF Challenges - {user}</title>
    <style>
        body {{
            font-family: 'Helvetica', Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #000000;
            color: #ffffff;
        }}
        h1 {{
            text-align: center;
            color: #ffffff;
            font-weight: bold;
        }}
        h2 {{
            color: #d3d3d3;
            margin-top: 30px;
            font-weight: normal;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #1c1c1c;
            border: 1px solid #333333;
        }}
        th, td {{
            padding: 14px;
            text-align: left;
            border-bottom: 1px solid #333333;
        }}
        th {{
            background-color: #222222;
            color: #ffffff;
            font-weight: bold;
        }}
        td {{
            color: #e0e0e0;
        }}
        tr:hover {{
            background-color: #2d2d2d;
        }}
        .solved-table th {{
            background-color: #333333;
        }}
        .solved-table td {{
            color: #f0f0f0;
        }}
    </style>
</head>
<body>
    <h1>CTF Challenges for {user}</h1>
    
    <h2>Solved Challenges</h2>
    <table class="solved-table">
        <tr>
            <th>Challenge</th>
            <th>Solved Time</th>
            <th>Points</th>
        </tr>
    """
    
    # Add solved challenges to table
    for _, row in user_solved.iterrows():
        challenge = row['Challenge']
        points = challenge_points.get(challenge, 'N/A')
        html_content += f"""
        <tr>
            <td>{challenge}</td>
            <td>{row['Solved time']}</td>
            <td>{points}</td>
        </tr>
        """
    
    html_content += """
    </table>
    
    <h2>Unsolved Challenges</h2>
    <table>
        <tr>
            <th>Challenge</th>
            <th>Points</th>
        </tr>
    """
    
    # Add unsolved challenges to table
    for challenge in unsolved_challenges:
        points = challenge_points.get(challenge, 'N/A')
        html_content += f"""
        <tr>
            <td>{challenge}</td>
            <td>{points}</td>
        </tr>
        """
    
    html_content += """
    </table>
</body>
</html>
    """
    
    # Write HTML file
    try:
        with open(f'{user_dir}/challenges.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML file generated for user '{user}' in '{user_dir}'")
    except Exception as e:
        print(f"Error writing HTML file for user '{user}': {e}")

print("HTML files generation completed.")