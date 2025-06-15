import html
import re
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

def sanitize_text(text):
    """Sanitize text to prevent HTML injection."""
    if not isinstance(text, str):
        return ""
    return html.escape(text.strip())


def main():
    # Read Excel file
    try:
        df = pd.read_excel("challenges_with_points.xlsx", sheet_name="Sheet1")
    except FileNotFoundError:
        print("Error: challenges_with_points.xlsx not found.")
        return
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Read HTML file
    try:
        with open("challenges.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: challenges.html not found.")
        return
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all challenge divs
    challenges = soup.find_all("div", class_="challenge")

    # Process Excel data
    for _, row in df.iterrows():
        title = row["Title"]
        if pd.isna(title) or not isinstance(title, str):
            continue  # Skip invalid titles

        points = int(row["Points"]) if pd.notna(row["Points"]) else 0

        # Find matching challenge by title
        for challenge in challenges:
            h3 = challenge.find("h3")
            if h3 and h3.text.strip() == title:
                # Find or create challenge-header
                header = challenge.find("div", class_="challenge-header")
                if not header:
                    # Create challenge-header if missing
                    header = soup.new_tag(
                        "div", attrs={"class": "challenge-header"})
                    h3.insert_before(header)
                    header.append(h3)  # Move title into header
                    difficulty = challenge.find("div", class_="difficulty")
                    if difficulty:
                        # Move difficulty into header
                        header.append(difficulty)

                # Check if points already exist
                points_div = header.find("div", class_="points")
                if points_div:
                    # Update existing points
                    points_div.string = f"🚩{points}"
                else:
                    # Add new points div with similar styling to difficulty
                    points_html = f'<div class="points">🚩{points}</div>'
                    points_tag = BeautifulSoup(points_html, "html.parser")
                    difficulty = header.find("div", class_="difficulty")
                    if difficulty:
                        difficulty.insert_after(points_tag)
                    else:
                        header.append(points_tag)
                break

    # Write updated HTML to a new file
    try:
        with open("challenges.html", "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
        print("Updated HTML written to updated_challenges.html")
    except Exception as e:
        print(f"Error writing HTML file: {e}")


if __name__ == "__main__":
    main()