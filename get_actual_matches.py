import pandas as pd
import requests
import time

df1 = pd.read_csv('data/match_links.csv')
cities = set()
df2 = pd.DataFrame(columns=['city','match_link','actual_link'])
for _,row in df1.iterrows():
    if row['city'] not in cities:
        cities.add(row['city'])
        res = requests.get(
            row['match_link'],
            headers={'user-agent': 'Mozilla/5.0'}
        )
        append_row = pd.DataFrame([{
            'city': row['city'],
            'match_link': row['match_link'],
            'actual_link': str(res.url).replace('full-scorecard','live-cricket-score')
        }])
        df2 = pd.concat([df2,append_row],ignore_index=True)        
        print(f'got link for {row["city"]}')
        time.sleep(1)

df2.to_csv('actual_links.csv')