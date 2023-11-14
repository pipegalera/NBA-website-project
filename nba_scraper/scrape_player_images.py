from nba_api.stats.static import players
from PIL import Image
import requests
from io import BytesIO
from tqdm import tqdm
from time import sleep
import os 

def get_images_players(images_path =  'static/images/players_images/'):
  # Get list of ids for every player
  list_all_players = [player['id'] for player in players.get_players()]
  # We do not need to download the images that we already have
  list_players_already_downloaded = [f[:-4] for f in os.listdir(images_path) if f.endswith('.png')]
  list_players_already_downloaded = set(map(int, list_players_already_downloaded))
  players_images_list = [id for id in list_all_players if id not in list_players_already_downloaded]
  # Loop over NBA.com to get the pngs
  for player in tqdm(players_images_list):
    sleep(0.3)
    url = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player}.png'
    try:
      response = requests.get(url)
      response.raise_for_status()
      img = Image.open(BytesIO(response.content))
      img_info = img.info
      img.save(images_path + f'{player}.png', **img_info)
  # If the player do not have image, use fallback image (called '0.png')
    except requests.exceptions.HTTPError as err:
      fallback_img = Image.open(images_path + '0.png')
      fallback_img.save(images_path + f'{player}.png')
get_images_players()
