
import requests
import markdown
import sys

stats_available = ['abilities', 'base_experience', 'cries', 'forms', 'game_indices', 'height', 'held_items', 'id', 'is_default', 'location_area_encounters', 'moves', 'name', 'order', 'past_abilities', 'past_types', 'species', 'sprites', 'stats', 'types', 'weight']

def get_dataset(id) -> dict:
    if isinstance(id, str):
        id = id.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    data = requests.get(url)
    data_json = data.json()
    return data_json

def pokedata(id: str, stat: str = None) -> str:
    data_json = get_dataset(id)

    if isinstance(stat, str):
        stat = stat.lower()

    if isinstance(stat, int):
        if 1 <= stat <= len(stats_available):
            stat = stats_available[stat - 1]

    if stat in stats_available:
        if stat == stats_available[0]:
            abilities = [ability['ability']['name'] for ability in data_json[stat]]
            return abilities
        elif stat == stats_available[4]:
            games = [game['version']['name'] for game in data_json[stat]]
            return games
        elif stat == stats_available[6]:
            items = [item['item']['name'] for item in data_json[stat]]
            return items
        elif stat == stats_available[10]:
            moves = [move['move']['name'] for move in data_json[stat]]
            return moves
        elif stat == stats_available[17]:
            stats = {stat_info['stat']['name']: stat_info['base_stat'] for stat_info in data_json[stat]}
            return stats
        elif stat == stats_available[18]:
            types = [type_info['type']['name'] for type_info in data_json[stat]]
            return types
        return data_json[stat]

    print('Error: stat not found')
    print('stats available:')
    
    for i in range(len(stats_available)):
        print(' ' + '(' + str(i + 1) + ')' + ' ' + stats_available[i])

def get_pokemon_name_in_french_by_id(pokemon_id: int) -> str:
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    french_name = next(name['name'] for name in data['names'] if name['language']['name'] == 'fr')
    return french_name

def calculate_similarity_between_sets(set1: set, set2: set) -> float:
    common_elements = set1.intersection(set2)
    total_elements = set1.union(set2)
    return (len(common_elements) / len(total_elements)) * 100 if len(total_elements) > 0 else 0

def calculate_average_similarity(pokemon_sets: list) -> float:
    total_pokemon = len(pokemon_sets)
    similarity_percentages = []
    
    for i in range(total_pokemon):
        for j in range(i + 1, total_pokemon):
            similarity = calculate_similarity_between_sets(pokemon_sets[i], pokemon_sets[j])
            similarity_percentages.append(similarity)
    
    if similarity_percentages:
        return sum(similarity_percentages) / len(similarity_percentages)
    return 0

VERSION_GROUP_TO_REGION = {
    "red-blue": "kanto",
    "yellow": "kanto",
    "gold-silver": "johto",
    "crystal": "johto",
    "ruby-sapphire": "hoenn",
    "emerald": "hoenn",
    "fire-red-leaf-green": "kanto",
    "diamond-pearl": "sinnoh",
    "platinum": "sinnoh",
    "heartgold-soulsilver": "johto",
    "black-white": "unova",
    "black-2-white-2": "unova",
    "x-y": "kalos",
    "omega-ruby-alpha-sapphire": "hoenn",
    "sun-moon": "alola",
    "ultra-sun-ultra-moon": "alola",
    "sword-shield": "galar",
    "brilliant-diamond-shining-pearl": "sinnoh",
    "legends-arceus": "hisui",
}

STAT_TRANSLATIONS = {
    'hp': 'Pv',
    'attack': 'Attaque',
    'defense': 'Défense',
    'special-attack': 'Attaque Spéciale',
    'special-defense': 'Défense Spéciale',
    'speed': 'Vitesse',
}

def get_translated_type_name(type_id: int, language: str = "fr") -> str:
    url = f"https://pokeapi.co/api/v2/type/{type_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for language_data in data["names"]:
            if language_data["language"]["name"] == language:
                return language_data["name"]
    return None

def get_translated_ability_name(ability_id: int, language: str = "fr") -> str:
    url = f"https://pokeapi.co/api/v2/ability/{ability_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for language_data in data["names"]:
            if language_data["language"]["name"] == language:
                return language_data["name"]
    return None

def compute_statistics(area_id: int) -> dict:
    url = f"https://pokeapi.co/api/v2/location-area/{area_id}"
    data = requests.get(url).json()

    area_name = data['name']
    pokemon_ids = []
    games_with_regions = {}
    pokemon_names_in_french = []
    all_types = set()
    type_sets = []
    solo_types_count = 0
    double_types_count = 0
    talents_by_pokemon = {}

    for encounter in data.get('pokemon_encounters', []):
        pokemon_id = encounter['pokemon']['url'].split('/')[-2]
        pokemon_ids.append(pokemon_id)
        
        pokemon_name = get_pokemon_name_in_french_by_id(pokemon_id)
        pokemon_names_in_french.append(pokemon_name)

        for version_detail in encounter.get('version_details', []):
            game_name = version_detail['version']['name']
            
            if game_name not in games_with_regions:
                game_url = f"https://pokeapi.co/api/v2/version/{game_name}"
                game_data = requests.get(game_url).json()
                version_group = game_data.get('version_group', {}).get('name', 'unknown')
                region_name = VERSION_GROUP_TO_REGION.get(version_group, 'unknown')
                games_with_regions[game_name] = region_name

        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(pokemon_url).json()
        talents = [ability['ability']['name'] for ability in pokemon_data['abilities']]
        translated_talents = [get_translated_ability_name(ability) for ability in talents]
        talents_by_pokemon[pokemon_name] = translated_talents

    for pokemon_id in pokemon_ids:
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        pokemon_data = requests.get(pokemon_url).json()

        types = set([get_translated_type_name(t['type']['name'], language="fr") for t in pokemon_data['types']])
        type_sets.append(types)
        all_types.update(types)

        if len(types) == 1:
            solo_types_count += 1
        elif len(types) == 2:
            double_types_count += 1

    type_similarity = calculate_average_similarity(type_sets)

    total_pokemon = len(pokemon_ids)
    solo_type_percentage = (solo_types_count / total_pokemon) * 100 if total_pokemon > 0 else 0
    double_type_percentage = (double_types_count / total_pokemon) * 100 if total_pokemon > 0 else 0

    info = {
        'area_name': area_name,
        'games_with_regions': games_with_regions,
        'pokemon_ids_and_names': list(zip(pokemon_ids, pokemon_names_in_french)),
        'pokemon_info': {
            'types': list(all_types),
            'talents': talents_by_pokemon
        },
        'comparison': {
            'type_similarity_percentage': type_similarity,
            'solo_type_percentage': solo_type_percentage,
            'double_type_percentage': double_type_percentage,
        }
    }

    generate_markdown_report(info)

    return info

def generate_markdown_report(info: dict):
    report = f"# Rapport de la zone : {info['area_name']}\n\n"
    
    report += "## Jeux et Régions :\n"
    for game, region in info['games_with_regions'].items():
        report += f"  - {game}: {region}\n"
    
    report += "\n## IDs et noms des Pokémon analysés :\n"
    for pokemon_id, pokemon_name in info['pokemon_ids_and_names']:
        report += f"  - ID: {pokemon_id}, Nom: {pokemon_name}\n"
    
    report += "\n## Types disponibles :\n"
    report += ", ".join(info['pokemon_info']['types']) + "\n"

    report += "\n## Talents des Pokémon :\n"
    for pokemon_name, talents in info['pokemon_info']['talents'].items():
        report += f"  - {pokemon_name} : {', '.join(talents)}\n"
    
    report += "\n## Comparaison des similitudes :\n"
    
    type_similarity = info['comparison'].get('type_similarity_percentage', None)
    solo_type_percentage = info['comparison'].get('solo_type_percentage', None)
    double_type_percentage = info['comparison'].get('double_type_percentage', None)

    report += f"  - Pourcentage de similarité des types : {type_similarity if type_similarity is not None else 0.00:.2f}%\n"
    report += f"  - Pourcentage de types solo : {solo_type_percentage if solo_type_percentage is not None else 0.00:.2f}%\n"
    report += f"  - Pourcentage de types double : {double_type_percentage if double_type_percentage is not None else 0.00:.2f}%\n"

    file_name = f"{info['area_name']}_report.md"
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Fichier MD généré : {file_name}")

def markdown_to_html(markdown_file: str, html_file: str, area_name: str):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    html_content = markdown.markdown(markdown_content)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport pour la zone : {area_name}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                transition: background-color 0.3s, color 0.3s;
            }}
            .dark-mode {{
                background-color: #121212;
                color: white;
            }}
            button {{
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 15px 25px;
                background-color: #56001f;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 16px;
                border-radius: 12px;
                transition: transform 0.2s ease, background-color 0.3s ease;
            }}
            button:hover {{
                background-color: #25000d;
                transform: scale(1.1);
            }}
        </style>
    </head>
    <body>
        <button onclick="toggleDarkMode()">Mode sombre/clair</button>
        <div id="content">
            {html_content}
        </div>
        <script>
            function toggleDarkMode() {{
                document.body.classList.toggle('dark-mode');
            }}
        </script>
    </body>
    </html>
    """

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"Fichier HTML généré : {html_file}")

def start(area_id: int):
    info = compute_statistics(area_id)
    markdown_file = f"{info['area_name']}_report.md"
    generate_markdown_report(info)
    html_file = f"{info['area_name']}_report.html"
    markdown_to_html(markdown_file, html_file, info['area_name'])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python3 pokefiche.py <id_pokemon>")
        sys.exit(1)
    
    try:
        area_id = int(sys.argv[1])
        start(area_id)
    except ValueError:
        print("Erreur : l'ID de la zone doit être un entier valide.")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        sys.exit(1)
