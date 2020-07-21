import urllib.request 
import json

jsonFiles = ['commands', 'sfx_votes']

for file in jsonFiles:

    url = f"https://mygeoangelfirespace.city/db/{file}.json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    with open(f'json/{file}.json', 'r+') as commandsFile:
          commandsFile.seek(0)
          json.dump(data, commandsFile, indent=2)
          commandsFile.close()
          print(f"{file} updated")
