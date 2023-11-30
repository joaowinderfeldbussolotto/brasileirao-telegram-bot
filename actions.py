from os import getenv
from dotenv import load_dotenv
import requests

load_dotenv()
API_ENDPOINT =  getenv('API_URL')

def format_games(data):
    text = ""
    for match in data:
        text += f"{match['home_team']} {match['score']} {match['away_team']}\n"
    return text

def get_live_games():
    api_endpoint = f'{API_ENDPOINT}/api/v1/ao-vivo'
    response = requests.get(api_endpoint)
    data = response.json()
    if response.status_code == 200:
        if not data:
            return "Sem jogos ao vivo agora!"

        games = format_games(data)
        return games
    return "Algo deu errado"
        

def format_standings_table(data):
    formatted_data = """
    **Classificação do Campeonato Brasileiro:**

    {}
    """.format("\n\n".join(
        "{}. **{}**\n   - Posição: {}\n   - Pontos: {}\n   - Jogos: {}".format(
            entry['position'], entry['team'], entry['position'], entry['points'], entry['games_played']
        )
        for entry in data
    ))

    return formatted_data

def get_standings():
    endpoint = f'{API_ENDPOINT}/api/v1/tabela/'
    response = requests.get(endpoint)
    data = response.json()

    if response.status_code == 200:
        standings = format_standings_table(data)
        return standings
    
    return ("Algo deu errado")