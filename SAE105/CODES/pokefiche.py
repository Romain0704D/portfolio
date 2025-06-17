
import sys
import requests
import markdown

stats_available = ['abilities',
                   'base_experience',
                   'cries',
                   'forms',
                   'game_indices',
                   'height',
                   'held_items',
                   'id',
                   'is_default',
                   'location_area_encounters',
                   'moves',
                   'name',
                   'order',
                   'past_abilities',
                   'past_types',
                   'species',
                   'sprites',
                   'stats',
                   'types',
                   'weight']

def download_poke(id) -> dict:
    if isinstance(id, str):
        id = id.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    data = requests.get(url)
    data_json = data.json()
    return data_json

def pokedata(id: str, stat: str) -> str:
    data_json = download_poke(id)
    
    if isinstance(stat, str):
        stat = stat.lower()
    
    if isinstance(stat, int):
        if 1 <= stat <= len(stats_available):
            stat = stats_available[stat - 1]
    
    if stat in stats_available :
        
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
        
        elif stat == stats_available[17] :
            stats = {stat_info['stat']['name']: stat_info['base_stat'] for stat_info in data_json[stat]}
            return stats
        
        elif stat == stats_available[18] :
            types = [type_info['type']['name'] for type_info in data_json[stat]]
            return types
        
        return data_json[stat]
        
    print('Error : stat not found')
    print('stats available :')
    
    for i in range(len(stats_available)) :
        print(' (' + str(i + 1) + ') ' + stats_available[i])

def get_pokemon_name_in_french_by_id(pokemon_id: int) -> str:
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    french_name = next(name['name'] for name in data['names'] if name['language']['name'] == 'fr')
    return french_name

def get_pokemon_types_in_french_by_id(pokemon_id: int) -> list:
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    types_in_french = []
    for type_info in data['types']:
        type_url = type_info['type']['url']
        type_response = requests.get(type_url)
        type_response.raise_for_status()
        type_data = type_response.json()
        french_type = next(name['name'] for name in type_data['names'] if name['language']['name'] == 'fr')
        types_in_french.append(french_type)
    return types_in_french

def taille_dm_to_m(taille_dm: int) -> float:
    return taille_dm / 10

def poids_hg_to_kg(poids_hg: int) -> float:
    return poids_hg / 10

def dataset_to_md(fiche: dict, nom_fichier: str = "fiche_pokemon.md") -> str:
    traduction_stats = {
        "hp": "Pv",
        "attack": "Attaque",
        "defense": "Défense",
        "special-attack": "Attaque spéciale",
        "special-defense": "Défense spéciale",
        "speed": "Vitesse"
    }

    nom = fiche.get("nom", "Inconnu")
    taille = fiche.get("taille", "Inconnu")
    poids = fiche.get("poids", "Inconnu")
    types = ", ".join(fiche.get("types", []))
    stats = fiche.get("Statistiques", {})
    sprite = fiche.get("sprite", "")
    
    if stats and isinstance(stats, dict):
        stats_md = "\n".join([
            f"- **{traduction_stats.get(stat, stat.capitalize())}** : {valeur}" 
            for stat, valeur in stats.items()
        ])
    else:
        stats_md = "- Aucune statistique disponible."
    
    markdown_content = f"""
# Fiche Pokémon : {nom}

<img src="{sprite}" alt="Sprite de {nom}" width="150" height="150">

## Informations générales
- **Taille** : {taille}
- **Poids** : {poids}
- **Type(s)** : {types}

## Statistiques
{stats_md}

## Plus d'informations
- [Description complète sur Pokebip](https://www.pokebip.com/pokedex/ecarlate-violet/pokemon/{nom.lower()})

"""

    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        fichier.write(markdown_content.strip())
    
    return nom_fichier

def markdown_to_html(markdown_file: str, html_file: str, pokemon_name: str):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    html_content = markdown.markdown(markdown_content)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fiche de {pokemon_name}</title>
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


def fiche_pokemon(id_fs: int) -> dict:

    nom_fs = get_pokemon_name_in_french_by_id(id_fs)
    poids_fs = poids_hg_to_kg(pokedata(id_fs, 20))
    taille_fs = taille_dm_to_m(pokedata(id_fs, 6))
    types_fs = get_pokemon_types_in_french_by_id(id_fs)
    stats_fs = pokedata(id_fs, 18)
    sprite_fs = pokedata(id_fs, 17)['front_default']

    fiche = {
        'sprite': sprite_fs,
        'nom': nom_fs,
        'types': types_fs,
        'Statistiques': stats_fs,
        'taille': str(taille_fs) + 'm',
        'poids': str(poids_fs) + 'kg'
    }
    
    nom_fichier_md = f"{nom_fs}_fiche.md"
    dataset_to_md(fiche, nom_fichier=nom_fichier_md)
    print(f"Fiche MD générée avec succès : {nom_fichier_md}")
    
    nom_fichier_html = f"{nom_fs}_fiche.html"
    markdown_to_html(nom_fichier_md, nom_fichier_html, nom_fs)
    print(f"Fiche HTML générée avec succès : {nom_fichier_html}")

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python3 pokefiche.py <id_pokemon>")
        sys.exit(1)
    
    try:
        id_pokemon = int(sys.argv[1])
        fiche_pokemon(id_pokemon)
    except ValueError:
        print("Erreur : l'ID du Pokémon doit être un entier valide.")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        sys.exit(1)
