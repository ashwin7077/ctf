import pandas as pd
import os
import re
from bs4 import BeautifulSoup
import json

# Function to sanitize directory names
def sanitize_dirname(name):
    # Convert name to string to handle numeric values
    name = str(name)
    # Replace invalid characters with underscore
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', name)

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Read user points from user_total_points.xlsx
try:
    points_df = pd.read_excel('user_total_points.xlsx')
    print("user_total_points.xlsx read successfully.")
except Exception as e:
    print(f"Error reading user_total_points.xlsx: {e}")
    raise

# Ensure points_df has 'User' and 'Points' columns
if not {'User', 'Points'}.issubset(points_df.columns):
    raise ValueError("user_total_points.xlsx must contain 'User' and 'Points' columns.")

# Sort users by points in descending order
points_df = points_df.sort_values(by='Points', ascending=False).reset_index(drop=True)

# Assign ranks with medal emojis for top 3
medals = ['🥇', '🥈', '🥉']
points_df['Rank'] = [medals[i] if i < 3 else str(i + 1) for i in range(len(points_df))]

# Read the existing scoreboard.html
try:
    with open('scoreboard.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    print("scoreboard.html read successfully.")
except Exception as e:
    print(f"Error reading scoreboard.html: {e}")
    raise

# Find the scoreboard table body
table = soup.find('table', class_='scoreboard')
if not table:
    raise ValueError("Scoreboard table not found in scoreboard.html.")
tbody = table.find('tbody')
if not tbody:
    raise ValueError("Scoreboard table body not found in scoreboard.html.")

# Clear existing tbody content
tbody.clear()

# Add new rows with hyperlinks
for _, row in points_df.iterrows():
    user = row['User']
    points = row['Points']
    rank = row['Rank']
    # Sanitize user name for directory link
    safe_user = sanitize_dirname(user)  # Now handles integer user IDs
    # Relative path to user's challenges.html
    user_link = f"user/{safe_user}/challenges.html"
    # Create new table row
    tr = soup.new_tag('tr')
    # Add rank cell
    td_rank = soup.new_tag('td')
    td_rank.string = rank
    tr.append(td_rank)
    # Add user cell with hyperlink
    td_user = soup.new_tag('td')
    a = soup.new_tag('a', href=user_link)
    a.string = str(user)  # Ensure user is string for display
    td_user.append(a)
    tr.append(td_user)
    # Add points cell
    td_points = soup.new_tag('td')
    td_points.string = str(points)
    tr.append(td_points)
    # Append row to tbody
    tbody.append(tr)

# Update rank classes for top 3
for i, tr in enumerate(tbody.find_all('tr')):
    if i == 0:
        tr['class'] = tr.get('class', []) + ['rank-1']
    elif i == 1:
        tr['class'] = tr.get('class', []) + ['rank-2']
    elif i == 2:
        tr['class'] = tr.get('class', []) + ['rank-3']

# Update Chart.js data in the script tag
script = soup.find('script', string=lambda text: text and 'pointsChart' in text)
if script:
    # Extract top 10 users and points for the chart
    top_10 = points_df.head(10)
    labels = json.dumps(list(top_10['User'].astype(str)))  # Convert to string for JSON
    data = list(top_10['Points'])
    # Update the Chart.js configuration
    new_chart_data = f"""
        // Add rank classes to table rows
        document.addEventListener('DOMContentLoaded', function() {{
            const rows = document.querySelectorAll('.scoreboard tbody tr');
            rows.forEach((row, index) => {{
                const rankCell = row.querySelector('td:first-child');
                if (rankCell.textContent.includes('🥇')) {{
                    row.classList.add('rank-1');
                }} else if (rankCell.textContent.includes('🥈')) {{
                    row.classList.add('rank-2');
                }} else if (rankCell.textContent.includes('🥉')) {{
                    row.classList.add('rank-3');
                }}
            }});
        }});
        
        // Enhanced Chart Configuration
        const ctx = document.getElementById('pointsChart').getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(224, 224, 224, 0.75)');
        gradient.addColorStop(1, 'rgba(224, 224, 224, 0.55)');
        
        const pointsChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {labels},
                datasets: [{{
                    label: 'Points',
                    data: {data},
                    backgroundColor: gradient,
                    borderColor: 'rgba(224, 224, 224, 0.9)',
                    borderWidth: 1,
                    borderRadius: 2,
                    hoverBackgroundColor: 'rgba(255, 255, 255, 0.9)',
                    hoverBorderColor: '#ffffff',
                    hoverBorderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                layout: {{
                    padding: {{
                        top: 20,
                        right: 20,
                        bottom: 30,
                        left: 30
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false,
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(16, 16, 16, 0.95)',
                        titleColor: '#ffffff',
                        bodyColor: '#e2e2e2',
                        borderColor: 'rgba(42, 42, 42, 0.8)',
                        borderWidth: 1,
                        padding: 15,
                        cornerRadius: 4,
                        displayColors: false,
                        boxPadding: 5,
                        callbacks: {{
                            label: function(context) {{
                                return `${{context.parsed.y.toLocaleString()}} points`;
                            }}
                        }}
                    }},
                    title: {{
                        display: false,
                        text: 'Top 10 CTF Competitors (Points Distribution)',
                        color: '#ffffff',
                        font: {{
                            size: 18,
                            family: "'Courier New', monospace",
                            weight: '600'
                        }},
                        padding: {{
                            top: 10,
                            bottom: 20
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        min: getRoundedMin({data}),
                        max: getRoundedMax({data}),
                        ticks: {{
                            color: '#a0a0a0',
                            font: {{
                                family: "'Courier New', monospace",
                                size: 12
                            }},
                            padding: 10,
                            stepSize: getStepSize({data}),
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }},
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.06)',
                            drawBorder: false
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false,
                            drawBorder: false
                        }},
                        ticks: {{
                            color: '#a0a0a0',
                            font: {{
                                family: "'Courier New', monospace",
                                size: 12
                            }},
                            padding: 5,
                            maxRotation: 45,
                            minRotation: 45
                        }}
                    }}
                }},
                animation: {{
                    duration: 1500,
                    easing: 'easeOutQuart'
                }},
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }}
            }}
        }});

        // Helper functions for clean axis scaling
        function getRoundedMin(points) {{
            const min = Math.min(...points);
            return Math.floor(min / 1000) * 1000;
        }}
        
        function getRoundedMax(points) {{
            const max = Math.max(...points);
            return Math.ceil(max / 1000) * 1000;
        }}
        
        function getStepSize(points) {{
            const range = getRoundedMax(points) - getRoundedMin(points);
            if (range <= 5000) return 1000;
            if (range <= 10000) return 2000;
            return 5000;
        }}
    """
    script.string = new_chart_data
else:
    print("Warning: Chart.js script not found in scoreboard.html.")

# Write to scoreboard.html
try:
    with open('scoreboard.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    print("scoreboard.html generated successfully.")
except Exception as e:
    print(f"Error writing scoreboard.html: {e}")