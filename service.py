import json
from pprint import pprint

def json_load(path: str):
    with open(path, 'r') as file:
        return json.load(file)
    

def bundle_css(html_path: str, css_path: str) -> None:
    """Function that takes a css file that was previously linked by href and 
    explicitly puts it into the html file into <style> tag so that we can 
    double-click open it"""
    
    with open(html_path, "r", encoding="utf-8") as html_file:
        html = html_file.read()

    with open(css_path, "r", encoding="utf-8") as css_file:
        css = css_file.read()

    # Replace the <link> tag with inline <style>
    import re
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
    output = []

    if unit['type'] == 'unit':
        # Iterate through selections' (models') weapon loadout
        for selection in unit['selections']:
            for weapon in selection['selections']:
                if (weapon['profiles'][0]['typeName'] == 'Ranged Weapons' and ranged
                or weapon['profiles'][0]['typeName'] == 'Melee Weapons' and not ranged):
                    output.append(weapon)
    elif unit['type'] == 'model':
        # Just take model's weapons
        for weapon in unit['selections']:
            if (weapon['profiles'][0]['typeName'] == 'Ranged Weapons' and ranged
                or weapon['profiles'][0]['typeName'] == 'Melee Weapons' and not ranged):
                    output.append(weapon)
    
    return output



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


