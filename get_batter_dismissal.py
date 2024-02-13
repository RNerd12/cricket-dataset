import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from tqdm import tqdm

reason_map = {
    'c ': 'caught',
    'b ': 'bowled',
    ' b': 'bowled',
    ' c': 'caught',
    'st': 'stumped',
    'lb': 'lbw',
    'no': 'not out',
    'ru': 'run out',
    're': 'retired',
    'hi': 'hit wicket',
    'ob': 'obstructing'
}
dismissals = pd.DataFrame(columns=['player_id','match_id','dismissal'])
matches_df = pd.read_csv('data/international_batter_info.csv')
matches = set()

def get_match_dismissals(match_id):
    global dismissals
    res = requests.get(
        f'https://www.espncricinfo.com/ci/engine/match/{match_id}.html',
        headers={'user-agent': 'Mozilla/5.0'}
    )
    soup = BeautifulSoup(res.text,'html.parser')
    mainTables = []
    for table in soup.find_all('table'):
        if table.find('thead') and table.find('thead').find('th', string='BATTING'):
            mainTables.append(table)
    for mainTable in mainTables:
        for row in mainTable.find('tbody').find_all('tr'):
            if row.find('a', href=re.compile('[^"]*cricketer[^"]*')) and not row.find('strong', string='Did not bat: '):
                cells = row.find_all('td')
                player_map = pd.DataFrame([{
                    'player_id': cells[0].find('a')['href'].split('-')[-1],
                    'match_id': match_id,
                    'dismissal': reason_map[cells[1].find('span').text[:2]] if cells[1].find('span') else cells[1].text
                }])
                dismissals = pd.concat([dismissals,player_map],ignore_index=True)
    time.sleep(0.5)

if __name__ == '__main__':
    total = len(matches_df)
    count = 0
    for _,row in matches_df.iterrows():
        count += 1
        if row['match_link'] not in matches:
            matches.add(row['match_link'])
            get_match_dismissals(row['match_link'].split('/')[-1][:-5])
        if count%10 == 0:
            print(f'completed {count}/{total}')
    dismissals.to_csv('all_dismissals.csv')