import pandas as pd
import json 
from sqlmodel import create_engine, Session
import sys

PATH = '/Users/pipegalera/Documents/GitHub/NBA-website-project'
sys.path.insert(0, PATH)

def aws_engine():
  open_creds = open(PATH + '/sql/credentials_aws.json')
  creds = json.load(open_creds)

  username = creds['username']
  password = creds['password']
  server = creds['server']
  host = creds['host']
  database = creds['database']

  connection_string = f'mysql://{username}:{password}@{server}:{host}/{database}'
  engine = create_engine(connection_string)

  return engine

def get_current_games_aws(engine) -> list:
  # Get all current games 
  with Session(engine) as session:
    dist_games = 'select distinct game_id from gamestats'
    results = session.exec(dist_games).mappings().all()

  # Store as list
  current_games_aws = []
  for i in range(0,len(results)): 
    current_games_aws.append(results[i]['game_id'])
  # Create a print statement
  print('There are currently', len(current_games_aws), 'in the AWS DB')
  print('-------------------------------------')
  return current_games_aws

def update_table(df_output: pd.DataFrame, 
                     table: str,
                     list_current_games: list):

  # We only update the games we do not have already
  df = df_output[~(df_output['game_id'].isin(list_current_games))]

  if len(df) > 0:
      df.to_sql(name=table, con= aws_engine(),if_exists='append')

      # Create a print statement
      df['match_info'] = df['matchup'].str.replace('vs.', '@', regex=False) + ' , ' + df['game_date'].str[:10]
      return [print('   Players stats added for the game', match) for match in df['match_info'].unique()]

  return print('No games to be added')


def get_data_aws(query):
  engine = aws_engine()
  with Session(engine) as session:
    results = session.exec(query).mappings().all()
    return results
