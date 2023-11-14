import sys

PATH = '/Users/pipegalera/Documents/GitHub/NBA-website-project'
sys.path.insert(0, PATH)

# Custom functions
from nba_scraper.scrape_base_game_data import scrape_base_game_data
from mvp_methodology.calculate_kpis_mvp import create_field_top_player
from mysql_SDK import aws_engine, get_current_games_aws, update_table


if __name__ == "__main__":
  # Load base game data
  df_input = scrape_base_game_data().set_index('player_game_id')
  # Create the field "top_player"
  df_output = create_field_top_player(df_input)
  # Create  an engine 
  engine = aws_engine()
  # Get the current games already in the DB, to not overide them
  list_current_games = get_current_games_aws(engine)
  # Update the gamestats table
  update_table(df_output, 'gamestats', list_current_games)