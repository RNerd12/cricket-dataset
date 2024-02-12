import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

search_url = "https://search.espncricinfo.com/ci/content/site/search.html"

def get_player_id(row):
    player = row['player_name']
    params = {'search': player, 'type': 'player'}
    response = requests.get(search_url, params=params, headers={'user-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    player_link = soup.find('a', href=True, string=re.compile(player.split(' ')[-1]))
    time.sleep(1)
    if player_link:
        return player_link['href']
    else:
        print(f'{player}, ')
        return None
if __name__ == '__main__':
    df = pd.read_csv('data/players.csv')
    df['profile'] = None
    df['profile'] = df.apply(get_player_id, axis=1)
    df.to_csv('data/player_profiles.csv')
