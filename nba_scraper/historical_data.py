from nba_api.stats.endpoints import playergamelogs
from time import sleep
import pandas as pd 

def extract_season_data(seasons_list = ['2023-24']):
  players_game_logs = pd.DataFrame()

  for season in seasons_list:
    sleep(5)
    log_season = (playergamelogs.PlayerGameLogs(season_nullable=season)
                                .player_game_logs
                                .get_data_frame())
    
    players_game_logs = pd.concat([players_game_logs, log_season])

  return players_game_logs


df = extract_season_data(seasons_list = ['2022-23'])

print(df)


