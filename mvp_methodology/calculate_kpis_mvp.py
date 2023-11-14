
import pandas as pd
import numpy as np

# Function for calculating "top_player" field (MVP) based on 1 metric
def create_field_top_player(df: pd.DataFrame, metric:str = 'pts'):
  # Create condition to select top_player based on 'metric' (default = points)
  cond_top_player = df.groupby(['game_id', 'team_id'])[metric].transform(max) == df[metric]
  list_top_players = df.loc[cond_top_player].sort_values(['game_id', 'game_date'], ascending=False).index.to_list()

  # Create field
  mask = df.index.isin(list_top_players)
  df['top_player'] = np.where(mask, 1, 0)

  return df