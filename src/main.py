# main.py
from dotenv import load_dotenv
import os
import requests

load_dotenv()

baseURL = "https://api.hypixel.net/"
playerUUID = "0fcdbe40-28e9-43fa-9946-7dc648656e17"  # Faiths
apiKey = os.getenv('API-KEY')
print(apiKey)

headers = {
    "API-Key": apiKey
}
url = f"{baseURL}player?uuid={playerUUID}"
response = requests.get(url, headers=headers)

if response.status_code == 200:

    data = response.json()

    display_name = data["player"]["displayname"]
    print(f"Display Name: {display_name}")

    #last_login =

    chosen_class = data["player"]["stats"]["Walls3"]["chosen_class"]
    print(f"Chosen class: {chosen_class}")

    skins = [
             "Spider", "Golem", "Enderman", "Squid", "Dreadlord", "Arcanist",
             "Pirate", "Skeleton", "Zombie", "Spider", "Pigman", "Blaze", "Moleman",
             "Hunter", "Creeper", "Shaman", "Herobrine", "Phoenix", "Werewolf", "Automaton",
             "Assassin", "Cow", "Renegade", "Shark", "Snowman"
             ]

    for skin in skins:
        key = f"chosen_skin_{skin}"
        value = data["player"]["stats"]["Walls3"][key]
        print(f"{key}: {value}")
else:
    print(f"Error: {response.status_code}, {response.text}")
