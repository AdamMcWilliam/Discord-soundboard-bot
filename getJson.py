import urllib.request 
import json

url = "https://mygeoangelfirespace.city/db/commands.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

with open('json/commands.json', 'r+') as commandsFile:
      commandsFile.seek(0)
      json.dump(data, commandsFile, indent=2)
      commandsFile.close()
      print("commands updated")

