import requests, os

def update():
    try: os.remove('./pokeDB.csv')
    except: pass
    
    pokemon = open("./pokeDB.csv", "w")
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0'}

    pokemon.write('id,name,type1,type2,hp,attack,defense,sp_attack,sp_defense,speed,image,cry\n')
    for i in range(1025):
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i + 1), headers=headers)
        data = response.json()
        
        if response.status_code != 200:
            print(f'response: {response.status_code}')
        
        line = ''
        name = data.get('name')
        pokemon_id = data.get('id')
        image = data.get('sprites')['front_default']
        cry = data.get('cries')['latest']
        stats = [i['base_stat'] for i in data['stats']]
        types = [t['type']['name'] for t in data['types']]
        
        hp, attack, defense, sp_attack, sp_defense, speed = stats
        type1 = types[0]
        try: type2 = types[1]
        except: type2 = ''
        
        line = f'{pokemon_id},{name},{type1},{type2},{hp},{attack},{defense},{sp_attack},{sp_defense},{speed},{image},{cry}'
        print(line)
        pokemon.write(line + '\n')
    
    pokemon.close()

if __name__ == '__main__':
    update()