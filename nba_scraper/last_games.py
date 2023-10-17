from nba_api.live.nba.endpoints import scoreboard, boxscore
import pandas as pd 

def get_DataFrame_lastgames() -> pd.DataFrame:
  games = scoreboard.ScoreBoard().games.get_dict()
  # Take only finished games
  games = list(filter(lambda game: game['gameStatusText'] == 'Final', games))
  games_total = pd.DataFrame()

  for game in games:
    gameId = game['gameId']
    gameName = game['homeTeam']['teamName'] + ' vs. ' + game['awayTeam']['teamName']

    players_stats = boxscore.BoxScore(gameId).game.get_dict()

    home_players = pd.json_normalize(players_stats['homeTeam'], record_path =['players'])
    home_players['teamName'] = players_stats['homeTeam']['teamName']
    home_players['teamId'] = players_stats['homeTeam']['teamId']
    home_players['homeTeam'] = 1

    away_players = pd.json_normalize(players_stats['awayTeam'], record_path =['players'])
    away_players['teamName'] = players_stats['awayTeam']['teamName']
    away_players['teamId'] = players_stats['awayTeam']['teamId']
    away_players['homeTeam'] = 0

    game_stats = pd.concat([home_players, away_players])
    game_stats['gameId'] = gameId
    game_stats['gameName'] = gameName
    game_stats['gameTime'] = pd.to_datetime(players_stats['gameTimeLocal'][:10])
    games_total = pd.concat([games_total, game_stats])
    games_total['personGameId'] = games_total['personId'].astype(str) + '_' + games_total['gameId'].astype(str)

  # Filter columns 
  columns_to_filter = ['personGameId', 'status', 
                       'name', 'personId', 
                       'teamName', 'teamId',
                       'gameName', 'gameId', 'gameTime', 
                       'statistics.points', 
                       'statistics.assists', 
                       'statistics.reboundsTotal',
                       'statistics.blocks',
                       'statistics.turnovers',
                       ]
  games_total = games_total.filter(items = columns_to_filter)
  games_total = games_total.rename({'statistics.points': 'points', 
                                    'statistics.assists':'assists', 
                                    'statistics.reboundsTotal':'rebounds',
                                    'statistics.blocks':'blocks',
                                    'statistics.turnovers':'turnovers',}, axis=1)
  try:
    games_total.set_index('personGameId', inplace=True)
  except:
    print('No games finished today yet')

  return games_total