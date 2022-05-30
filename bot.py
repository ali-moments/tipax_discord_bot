from time import sleep
import requests
import datetime
import tpax_grabber
import logging
from configparser import ConfigParser

today = datetime.datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(level=logging.INFO, filename=f"log_{today}.log", 
format="%(asctime)s:%(levelname)s:%(message)s")
parser = ConfigParser()
parser.read('conf.ini')

def get_time():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    return f"{date}T{time}Z"

ID = parser.get('info', 'id')
url = parser.get('info', 'webhook')
timer= parser.get('time', 'timer')

message = {
    "content": None,
    "embeds": [
      	{
        "title": "اطلاعات بسته",
        "description": "",
        "url": "",
        "color": 7995224,
        "fields": [],
        "author": {
        	"name": "tpax-grabber",
        	"url": "https://github.com/ali-moments",
        	"icon_url": "https://github.com/ali-moments/tipax_discord_bot/blob/main/pictures/logo-tipax.jpg"
        },
        "footer": {
        	"text": "visit ali.ir for more stuff",
          	"icon_url": "https://github.com/ali-moments/tipax_discord_bot/blob/main/pictures/profile.jpg"
        },
        "timestamp": ""
      	}
    ],
    "username": "TPAX",
    "avatar_url": "https://github.com/ali-moments/tipax_discord_bot/blob/main/pictures/logo-tipax.jpg",
    "attachments": []
	}


while True:
    message['embeds'][0]['description'] = tpax_grabber.get_info(ID)
    message['embeds'][0]['fields'] = tpax_grabber.get_state(ID)
    message['embeds'][0]['timestamp'] = get_time()
    message['embeds'][0]['url'] = f"https://tipaxco.com/tracking?id={ID}"
    result = requests.post(url, json = message)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(err)
    else:
        logging.info("Payload delivered successfully, code {}.".format(result.status_code))
    
    time = datetime.datetime.now().strftime("%H:%M:%S")
    logging.info(f"[{time}] sleeping {timer} seconds")
    sleep(int(timer))

