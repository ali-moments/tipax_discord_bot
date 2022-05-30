from configparser import ConfigParser
config = ConfigParser()

config['info'] = {
    "id": "",
    "webhook": ""
}

config['time'] = {
    "timer": "7200"
}

with open('conf.ini', 'w') as f:
    config.write(f)