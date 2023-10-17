from nba_api.stats.static import players
from PIL import Image
import requests
from io import BytesIO
from tqdm import tqdm
from time import sleep

def get_images_players():
  # Get list of ids for every player
  playerId_list = [player['id'] for player in players.get_players()]
  # Loop over NBA.com to get the pngs
  for player in tqdm(playerId_list):
    sleep(0.6)
    url = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player}.png'
    try:
      response = requests.get(url)
      response.raise_for_status()
      img = Image.open(BytesIO(response.content))
      img_info = img.info
      img.save(f'static/images/players_images/{player}.png', **img_info)
    except requests.exceptions.HTTPError as err:
      pass

get_images_players()
