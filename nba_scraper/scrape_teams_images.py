from nba_api.stats.static import teams
from PIL import Image
import requests
from io import BytesIO
from tqdm import tqdm
from time import sleep
from nba_api.stats.static import teams


def get_images_teams():
  teamId_list = [team['id'] for team in teams.get_teams()]
  for team in tqdm(teamId_list):
    sleep(0.6)
    url = f'https://cdn.nba.com/logos/nba/{team}/global/L/logo.svg'
    response = requests.get(url).text
    with open(f'static/images/teams_images/{team}.svg', 'w') as file:
        file.write(response)

get_images_teams()