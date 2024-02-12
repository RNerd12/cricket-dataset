import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

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
    'hi': 'hit wicket'
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
    mainTable = None
    for table in soup.find_all('table'):
        if table.find('thead').find('th', string='BATTING'):
            mainTable = table
            break
    for row in mainTable.find('tbody').find_all('tr'):
        if row.find('a', href=re.compile('[^"]*cricketer[^"]*')) and not row.find('strong', string='Did not bat: '):
            cells = row.find_all('td')
            player_map = pd.DataFrame([{
                'player_id': cells[0].find('a')['href'].split('-')[-1],
                'match_id': match_id,
                'dismissal': reason_map[cells[1].find('span').text[:2]] if cells[1].find('span') else cells[1].text
            }])
            print(player_map)
            dismissals = pd.concat([dismissals,player_map],ignore_index=True)
    time.sleep(0.5)

if __name__ == '__main__':
    for _,row in matches_df.iterrows():
        if row['match_link'] not in matches:
            matches.add(row['match_link'])
            get_match_dismissals(row['match_link'].split('/')[-1][:-5])
    dismissals.to_csv('data/dismissals.csv')