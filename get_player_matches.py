import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

players = pd.read_csv('player_ids.csv')
batter_matches = pd.DataFrame(
    columns=['player_id','player_name','position','country','opposition','runs','dismissal','ground','date','match_link']
)
bowler_matches = pd.DataFrame(
    columns=['player_id','player_name','position','country','opposition','overs','runs','wickets','ground','date','match_link']
)
base_url = 'https://www.espncricinfo.com'

def get_batter_matches(Row):
    global batter_matches
    res = requests.get(
        f'https://stats.espncricinfo.com/ci/engine/player/{Row["player_id"]}.html?class=3;spanmax1=31+Dec+2100;spanmin1=01+Jan+2001;spanval1=span;template=results;type=batting;view=match',
        headers={'user-agent': 'Mozilla/5.0'}
    )
    soup =  BeautifulSoup(res.text,'html.parser')
    tables = soup.findAll('table', class_='engineTable')
    for table in tables:
        if table.find('caption', string='Match by match list'):
            mainTable = table
            break
    if  mainTable.find('b',string='No records available to match this query'):
        print(f'batting table not found for {Row["player_name"]}')
        return
    for row in mainTable.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if cells[1].text.isnumeric():
            row_data = pd.DataFrame([{
                'player_id':Row['player_id'],
                'player_name':Row['player_name'],
                'country':Row['country'],
                'position':Row['type'],
                'opposition':cells[7].find('a').text,
                'runs':cells[1].text,
                'dismissal':'',
                'ground':cells[8].find('a').text,
                'date':cells[9].find('b').text,
                'match_link':base_url+cells[10].find('a')['href']
            }])
            batter_matches = pd.concat([batter_matches, row_data], ignore_index=True)
    print(f'attached batter matches for {Row["player_name"]}')
    time.sleep(0.5)

def get_bowler_matches(Row):
    global bowler_matches
    res = requests.get(
        f'https://stats.espncricinfo.com/ci/engine/player/{Row["player_id"]}.html?class=3;spanmax1=31+Dec+2100;spanmin1=01+Jan+2001;spanval1=span;template=results;type=bowling;view=match',
        headers={'user-agent': 'Mozilla/5.0'}
    )
    soup =  BeautifulSoup(res.text,'html.parser')
    tables = soup.findAll('table', class_='engineTable')
    for table in tables:
        if table.find('caption', string='Match by match list'):
            mainTable = table
            break
    if mainTable.find('b',string='No records available to match this query'):
        print(f'bwoling table not found for {Row["player_name"]}')
        return
    for row in mainTable.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if cells[2].text.isnumeric():
            row_data = pd.DataFrame([{
                'player_id':Row['player_id'],
                'player_name':Row['player_name'],
                'country':Row['country'],
                'position':Row['type'],
                'opposition':cells[8].find('a').text,
                'overs':cells[0].text,
                'runs':cells[2].text,
                'wickets':cells[3].text,
                'ground':cells[9].find('a').text,
                'date':cells[10].find('b').text,
                'match_link':base_url+cells[11].find('a')['href']
            }])
            bowler_matches = pd.concat([bowler_matches, row_data], ignore_index=True)
    print(f'attached bowler matches for {Row["player_name"]}')
    time.sleep(0.5)

if __name__ == '__main__':
    for _,row in players.iterrows():
        if row['type'] in ['Batter', 'All Rounder', 'All rounder']:
            get_batter_matches(row)
        if row['type'] in ['Bowler', 'All Rounder', 'All rounder']:
            get_bowler_matches(row)
    batter_matches.to_csv('international_batter_info.csv')
    bowler_matches.to_csv('international_bowler_info.csv')
