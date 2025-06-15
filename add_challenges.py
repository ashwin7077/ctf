import os
import hashlib
import random

HTML_FILE = "challenges.html"
CATEGORIES = ['misc', 'forensic', 'crypto', 'rev', 'pwn', 'osint', 'web']  

def get_input(prompt, optional=False):
    value = input(prompt)
    return value if value or not optional else None

def sha256_hash(flag):
    return hashlib.sha256(flag.encode()).hexdigest()

def create_html_base():
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attack On Hash Function CTF Challenges</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00ff99;
            --primary-dark: #00cc77;
            --primary-light: #99ffcc;
            --secondary: #00ccff;
            --secondary-dark: #0099cc;
            --secondary-light: #99e6ff;
            --dark-bg: #121212;
            --darker-bg: #0a0a0a;
            --card-bg: #1e1e1e;
            --card-hover: #252525;
            --text: #e0e0e0;
            --text-dim: #a0a0a0;
            --danger: #ff4d4d;
            --danger-dark: #cc0000;
            --success: #00cc66;
            --success-dark: #00994d;
            --warning: #ffcc00;
            --warning-dark: #cc9900;
            --elevation-1: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
            --elevation-2: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
            --elevation-3: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23);
            --elevation-4: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
            --transition-fast: all 0.1s ease;
            --transition-medium: all 0.3s ease;
            --transition-slow: all 0.5s ease;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Fira Code', 'Consolas', monospace;
            margin: 0;
            padding: 0;
            background-color: var(--dark-bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 255, 153, 0.03) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 204, 255, 0.03) 0%, transparent 20%);
        }

        ::selection {
            background-color: var(--primary);
            color: #000;
        }

        h1 {
            color: var(--primary);
            text-align: center;
            margin: 2rem 0;
            font-size: clamp(2rem, 5vw, 3.5rem);
            text-shadow: 0 0 10px rgba(0, 255, 153, 0.3);
            position: relative;
            display: inline-block;
            width: 100%;
            font-weight: 700;
            letter-spacing: -0.05em;
        }

        h1::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 3px;
        }

        h2 {
            color: var(--secondary);
            border-bottom: 2px solid var(--secondary);
            padding-bottom: 0.5rem;
            margin: 2.5rem 0 1.5rem;
            font-size: 1.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
        }

        h2::before {
            content: '#';
            margin-right: 0.5rem;
            color: var(--primary);
            font-weight: 700;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .logo {
            font-family: 'Share Tech Mono', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary);
            text-decoration: none;
            display: flex;
            align-items: center;
        }

        .logo span {
            color: var(--secondary);
        }

        .nav {
            display: flex;
            gap: 1.5rem;
        }

        .nav-link {
            color: var(--text);
            text-decoration: none;
            font-weight: 500;
            position: relative;
            padding: 0.5rem 0;
            transition: var(--transition-medium);
        }

        .nav-link:hover {
            color: var(--primary);
        }

        .nav-link::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background-color: var(--primary);
            transition: var(--transition-medium);
        }

        .nav-link:hover::after {
            width: 100%;
        }

        .category {
            margin-bottom: 3rem;
            background-color: var(--darker-bg);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            box-shadow: var(--elevation-1);
            transition: var(--transition-medium);
        }

        .category:hover {
            box-shadow: var(--elevation-2);
            transform: translateY(-2px);
        }

        .challenges-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .challenge {
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 8px;
            box-shadow: var(--elevation-1);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: var(--transition-medium);
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        }

        .challenge-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            padding: 0.5rem;
            margin: -0.5rem;
            transition: var(--transition-medium);
        }

        .challenge-header:hover {
            background-color: rgba(0, 255, 153, 0.05);
        }

        .challenge-header h3 {
            margin: 0;
            flex-grow: 1;
            color: var(--primary);
            font-size: 1.2rem;
        }

        .challenge-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .toggle-icon {
            margin-left: 1rem;
            transition: var(--transition-medium);
            font-size: 0.9rem;
            color: var(--primary);
        }

        .challenge-details {
            padding-top: 1rem;
            margin-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: none;
            animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .challenge-description {
            margin-bottom: 1rem;
            color: var(--text-dim);
        }

        .meta-item {
            display: flex;
            align-items: center;
            font-size: 0.85rem;
            color: var(--text-dim);
        }

        .meta-item i {
            margin-right: 0.4rem;
            font-size: 1rem;
        }

        .flag-form {
            margin-top: 1.5rem;
            position: relative;
        }

        .flag-input {
            width: 100%;
            padding: 0.8rem 1rem;
            background-color: var(--darker-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            color: var(--text);
            font-family: inherit;
            font-size: 0.95rem;
            transition: var(--transition-medium);
        }

        .flag-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 255, 153, 0.2);
        }

        .flag-input::placeholder {
            color: rgba(255, 255, 255, 0.3);
        }

        .flag-submit {
            margin-top: 0.8rem;
            padding: 0.7rem 1.5rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: #000;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-family: inherit;
            font-size: 0.95rem;
            transition: var(--transition-medium);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            width: 100%;
        }

        .flag-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 153, 0.3);
        }

        .flag-submit:active {
            transform: translateY(0);
        }

        .flag-submit i {
            font-size: 1rem;
        }

        .result {
            margin-top: 1rem;
            font-weight: 500;
            padding: 0.8rem;
            border-radius: 6px;
            text-align: center;
            font-size: 0.9rem;
            opacity: 0;
            transform: translateY(10px);
            transition: var(--transition-medium);
            display: none;
        }

        .result.show {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        .success {
            color: var(--success);
            background-color: rgba(0, 204, 102, 0.1);
            border: 1px solid rgba(0, 204, 102, 0.3);
        }

        .error {
            color: var(--danger);
            background-color: rgba(255, 77, 77, 0.1);
            border: 1px solid rgba(255, 77, 77, 0.3);
        }

        .loading {
            color: var(--secondary);
            background-color: rgba(0, 204, 255, 0.1);
            border: 1px solid rgba(0, 204, 255, 0.3);
        }

        .difficulty {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .difficulty-easy {
            background-color: rgba(0, 204, 102, 0.2);
            color: var(--success);
            border: 1px solid var(--success);
        }

        .difficulty-medium {
            background-color: rgba(255, 204, 0, 0.2);
            color: var(--warning);
            border: 1px solid var(--warning);
        }

        .difficulty-hard {
            background-color: rgba(255, 77, 77, 0.2);
            color: var(--danger);
            border: 1px solid var(--danger);
        }

        .footer {
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-dim);
            font-size: 0.9rem;
        }

        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background-color: var(--primary);
            opacity: 0;
            z-index: 9999;
            animation: confetti-fall 3s ease-in-out forwards;
        }

        @keyframes confetti-fall {
            0% {
                transform: translateY(-100px) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-5px); }
            40%, 80% { transform: translateX(5px); }
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 153, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(0, 255, 153, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 153, 0); }
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        code {
            background-color: rgba(0, 255, 153, 0.1);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Fira Code', monospace;
            color: var(--primary);
            font-size: 0.9rem;
            border: 1px solid rgba(0, 255, 153, 0.2);
        }

        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: var(--darker-bg);
            color: var(--text);
            text-align: center;
            border-radius: 6px;
            padding: 0.5rem;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: var(--transition-medium);
            font-size: 0.8rem;
            border: 1px solid rgba(0, 255, 153, 0.2);
            box-shadow: var(--elevation-2);
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .challenges-grid {
                grid-template-columns: 1fr;
            }
            
            .nav {
                display: none;
            }
            
            .category {
                padding: 1rem;
            }
        }

        /* Dark mode toggle (for future enhancement) */
        .theme-toggle {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: var(--elevation-2);
            transition: var(--transition-medium);
            z-index: 100;
        }

        .theme-toggle:hover {
            transform: scale(1.1);
            box-shadow: var(--elevation-3);
        }

        .theme-toggle i {
            font-size: 1.2rem;
            color: var(--text);
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <a href="index.html" class="logo">Attack On <span>&nbsp;Hash Function</span></a>
            <nav class="nav">
                <a href="index.html" class="nav-link">Home</a>
                <a href="challenges.html" class="nav-link">Challenges</a>
                <a href="scoreboard.html" class="nav-link">Scoreboard</a>
            </nav>
        </header>

        <main>
            <h1>CTF Challenge Platform</h1>
""")
        
        for cat in CATEGORIES:
            f.write(f'            <section class="category" id="cat-{cat}">\n')
            f.write(f'                <h2>{cat.upper()} Challenges</h2>\n')
            f.write(f'                <div class="challenges-grid" id="grid-{cat}">\n')
            f.write(f'                    <!-- {cat}-challenges-here -->\n')
            f.write('                </div>\n')
            f.write('            </section>\n\n')
        f.write("""        </main>

        <footer class="footer">
            <p>&copy; 2025 Attack On Hash Function CTF Platform. All rights reserved.</p>
        </footer>
    </div>

    <script>
        // Enhanced animations and interactions
        document.addEventListener('DOMContentLoaded', function() {
            // Hide empty categories first
            document.querySelectorAll('.category').forEach(category => {
                const grid = category.querySelector('.challenges-grid');
                if (grid && grid.children.length <= 1) { // 1 for the comment node
                    category.style.display = 'none';
                }
            });

            // Animate challenge cards with staggered delay
            const challenges = document.querySelectorAll('.challenge');
            challenges.forEach((challenge, index) => {
                challenge.style.opacity = '0';
                challenge.style.transform = 'translateY(30px)';
                challenge.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                
                setTimeout(() => {
                    challenge.style.opacity = '1';
                    challenge.style.transform = 'translateY(0)';
                }, 150 * index);
            });

            // Smooth scrolling for navigation
            document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId.startsWith('#')) {
            e.preventDefault(); // Only prevent default for anchor links
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                            });
                        }
                    }
                });
            });

            // Theme toggle functionality
            const themeToggle = document.getElementById('themeToggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', function() {
                    document.body.classList.toggle('light-mode');
                    this.querySelector('i').textContent = 
                        document.body.classList.contains('light-mode') ? '🌙' : '☀️';
                });
            }

            // Tooltip initialization
            document.querySelectorAll('.tooltip').forEach(el => {
                el.addEventListener('mouseenter', function() {
                    const tooltip = this.querySelector('.tooltiptext');
                    if (tooltip) {
                        tooltip.style.visibility = 'visible';
                        tooltip.style.opacity = '1';
                    }
                });
                
                el.addEventListener('mouseleave', function() {
                    const tooltip = this.querySelector('.tooltiptext');
                    if (tooltip) {
                        tooltip.style.visibility = 'hidden';
                        tooltip.style.opacity = '0';
                    }
                });
            });
        });

        function toggleChallengeDetails(id) {
            const details = document.getElementById(`details-${id}`);
            const icon = document.querySelector(`#${id} .toggle-icon`);
            if (details.style.display === 'none' || !details.style.display) {
                details.style.display = 'block';
                icon.textContent = '▲';
            } else {
                details.style.display = 'none';
                icon.textContent = '▼';
            }
        }

        function createConfetti() {
            const colors = ['#00ff99', '#00ccff', '#ffcc00', '#ff4d4d', '#9900ff'];
            for (let i = 0; i < 100; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.width = Math.random() * 10 + 5 + 'px';
                confetti.style.height = Math.random() * 10 + 5 + 'px';
                confetti.style.animationDuration = Math.random() * 3 + 2 + 's';
                document.body.appendChild(confetti);
                
                setTimeout(() => {
                    confetti.remove();
                }, 3000);
            }
        }
    </script>
</body>
</html>""")

def generate_challenge_html(id, name, desc, attachment, difficulty, flag_format, flag_hash):
    escaped_id = id.replace(" ", "_").lower()
    difficulty_class = f"difficulty-{difficulty.lower()}"
    accent_color = f"hsl({random.randint(0, 360)}, 80%, 60%)"
    
    return f"""
        <div class="challenge" id="{escaped_id}" style="--accent-color: {accent_color}">
            <div class="challenge-header" onclick="toggleChallengeDetails('{escaped_id}')">
                <h3>{name}</h3>
                <div class="challenge-meta">
                    <div class="meta-item"><i>⚡</i> <span class="{difficulty_class}">{difficulty}</span></div>
                </div>
                <i class="toggle-icon">▼</i>
            </div>
            
            <div class="challenge-details" id="details-{escaped_id}">
                <div class="challenge-description">
                    <p><strong>Description:</strong> {desc}</p>
                    {'<p><strong>Attachment:</strong> <a href="' + attachment + '" target="_blank">Download</a></p>' if attachment else ''}
                    <div class="meta-item"><i>🔑</i> <span class="tooltip">Flag Format<span class="tooltiptext">The flag must match this pattern exactly</span></span>: <code>{flag_format}</code></div>
                </div>
                
                <div class="flag-form">
                    <input type="text" class="flag-input" id="input-{escaped_id}" placeholder="Enter your flag here..." autocomplete="off">
                    <button class="flag-submit" onclick="checkFlag_{escaped_id}()">
                        <i>🔒</i> Submit Flag
                    </button>
                    <div class="result" id="result-{escaped_id}"></div>
                </div>
            </div>
        </div>
        
        <script>
        async function checkFlag_{escaped_id}() {{
            const input = document.getElementById("input-{escaped_id}").value.trim();
            const resultElement = document.getElementById("result-{escaped_id}");
            const challengeCard = document.getElementById("{escaped_id}");
            
            // Clear previous result and show loading state
            resultElement.className = "result loading show";
            resultElement.textContent = "🔐 Verifying your flag...";
            
            // Simulate network delay for realism
            await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 700));
            
            try {{
                // Client-side SHA-256 hashing
                const msgBuffer = new TextEncoder().encode(input);
                const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

                if (hashHex === "{flag_hash}") {{
                    // Correct flag
                    resultElement.className = "result success show";
                    resultElement.textContent = "✅ Correct! Flag accepted!";
                    
                    // Celebration effects
                    challengeCard.style.border = "1px solid var(--success)";
                    challengeCard.style.boxShadow = "0 0 20px rgba(0, 204, 102, 0.5)";
                    challengeCard.style.animation = "pulse 1.5s infinite";
                    
                    // Create confetti explosion
                    createConfetti();
                    
                    // Add success badge to challenge
                    const successBadge = document.createElement('div');
                    successBadge.innerHTML = '<div style="position: absolute; top: 10px; right: 10px; background: var(--success); color: black; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: bold;">SOLVED</div>';
                    challengeCard.appendChild(successBadge);
                    
                    // Disable input after success
                    document.getElementById("input-{escaped_id}").disabled = true;
                    document.querySelector(`button[onclick="checkFlag_{escaped_id}()"]`).disabled = true;
                    
                    // Stop pulse animation after 3 seconds
                    setTimeout(() => {{
                        challengeCard.style.animation = "";
                    }}, 3000);
                }} else {{
                    // Incorrect flag
                    resultElement.className = "result error show";
                    resultElement.textContent = "❌ Incorrect flag! Try again.";
                    
                    // Shake animation
                    challengeCard.style.animation = "shake 0.5s";
                    setTimeout(() => {{
                        challengeCard.style.animation = "";
                    }}, 500);
                }}
            }} catch (error) {{
                resultElement.className = "result error show";
                resultElement.textContent = "⚠️ Error verifying flag. Please try again.";
                console.error("Flag verification error:", error);
            }}
        }}
        </script>


        
    """

def insert_challenge_to_html(category, challenge_html):
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    placeholder = f"<!-- {category}-challenges-here -->"
    new_lines = []
    for line in lines:
        if placeholder in line:
            new_lines.append(challenge_html)
            new_lines.append('<script>document.querySelector(`.category[id="cat-' + category + '"]`).style.display = "block";</script>\n')
        new_lines.append(line)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    print("=== CTF Challenge Generator ===")
    print("Create professional CTF challenges with interactive verification\n")
    
    if not os.path.exists(HTML_FILE):
        print("✨ Creating base HTML template...")
        create_html_base()

    name = get_input("Challenge Name: ")
    desc = get_input("Description: ")
    attachment = get_input("Attachment Link (optional): ", optional=True)
    difficulty = get_input("Difficulty (Easy/Medium/Hard): ")
    flag_format = get_input("Flag Format (e.g., CTF{...}): ")
    real_flag = get_input("Real Flag (will be hashed): ")

    while True:
        category = get_input(f"Category ({', '.join(CATEGORIES)}): ").lower()
        if category in CATEGORIES:
            break
        print("❌ Invalid category. Please choose from the list.")

    flag_hash = sha256_hash(real_flag)
    chal_html = generate_challenge_html(name, name, desc, attachment, difficulty, flag_format, flag_hash)
    insert_challenge_to_html(category, chal_html)

    print(f"\n🎉 Challenge '{name}' successfully added to '{HTML_FILE}' under '{category}' category!")
    print("🔒 Flag has been securely hashed for client-side verification.")