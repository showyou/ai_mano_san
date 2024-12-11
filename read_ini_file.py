import configparser
import os

config = configparser.ConfigParser()
path = os.path.dirname(os.path.abspath(__file__))
config.read(path+'/api_key.ini')

print(config.sections())
print(config["key"]["claude_key"])
print(config["mail"]["from_account"])
print(config["mail"]["to_account"])
