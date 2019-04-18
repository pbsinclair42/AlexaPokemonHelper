import collections
import json

import requests

all_types = list(map(lambda x: x['name'], json.loads(requests.get("https://pokeapi.co/api/v2/type").content)['results']))
all_types.remove("unknown")
all_types.remove("shadow")


def get_types(pokemon):
    pokemon_data = json.loads(requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon).content)
    return list(map(lambda x: x["type"]["name"], pokemon_data["types"]))


def get_type_effectiveness_for_type(type):
    type_data = json.loads(requests.get("https://pokeapi.co/api/v2/type/" + type).content)["damage_relations"]
    weaknesses = {2: list(map(lambda x: x['name'], type_data["double_damage_from"]))}
    resistances = {2: list(map(lambda x: x['name'], type_data["half_damage_from"]))}
    immunities = {2: list(map(lambda x: x['name'], type_data["no_damage_from"]))}
    return {"weaknesses": weaknesses, "resistances": resistances, "immunities": immunities}


def get_type_effectiveness_for_pokemon(pokemon):
    types = get_types(pokemon)
    types = list(map(lambda t: get_type_effectiveness_for_type(t), types))
    if len(types) == 1:
        return types[0]
    multipliers = {t: 1 for t in all_types}
    for type in types:
        for m, ts in type['weaknesses'].items():
            for t in ts:
                multipliers[t] *= m
        for m, ts in type['resistances'].items():
            for t in ts:
                multipliers[t] /= m
        for m, ts in type['immunities'].items():
            for t in ts:
                multipliers[t] *= 0

    weaknesses = collections.defaultdict(list)
    resistances = collections.defaultdict(list)
    immunities = []
    neutral = []
    for t, m in multipliers.items():
        if m == 0:
            immunities.append(t)
        elif m < 1:
            resistances[1 / m].append(t)
        elif m > 1:
            weaknesses[m].append(t)
        else:
            neutral.append(t)
    return {"weaknesses": weaknesses, "resistances": resistances, "immunities": immunities, "neutral": neutral}


def get_weaknesses_for_pokemon(pokemon):
    return get_type_effectiveness_for_pokemon(pokemon)["weaknesses"]