import json
import re
from pprint import pprint

def json_load(path: str) -> dict:
    with open(path, 'r') as file:
        return json.load(file)
    

def load_prefs() -> dict:
    return json_load('preferences.json')


def change_prefs(key: str, value) -> None:
    with open('preferences.json', 'rw') as file:
        content = json.load(file)
        content[key] = value
        file.write(content)


def normalise_markup(html: str) -> str:
    """
    Takes full html string and converts newrecruit-specific marking 
    symbols to readbale html
    """

    # Keywords first (^^...^^ inside)
    text: str = re.sub(r'\^\^([^\^]+)\^\^', r'<span class="keyword">\1</span>', html)
    # Bold (**...**)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
    
    return text

def bundle_css(html_path: str, css_path: str) -> None:
    """Function that takes a css file that was previously linked by href and 
    explicitly puts it into the html file into <style> tag so that we can 
    double-click open it"""
    
    with open(html_path, "r", encoding="utf-8") as html_file:
        html = html_file.read()

    with open(css_path, "r", encoding="utf-8") as css_file:
        css = css_file.read()

    html = re.sub(
        r'<link\s+rel="stylesheet"\s+href="[^"]*"\s*/?>',
        f"<style>\n{css}\n</style>",
        html,
        count=1
    )

    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html)


def sort_units_fields(units: list) -> list:
    """Takes the unit list and sorts the respective fields in them to 
    normalise the output.
    For now, does:
    the primary category will always be the primary one"""

    # Primary category sort
    for unit in units:
        categories: list = unit['categories']
        categories.sort(key=lambda x: x['primary'], reverse=True)

    return units


def find_unit_weapons(unit: dict, ranged: bool) -> list[dict]:
    """
    CAREFUL: doesnt return full weapon object, only its profile
    """
    output = []

    if unit['type'] == 'unit':
        # Iterate through selections' (models') weapon loadout
        for selection in unit['selections']:
            for weapon in selection['selections']:
                if ('profiles' not in weapon.keys() 
                or 'weapon' not in weapon['profiles'][0]['typeName'].lower()):
                    continue

                for profile in weapon['profiles']:
                    if (profile['typeName'] == 'Ranged Weapons' and ranged
                    or profile['typeName'] == 'Melee Weapons' and not ranged):
                        profile['number'] = weapon['number']
                        output.append(profile)

    elif unit['type'] == 'model':
        # Just take model's weapons
        for weapon in unit['selections']:
            if ('profiles' not in weapon.keys() 
                or 'weapon' not in weapon['profiles'][0]['typeName'].lower()):
                
                #  Fragile workaround! If facing problems, rewrite
                if 'selections' in weapon.keys():
                    weapon = weapon['selections'][0]
                else:
                    continue
            
            for profile in weapon['profiles']:
                if (profile['typeName'] == 'Ranged Weapons' and ranged
                    or profile['typeName'] == 'Melee Weapons' and not ranged):
                    profile['number'] = weapon['number']
                    output.append(profile)

    # Combining same positions into one with a bigger number
    merged = []

    for weapon in output:
        name = weapon.get("name")
        chars = weapon.get("characteristics", [])
        number = weapon.get("number", 1)

        found = False
        for existing in merged:
            if (
                existing.get("name") == name and
                existing.get("characteristics") == chars
            ):
                existing["number"] = existing.get("number", 1) + number
                found = True
                break

        if not found:
            merged.append(weapon.copy())

    
    return merged



def find_units(json_roster: dict) -> list:
    selections = json_roster['forces'][0]['selections']
    output = []

    for selection in selections:
        try:
            if selection['type'].lower() in ('unit', 'model'):
                output.append(selection)
        except KeyError:
            continue

    for unit in output:
        unit_ranged_weapons: list = find_unit_weapons(unit, True)
        unit_melee_weapons: list = find_unit_weapons(unit, False)

        unit['ranged_choices'] = unit_ranged_weapons
        unit['melee_choices'] = unit_melee_weapons
    
        # Get extra abilities for separate tables
        ignored_types = {"Unit", "Melee Weapons", "Ranged Weapons"}
        unit['extra_tables'] = {}

        for profile in unit.get("profiles", []):
            type_name = profile.get("typeName")
            if type_name and type_name not in ignored_types:
                unit['extra_tables'].setdefault(type_name, []).append(profile)

    sort_units_fields(output)

    return output


def find_rules(units: list) -> dict[str, tuple[str, str]]:
    output = {}

    for unit in units:
        # try:
        rules = unit['rules']

        for selection in unit['selections']:
            try:
                rules.extend(selection['rules'])
            except KeyError:
                continue

        for rule in rules:
            output[rule['id']] = (rule['name'], rule['description'])
        # except KeyError:
        #     continue
    
    return output


