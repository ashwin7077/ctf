# Attack On Hash Function — CTF Scoreboard

Static website for the AOHF Discord CTF, served by GitHub Pages at **https://discord.aohf.team** (see `CNAME`).

There is no backend. Solve data is exported from the CTF platform, turned into HTML by Python scripts on your machine, then committed and pushed.

## Pages

| File | What it is |
|---|---|
| `index.html` | Landing page with links to Discord, challenges and scoreboard. Loads `alert.js` (Discord invite popup). |
| `challenges.html` | All challenges by category. Flags are checked in the browser against a SHA-256 hash. |
| `scoreboard.html` | Ranked players plus a top-10 bar chart (Chart.js). |
| `user/<name>/challenges.html` | Solved and unsolved challenges for each player. |
| `theme.css` | Shared styles for `scoreboard.html` and `challenges.html`. |

## Updating the scoreboard

### Requirements

```
pip install pandas openpyxl requests beautifulsoup4
```

### Inputs

1. **Solve log**: export from the CTF platform as `CTF.xlsx` with the columns `Challenge`, `User` and `Solved time`. `User` may be a Discord ID; IDs are swapped for names using `output.xlsx`.
2. **Admin session cookies**: log in to the CTF admin panel in a browser and copy the `sessionid` and `csrftoken` cookies. They are used to scrape per-challenge solve counts.

### Run

```powershell
$env:CTF_SESSIONID = "<sessionid cookie>"
$env:CTF_CSRFTOKEN = "<csrftoken cookie>"
python update.py --solves path\to\CTF.xlsx
```

If `--solves` is omitted, `update.py` looks for `CTF.xlsx` in this folder, then in the parent folder.

To reuse the last scraped solve counts instead of scraping again:

```
python update.py --skip-scrape --solves path\to\CTF.xlsx
```

Then review and publish:

```
git status
git diff
git add -A
git commit -m "Updated Scoreboard"
git push
```

### What `update.py` does

| Step | Output |
|---|---|
| 1. Scrape solve counts from the admin panel | `Challenge_Solve_Counts.xlsx` |
| 2. Calculate challenge points | `challenges_with_points.xlsx` |
| 3. Write point badges into the challenge page (`points.py`) | `challenges.html` |
| 4. Add new Discord members from `members.json` to the name map (`excel.py`) | `output.xlsx` |
| 5. Replace Discord IDs in the solve log with names | `CTF_updated.xlsx` |
| 6. Total points per player (`rank.py`) | `user_total_points.xlsx` |
| 7. Rebuild the scoreboard table and chart (`dataconnect.py`) | `scoreboard.html` |
| 8. Rebuild each player's page (`user.py`) | `user/<name>/challenges.html` |

If the admin session has expired or the scrape finds no challenges, the script stops before changing any file.

### Scoring

Points are dynamic and depend on how many players solved a challenge:

```
points = max(500 - 50 × (solves - 1), 50)
```

0 or 1 solve = 500 points, 2 = 450, 3 = 400 … down to a minimum of 50. A player's score is the sum of the current points of every challenge they solved, so scores can drop as more people solve the same challenges.

## Adding a challenge

```
python add_challenges.py
```

The script asks for the name, description, attachment link, difficulty, flag format, real flag and category. It stores only the SHA-256 hash of the flag and inserts the challenge card into `challenges.html`. Run `update.py` afterwards to give it points.

Flags are checked in the browser, so anyone can try to brute-force a hash offline. Use long, random flags.

## Other files

| File | Purpose |
|---|---|
| `members.json`, `all_data.json` | Discord member lists (`username`, `userId`). |
| `output.xlsx` | Discord ID → display name map (`id`, `display_name`). |
| `automate.py` | Older scoreboard generator, replaced by `dataconnect.py`. |
| `solve_count.py`, `challenge_points.py`, `userid_to_name.py` | Old individual steps, now built into `update.py`. |
| `web/` | Unrelated side pages. |

## Security

Never put session cookies in the code. `update.py` reads them only from the `CTF_SESSIONID` and `CTF_CSRFTOKEN` environment variables.
