import pandas as pd

# Load the Excel file
try:
    df = pd.read_excel('user_total_points.xlsx')  # Make sure 'scoreboard.xlsx' is in the same folder
except FileNotFoundError:
    print("❌ Error: 'scoreboard.xlsx' file not found. Please check the filename and path.")
    exit()

# Clean column names: remove spaces and lowercase
df.columns = df.columns.str.strip().str.lower()

# Check if 'points' column exists
if 'points' not in df.columns:
    print("❌ Error: 'points' column not found in your Excel sheet. Please make sure it's named correctly.")
    print(f"Available columns are: {list(df.columns)}")
    exit()

# Add Rank column
df['Rank'] = df['points'].rank(method='min', ascending=False).astype(int)

# Sort by rank
df = df.sort_values(by='Rank')

# Add medal emojis
def add_medal(rank):
    if rank == 1:
        return '🥇'
    elif rank == 2:
        return '🥈'
    elif rank == 3:
        return '🥉'
    else:
        return str(rank)

df['Rank'] = df['Rank'].apply(add_medal)

# Reorder columns
df.rename(columns={'user': 'User', 'points': 'Points'}, inplace=True)
df = df[['Rank', 'User', 'Points']]

# Generate HTML table (with all users)
html_table = df.to_html(index=False, classes='scoreboard', escape=False)

# Prepare graph data (top 10 only)
top_10 = df.head(10)
usernames = top_10['User'].tolist()
points = [int(p) for p in top_10['Points'].tolist()]  # Make sure they are integers

# Modern Green/White Theme HTML
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTF Scoreboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {{
        --primary: #2e7d32;
        --primary-light: #4caf50;
        --primary-lighter: #81c784;
        --primary-dark: #1b5e20;
        --primary-darker: #0d3c13;
        --accent: #a5d6a7;
        --accent-light: #c8e6c9;
        --accent-dark: #75a478;
        --dark: #121212;
        --darker: #0a0a0a;
        --light: #f5f5f5;
        --lighter: #ffffff;
        --success: #4caf50;
        --warning: #ffc107;
        --danger: #f44336;
        --info: #2196f3;
        --text-primary: rgba(255, 255, 255, 0.95);
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-tertiary: rgba(255, 255, 255, 0.5);
        --elevation-1: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
        --elevation-2: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
        --elevation-3: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23);
        --elevation-4: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
        --transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }}
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    body {{
        background: linear-gradient(135deg, var(--darker), var(--dark));
        color: var(--text-primary);
        font-family: 'Montserrat', sans-serif;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0;
        background-attachment: fixed;
        overflow-x: hidden;
        line-height: 1.6;
    }}
    
    /* Navigation Bar */
    .navbar {{
        width: 100%;
        background: rgba(18, 18, 18, 0.98);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1rem 2rem;
        display: flex;
        justify-content: center;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: var(--elevation-2);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .nav-container {{
        width: 100%;
        max-width: 1200px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .nav-logo {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        color: var(--lighter);
        text-decoration: none;
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px rgba(76, 175, 80, 0.3);
        letter-spacing: 1px;
        transition: var(--transition);
    }}
    
    .nav-logo:hover {{
        text-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
    }}
    
    .nav-links {{
        display: flex;
        gap: 1rem;
    }}
    
    .nav-link {{
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: var(--transition);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        position: relative;
        overflow: hidden;
    }}
    
    .nav-link::before {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-light), var(--accent));
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.3s ease;
    }}
    
    .nav-link:hover, .nav-link.active {{
        color: var(--lighter);
    }}
    
    .nav-link:hover::before, .nav-link.active::before {{
        transform: scaleX(1);
        transform-origin: left;
    }}
    
    .nav-link i {{
        font-size: 1rem;
    }}
    
    .container {{
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1.5rem;
        flex: 1;
    }}
    
    header {{
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        width: 100%;
    }}
    
    h1 {{
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2.5rem, 5vw, 4rem);
        color: var(--lighter);
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px rgba(76, 175, 80, 0.3);
        position: relative;
        z-index: 1;
        line-height: 1.2;
    }}
    
    h1::after {{
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-light), var(--accent));
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
    }}
    
    .subtitle {{
        font-size: 1.2rem;
        color: var(--text-secondary);
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
        font-weight: 300;
    }}
    
    .chart-container {{
        width: 100%;
        max-width: 1000px;
        margin: 3rem auto;
        background: rgba(18, 18, 18, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--elevation-3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: var(--transition);
        height: 500px;
        position: relative;
        overflow: hidden;
    }}
    
    .chart-container::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(76, 175, 80, 0.1) 0%, rgba(0, 0, 0, 0) 70%);
        pointer-events: none;
    }}
    
    .chart-container:hover {{
        transform: translateY(-5px);
        box-shadow: var(--elevation-4);
        border-color: rgba(255, 255, 255, 0.15);
    }}
    
    canvas {{
        width: 100% !important;
        height: auto !important;
    }}
    
    table.scoreboard {{
        width: 100%;
        max-width: 1000px;
        margin: 4rem auto;
        border-collapse: separate;
        border-spacing: 0;
        background: rgba(18, 18, 18, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: var(--elevation-3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: var(--transition);
    }}
    
    table.scoreboard:hover {{
        transform: translateY(-5px);
        box-shadow: var(--elevation-4);
        border-color: rgba(255, 255, 255, 0.15);
    }}
    
    table.scoreboard thead {{
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    }}
    
    table.scoreboard th {{
        padding: 1.5rem 2rem;
        text-align: left;
        font-weight: 600;
        color: var(--lighter);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.9rem;
        font-family: 'Orbitron', sans-serif;
    }}
    
    table.scoreboard th:first-child {{
        border-top-left-radius: 20px;
    }}
    
    table.scoreboard th:last-child {{
        border-top-right-radius: 20px;
    }}
    
    table.scoreboard tbody tr {{
        transition: var(--transition);
    }}
    
    table.scoreboard tbody tr:nth-child(odd) {{
        background: rgba(255, 255, 255, 0.03);
    }}
    
    table.scoreboard tbody tr:hover {{
        background: rgba(76, 175, 80, 0.15);
        transform: scale(1.01);
    }}
    
    table.scoreboard td {{
        padding: 1.5rem 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-weight: 400;
        color: var(--text-primary);
    }}
    
    table.scoreboard td:first-child {{
        font-weight: 700;
        text-align: center;
        width: 80px;
        font-size: 1.1em;
        letter-spacing: 1px;
    }}
    
    table.scoreboard tr:last-child td {{
        border-bottom: none;
    }}
    
    /* Rank specific styling */
    .rank-1 {{
        background: rgba(255, 215, 0, 0.05) !important;
    }}
    
    .rank-1 td:first-child {{
        color: #ffd700;
        text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
        font-size: 1.3em;
    }}
    
    .rank-2 {{
        background: rgba(192, 192, 192, 0.05) !important;
    }}
    
    .rank-2 td:first-child {{
        color: #c0c0c0;
        text-shadow: 0 0 8px rgba(192, 192, 192, 0.5);
        font-size: 1.2em;
    }}
    
    .rank-3 {{
        background: rgba(205, 127, 50, 0.05) !important;
    }}
    
    .rank-3 td:first-child {{
        color: #cd7f32;
        text-shadow: 0 0 8px rgba(205, 127, 50, 0.5);
        font-size: 1.1em;
    }}
    
    /* Responsive adjustments */
    @media (max-width: 992px) {{
        .container {{
            padding: 2rem 1rem;
        }}
        
        .chart-container, table.scoreboard {{
            padding: 1.5rem;
        }}
        
        table.scoreboard th, table.scoreboard td {{
            padding: 1.2rem 1.5rem;
        }}
    }}
    
    @media (max-width: 768px) {{
        .nav-container {{
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .nav-links {{
            width: 100%;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .chart-container {{
            height: 400px;
            padding: 1.2rem;
        }}
        
        table.scoreboard th, table.scoreboard td {{
            padding: 1rem;
            font-size: 0.9rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
        }}
    }}
    
    @media (max-width: 576px) {{
        .nav-links {{
            flex-direction: column;
            gap: 0.5rem;
            align-items: center;
        }}
        
        .nav-link {{
            width: 100%;
            text-align: center;
            justify-content: center;
        }}
        
        .chart-container {{
            height: 350px;
            padding: 1rem;
        }}
        
        table.scoreboard th, table.scoreboard td {{
            padding: 0.8rem;
            font-size: 0.85rem;
        }}
        
        h1 {{
            font-size: 2rem;
        }}
        
        .subtitle {{
            font-size: 1rem;
        }}
    }}
    
    /* Animated background elements */
    .bg-elements {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        opacity: 0.6;
    }}
    
    .bg-element {{
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        animation: float 20s infinite linear;
        opacity: 0.5;
    }}
    
    @keyframes float {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 0.5; }}
        50% {{ transform: translateY(-50px) rotate(180deg); opacity: 0.8; }}
        100% {{ transform: translateY(0) rotate(360deg); opacity: 0.5; }}
    }}
    
    /* Footer */
    footer {{
        width: 100%;
        background: rgba(18, 18, 18, 0.9);
        padding: 2rem 1.5rem;
        text-align: center;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .footer-content {{
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }}
    
    .footer-links {{
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
        justify-content: center;
    }}
    
    .footer-link {{
        color: var(--text-secondary);
        text-decoration: none;
        transition: var(--transition);
        font-weight: 400;
        position: relative;
    }}
    
    .footer-link::after {{
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0;
        height: 1px;
        background: var(--primary-light);
        transition: width 0.3s ease;
    }}
    
    .footer-link:hover {{
        color: var(--accent);
    }}
    
    .footer-link:hover::after {{
        width: 100%;
    }}
    
    .copyright {{
        color: var(--text-tertiary);
        font-size: 0.9rem;
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(18, 18, 18, 0.5);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(var(--primary-dark), var(--primary-light));
        border-radius: 10px;
        border: 2px solid rgba(18, 18, 18, 0.5);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(var(--primary), var(--primary-lighter));
    }}
    
    /* Floating particles animation */
    .particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }}
    
    .particle {{
        position: absolute;
        background: rgba(76, 175, 80, 0.5);
        border-radius: 50%;
        filter: blur(1px);
        animation: float-particle 15s infinite linear;
    }}
    
    @keyframes float-particle {{
        0% {{ transform: translateY(0) translateX(0); opacity: 0; }}
        10% {{ opacity: 0.5; }}
        90% {{ opacity: 0.5; }}
        100% {{ transform: translateY(-100vh) translateX(50px); opacity: 0; }}
    }}
    </style>
</head>
<body>
    <div class="bg-elements">
        <div class="bg-element" style="width: 300px; height: 300px; top: 10%; left: 5%; animation-delay: 0s;"></div>
        <div class="bg-element" style="width: 400px; height: 400px; bottom: 15%; right: 10%; animation-delay: 3s;"></div>
        <div class="bg-element" style="width: 200px; height: 200px; top: 50%; left: 30%; animation-delay: 6s;"></div>
    </div>
    
    <!-- Navigation Bar -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">CTF Arena</a>
            <div class="nav-links">
                <a href="index.html" class="nav-link"><i class="fas fa-home"></i> Home</a>
                <a href="challenges.html" class="nav-link"><i class="fas fa-flag"></i> Challenges</a>
                <a href="scoreboard.html" class="nav-link active"><i class="fas fa-trophy"></i> Scoreboard</a>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <header>
            <h1>Attack On Hash Function</h1>
            <p class="subtitle">Discord CTF Dynamic Scoreboard - Real-time tracking of competitors' progress and rankings</p>
        </header>
        
        <div class="chart-container">
            <canvas id="pointsChart" width="800" height="400"></canvas>
        </div>
        
        {html_table}
    </div>

    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="footer-links">
                <a href="#" class="footer-link">Terms</a>
                <a href="#" class="footer-link">Privacy</a>
                <a href="#" class="footer-link">Contact</a>
            </div>
            <p class="copyright">© 2025 Attack On Hash Function. All rights reserved.</p>
        </div>
    </footer>

    <script>
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
        gradient.addColorStop(0, 'rgba(46, 125, 50, 0.8)');
        gradient.addColorStop(1, 'rgba(139, 195, 74, 0.8)');
        
        const pointsChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {usernames},
                datasets: [{{
                    label: 'Points',
                    data: {points},
                    backgroundColor: gradient,
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1,
                    borderRadius: 8,
                    hoverBackgroundColor: 'rgba(255, 255, 255, 0.2)',
                    hoverBorderColor: 'rgba(255, 255, 255, 0.5)',
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
                        backgroundColor: 'rgba(18, 18, 18, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#e2e2e2',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        padding: 15,
                        cornerRadius: 10,
                        displayColors: true,
                        boxPadding: 5,
                        callbacks: {{
                            label: function(context) {{
                                return `${{context.parsed.y.toLocaleString()}} points`;
                            }}
                        }}
                    }},
                    title: {{
                        display: true,
                        text: 'Top 10 CTF Competitors (Points Distribution)',
                        color: '#ffffff',
                        font: {{
                            size: 18,
                            family: 'Montserrat',
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
                        min: getRoundedMin({points}),
                        max: getRoundedMax({points}),
                        ticks: {{
                            color: 'rgba(255, 255, 255, 0.7)',
                            font: {{
                                family: 'Montserrat',
                                size: 12
                            }},
                            padding: 10,
                            stepSize: getStepSize({points}),
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }},
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.05)',
                            drawBorder: false
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false,
                            drawBorder: false
                        }},
                        ticks: {{
                            color: 'rgba(255, 255, 255, 0.7)',
                            font: {{
                                family: 'Montserrat',
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
    </script>

    
</body>
</html>
"""

# Save to file
with open('scoreboard.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ Green/white theme scoreboard saved as scoreboard.html")