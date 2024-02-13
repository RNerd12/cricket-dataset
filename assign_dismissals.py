import pandas as pd

batter_info = pd.read_csv('data/international_batter_info.csv')
dismissals = pd.read_csv('data/dismissals.csv') 
dismissals.set_index(['player_id','match_id'], inplace=True)
batter_info.drop('Unnamed: 0',axis=1,inplace=True)

def query_df(player_id,match_id):
    try:
        return dismissals.loc[(player_id,match_id)]['dismissal']
    except KeyError:
        return None
    
def assign_dismissal(row):
    player_id = row['player_id']
    match_id =  int(row['match_link'].split('/')[-1][:-5])
    print(player_id,match_id)
    row['dismissal'] = query_df(player_id,match_id)
    return row

batter_info = batter_info.apply(assign_dismissal, axis=1)
batter_info.to_csv('international_batter_info_all.csv')