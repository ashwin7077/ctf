"""Rebuild the scoreboard site in one go.

Steps:
  1. Scrape per-challenge solve counts from the CTF admin panel
  2. Compute dynamic challenge points
  3. Write point badges into challenges.html          (points.py)
  4. Merge members.json into the Discord id -> name map (excel.py)
  5. Replace Discord ids in the solve log with names
  6. Total points per user                             (rank.py)
  7. Rebuild scoreboard.html                           (dataconnect.py)
  8. Rebuild user/<name>/challenges.html               (user.py)

Admin session cookies are read from the environment, never from this file:
  CTF_SESSIONID, CTF_CSRFTOKEN

Usage:
  python update.py --solves path/to/CTF.xlsx
  python update.py --skip-scrape   # reuse the existing Challenge_Solve_Counts.xlsx
"""
import argparse
import os
import runpy
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
ADMIN_URL = 'https://conan.cote.ws/admin/db/challenge/'

SOLVE_COUNTS_FILE = 'Challenge_Solve_Counts.xlsx'
POINTS_FILE = 'challenges_with_points.xlsx'
NAME_MAP_FILE = 'output.xlsx'
SOLVES_UPDATED_FILE = 'CTF_updated.xlsx'


def step(title):
    print(f"\n=== {title} ===")


def scrape_solve_counts():
    sessionid = os.environ.get('CTF_SESSIONID')
    csrftoken = os.environ.get('CTF_CSRFTOKEN')
    if not sessionid or not csrftoken:
        sys.exit("Set CTF_SESSIONID and CTF_CSRFTOKEN (from a logged-in admin browser session), "
                 "or pass --skip-scrape.")

    response = requests.get(
        ADMIN_URL,
        cookies={'sessionid': sessionid, 'csrftoken': csrftoken},
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'},
        verify=False,
    )
    response.raise_for_status()
    if '/login' in response.url:
        sys.exit("Admin session is not logged in (redirected to login). Refresh CTF_SESSIONID/CTF_CSRFTOKEN.")

    soup = BeautifulSoup(response.text, 'html.parser')
    timestamp = str(int(time.time()))
    data = []
    for idx, row in enumerate(soup.find_all('tr'), start=1):
        cols = row.find_all('td')
        title_cell = row.find('th', class_='field-title')
        if len(cols) < 4 or not title_cell:
            continue
        data.append({
            'web-scraper-order': f'{timestamp}-{idx}',
            'web-scraper-start-url': ADMIN_URL,
            'Title': title_cell.text.strip(),
            'Is over': cols[1].img['alt'],
            'Disable solve notif': cols[2].img['alt'],
            'Solve count': int(cols[3].text.strip()),
        })

    # An empty result would wipe every challenge's points, so stop here instead
    if not data:
        sys.exit("No challenges found on the admin page; the page layout or login may have changed.")

    pd.DataFrame(data).to_excel(SOLVE_COUNTS_FILE, index=False)
    print(f"Scraped {len(data)} challenges -> {SOLVE_COUNTS_FILE}")


def calculate_points(solves):
    if solves <= 1:
        return 500
    return max(500 - (solves - 1) * 50, 50)


def compute_points():
    df = pd.read_excel(SOLVE_COUNTS_FILE)
    df['Points'] = df['Solve count'].apply(calculate_points)
    df.to_excel(POINTS_FILE, index=False)
    print(f"Points for {len(df)} challenges -> {POINTS_FILE}")


def map_ids_to_names(solves_path):
    ctf_df = pd.read_excel(solves_path)
    id_to_name = pd.read_excel(NAME_MAP_FILE).set_index('id')['display_name'].to_dict()
    ctf_df['User'] = ctf_df['User'].map(id_to_name).fillna(ctf_df['User'])
    ctf_df.to_excel(SOLVES_UPDATED_FILE, index=False)
    print(f"{len(ctf_df)} solves, {ctf_df['User'].nunique()} users -> {SOLVES_UPDATED_FILE}")


def run_script(name):
    runpy.run_path(str(BASE_DIR / name), run_name='__main__')


def find_default_solves():
    for candidate in (BASE_DIR / 'CTF.xlsx', BASE_DIR.parent / 'CTF.xlsx'):
        if candidate.exists():
            return candidate
    return None


def main():
    parser = argparse.ArgumentParser(description="Rebuild the CTF scoreboard site.")
    parser.add_argument('--solves', type=Path,
                        help="Solve log export (Challenge, User, Solved time). "
                             "Default: CTF.xlsx in this folder, then in the parent folder.")
    parser.add_argument('--skip-scrape', action='store_true',
                        help=f"Reuse the existing {SOLVE_COUNTS_FILE} instead of scraping.")
    args = parser.parse_args()

    # Resolve the solve log before chdir so relative paths are taken from where the user ran us
    solves_path = args.solves.resolve() if args.solves else find_default_solves()
    if not solves_path or not solves_path.exists():
        sys.exit("Solve log not found. Export it as CTF.xlsx or pass --solves PATH.")

    # The helper scripts use paths relative to the repo folder, and usernames contain
    # characters the Windows console code page can't print
    os.chdir(BASE_DIR)
    sys.stdout.reconfigure(encoding='utf-8')

    step("1. Solve counts")
    if args.skip_scrape:
        if not Path(SOLVE_COUNTS_FILE).exists():
            sys.exit(f"--skip-scrape given but {SOLVE_COUNTS_FILE} does not exist.")
        print(f"Reusing {SOLVE_COUNTS_FILE}")
    else:
        scrape_solve_counts()

    step("2. Challenge points")
    compute_points()

    step("3. Point badges in challenges.html")
    run_script('points.py')

    step("4. Discord name map")
    run_script('excel.py')

    step("5. Ids -> names in solve log")
    map_ids_to_names(solves_path)

    step("6. User totals")
    run_script('rank.py')

    step("7. scoreboard.html")
    run_script('dataconnect.py')

    step("8. User pages")
    run_script('user.py')

    print("\nDone. Review with `git status` / `git diff`, then commit and push.")


if __name__ == '__main__':
    main()
