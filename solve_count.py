import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup
url = 'https://conan.cote.ws/admin/db/challenge/'
cookies = {
    'csrftoken': 'ERH0yxUdiZQ7D1e0zw6GWgufcGrIUzx9',
    'sessionid': '1dq5e5yuu9agunvl47hwrzy63n3jh3e6',
}
headers = {
    'Host': 'conan.cote.ws',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Not.A/Brand";v="99", "Chromium";v="136"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'en-US,en;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
}

# Send GET request
response = requests.get(url, headers=headers, cookies=cookies, verify=False)

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr')

# Prepare data
data = []
timestamp = str(int(time.time()))
base_url = 'https://conan.cote.ws/admin/db/challenge/'

for idx, row in enumerate(rows, start=1):
    cols = row.find_all('td')
    if len(cols) >= 4:
        title = row.find('th', class_='field-title').text.strip()
        is_over = cols[1].img['alt']
        disable_notif = cols[2].img['alt']
        solve_count = cols[3].text.strip()
        
        data.append({
            'web-scraper-order': f'{timestamp}-{idx}',
            'web-scraper-start-url': base_url,
            'Title': title,
            'Is over': is_over,
            'Disable solve notif': disable_notif,
            'Solve count': solve_count
        })

# Create Excel
df = pd.DataFrame(data)
df.to_excel('Challenge_Solve_Counts.xlsx', index=False)
print("✅ Data scraped and saved to Challenge_Solve_Counts.xlsx")
