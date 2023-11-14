from nba_api.stats.endpoints import playergamelogs
import numpy as np
import pandas as pd

def scrape_base_game_data(seasons_list: list = ['2023-24']) -> pd.DataFrame:

  df = pd.DataFrame()

  for season in seasons_list:
    log_season = (playergamelogs.PlayerGameLogs(season_nullable=season)
                                .player_game_logs
                                .get_data_frame())
    
    df = pd.concat([df, log_season])

  df = df[['PLAYER_ID', 'PLAYER_NAME',
          'TEAM_NAME', 'TEAM_ABBREVIATION','TEAM_ID',
          'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 
          'PTS', 'AST', 'REB', 'BLK','TOV', ]]
  df['team_home'] = np.where(df.MATCHUP.str.contains(' vs. '),1, 0)

  # Format 
  df['player_game_id'] = df['PLAYER_ID'].astype(str) + df['GAME_ID'].astype(str)
  df.WL.replace({'W':1, 'L': 0},inplace=True)
  df.rename({'WL':'game_win'},axis=1, inplace=True)
  df.columns = df.columns.str.lower()

  return df
