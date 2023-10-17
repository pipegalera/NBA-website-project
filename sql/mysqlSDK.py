import pandas as pd
from sqlmodel import create_engine, Session
from datetime import datetime
from sqlalchemy.dialects.mysql import insert
import numpy as np 

# adding nba_scraper folder
import sys
PATH = '/Users/pipegalera/Documents/GitHub/NBA-website-project'
sys.path.insert(0, PATH)
import nba_scraper.last_games as last_games
from credentials_aws import admin_info

def aws_engine(admin_info: dict = admin_info, echo=True):

  sql_admin_info = admin_info.copy()

  username = sql_admin_info['username']
  password = sql_admin_info['password']
  server = sql_admin_info['server']
  host = sql_admin_info['host']
  database = sql_admin_info['database']

  connection_string = f'mysql://{username}:{password}@{server}:{host}/{database}'
  engine = create_engine(connection_string)

  return engine

def insert_on_duplicate(table, conn, keys, data_iter):
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
    conn.execute(on_duplicate_key_stmt)

def add_to_table_aws(lastgames: pd.DataFrame, table: str):
  df = lastgames.copy()  
  # Only add games if there is any info to be added
  if len(df) > 0:
    df.to_sql(table, 
                con = aws_engine(), 
                if_exists='append', 
                method=insert_on_duplicate)
    
    for date in df['gameTime'].astype(str).unique():
      print('Games date added', date) 
    for game in df['gameName'].unique():
      print('  Players stats added for the game: ', game)
  else:
     print('No data to be added, please check the DataFrame')
     return None

def get_data_aws(query):
  engine = aws_engine()
  with Session(engine) as session:
    results = session.exec(query).mappings().all()
    return results

def create_field_top_player(df: pd.DataFrame, metric:str = 'points'):
  # Create condition to select top_player based on 'metric' (default = points)
  cond_top_player = df.groupby(['gameId', 'teamName'])[metric].transform(max) == df[metric]
  list_top_players = df.loc[cond_top_player].sort_values(['gameId', 'gameTime'], ascending=False).index.to_list()

  # Create field
  mask = df.index.isin(list_top_players)
  df['top_player'] = np.where(mask, 1, 0)

  return df