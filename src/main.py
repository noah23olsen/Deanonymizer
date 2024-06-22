# main.py
import psycopg2
from dotenv import load_dotenv
import os
import requests

# load environment variables from .env file
load_dotenv()

# constants for the hypixel API
BASE_URL = "https://api.hypixel.net/"
PLAYER_UUID = "0fcdbe40-28e9-43fa-9946-7dc648656e17"  # Faith's UUID


def get_api_key():
    api_key = os.getenv('API-KEY')

    if not api_key:
        raise ValueError("api key was not found in the .env file.")
    return api_key


def make_request():
    headers = {"API-Key": get_api_key()}
    url = f"{BASE_URL}player?uuid={PLAYER_UUID}"
    response = requests.get(url, headers=headers)
    return response


classes = [
    "Spider", "Golem", "Enderman", "Squid", "Dreadlord", "Arcanist",
    "Pirate", "Skeleton", "Zombie", "Spider", "Pigman", "Blaze", "Moleman",
    "Hunter", "Creeper", "Shaman", "Herobrine", "Phoenix", "Werewolf", "Automaton",
    "Assassin", "Cow", "Renegade", "Shark", "Snowman"
]


def print_statistics(response):
    if response.status_code == 200:
        data = response.json()

        display_name = data["player"]["displayname"]
        print(f"Display Name: {display_name}")

        chosen_class = data["player"]["stats"]["Walls3"]["chosen_class"]
        print(f"Chosen class: {chosen_class}")

        counter = 0
        for mw_class in classes:
            if counter >= 5:
                break
            key = f"chosen_skin_{mw_class}"
            value = data["player"]["stats"]["Walls3"][key]
            counter += 1
            print(f"{key}: {value} | {counter}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def add_classes_to_database(class_list):
    connection = None
    cursor = None

    # test connection
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
        )
        cursor = connection.cursor()
        print("database connection successful")

        for class_name in classes:
            cursor.execute(
                'INSERT INTO classes ("class_name") VALUES (%s) ON CONFLICT DO NOTHING',
                (class_name,)
            )
        connection.commit()
        print(f"Classes inserted successfully")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    try:
        response = make_request()
        print_statistics(response)
        # test_database_connection(classes)
    except Exception as e:
        print(f"An error occured: {e}")


main()
