import configparser

config = configparser.ConfigParser()
config.read('api_key.ini')

print(config.sections())
print(config["key"]["claude_key"])
print(config["mail"]["from_account"])
print(config["mail"]["to_account"])
