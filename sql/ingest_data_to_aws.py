
import sys
# adding nba_scraper folder
PATH = '/Users/pipegalera/Documents/GitHub/NBA-website-project'
sys.path.insert(0, PATH)

# Local modules
from nba_scraper.last_games import get_DataFrame_lastgames
from mysqlSDK import aws_engine, add_to_table_aws, get_data_aws, create_field_top_player
import pandas as pd


# Load the data we need
df = pd.DataFrame(get_data_aws('select * from gamestats')).set_index('personGameId')

# Create the field "top_player"
df_to_be_updated = create_field_top_player(df)

# Submit to AWS
TABLE_NAME = 'gamestats'
add_to_table_aws(df_to_be_updated, TABLE_NAME)
