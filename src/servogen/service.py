import json
from appdirs import user_data_dir
import re
from collections import Counter
import importlib.resources


def json_load(path: str) -> dict:
    with open(path, 'r') as file:
        return json.load(file)


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

def bundle_css(html_path: str, base_css: str, theme_css: str) -> None:
    """Function that takes a css file that was previously linked by href and 
    explicitly puts it into the html file into <style> tag so that we can 
    double-click open it"""

    # Read base CSS
    base_css_content = importlib.resources.read_text('servogen', base_css)
    
    theme_css_content = ''
    if theme_css != '':
        theme_css_content = importlib.resources.read_text('servogen', theme_css)

    combined_css = f"<style>\n{base_css_content}\n{theme_css_content}\n</style>"

    with open(html_path, "r", encoding="utf-8") as html_file:
        html = html_file.read()

    html = re.sub(
        r'<link\s+rel="stylesheet"\s+href="[^"]*"\s*/?>',
        combined_css,
        html,
        count=1
    )

    # Write back the modified HTML
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


def find_faction_rule(roster: dict) -> tuple[str, str]:
    force = roster['forces'][0]

    faction_name = None
    for unit in force.get("selections", []):
        for cat in unit.get("categories", []):
            if cat["name"].startswith("Faction: "):
                faction_name = cat["name"].replace("Faction: ", "")
                break
        if faction_name:
            break

    if not faction_name:
        return ("Unknown", "Faction not found in unit categories")

    rules = []
    for unit in force.get("selections", []):
        categories = [c["name"] for c in unit.get("categories", [])]
        if f"Faction: {faction_name}" in categories:
            for rule in unit.get("rules", []):
                rules.append((rule["name"], rule["description"]))
            # Also check immediate children (1 level deep)
            for child in unit.get("selections", []):
                for rule in child.get("rules", []):
                    rules.append((rule["name"], rule["description"]))

    if not rules:
        return ("Unknown", f"No faction rules found for '{faction_name}'")

    most_common, _ = Counter(rules).most_common(1)[0]
    return most_common


def find_keywords(weapon: dict, profile: dict) -> list[tuple[str, dict]]:
    weapon_rules = weapon.get('rules', [])

    if len(weapon_rules) < 1:
        return []

    keywrods_char: dict = profile['characteristics'][-1]

    output: list = []
    
    for rule in weapon_rules:
        for keyword in keywrods_char['$text'].split(','):
            if rule['name'].lower() in keyword.lower():
                output.append((keyword, rule))
                break
    
    return output


def find_unit_weapons(unit: dict, ranged: bool) -> list[dict]:
    """
    CAREFUL: doesnt return full weapon object, only its profile + rules
    """
    output = []

    if unit['type'] == 'unit':
        # Iterate through selections' (models') weapon loadout
        model_selections = unit.get('selections', [])
        for selection in model_selections:
            weapon_selections = selection.get('selections', [])
            for weapon in weapon_selections:
                if ('profiles' not in weapon.keys() 
                or 'weapon' not in weapon['profiles'][0]['typeName'].lower()):
                    continue

                for profile in weapon['profiles']:
                    if (profile['typeName'] == 'Ranged Weapons' and ranged
                    or profile['typeName'] == 'Melee Weapons' and not ranged):
                        if 'number' in weapon.keys():
                            profile['number'] = weapon['number']
                        else:
                            profile['number'] = 1
                        profile['rules'] = find_keywords(weapon, profile)
                        output.append(profile)

    elif unit['type'] == 'model':
        # Just take model's weapons
        selections = unit.get('selections', [])
        for weapon in selections:
            nested_weapons = []
            if ('profiles' not in weapon.keys() 
                or 'weapon' not in weapon['profiles'][0]['typeName'].lower()):
                
                # If a 'weapon' is several weapons (e.g. 'Dreadnought Combat Weapon w/ Storm Bolter')
                if 'selections' in weapon.keys():
                    nested_weapons = weapon['selections']
                else:
                    continue
            
            if len(nested_weapons) > 0:
                for weapon_i in nested_weapons:
                    for profile in weapon_i['profiles']:
                        if (profile['typeName'] == 'Ranged Weapons' and ranged
                            or profile['typeName'] == 'Melee Weapons' and not ranged):
                            if 'number' in weapon.keys():
                                profile['number'] = weapon['number']
                            else:
                                profile['number'] = 1
                            profile['rules'] = find_keywords(weapon, profile)
                            output.append(profile)
            else:
                for profile in weapon['profiles']:
                    if (profile['typeName'] == 'Ranged Weapons' and ranged
                        or profile['typeName'] == 'Melee Weapons' and not ranged):
                        if 'number' in weapon.keys():
                            profile['number'] = weapon['number']
                        else:
                            profile['number'] = 1
                        profile['rules'] = find_keywords(weapon, profile)
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
        # Adding custom fields
        unit_ranged_weapons: list = find_unit_weapons(unit, True)
        unit_melee_weapons: list = find_unit_weapons(unit, False)

        unit['ranged_choices'] = unit_ranged_weapons
        unit['melee_choices'] = unit_melee_weapons

        unit_profiles: list = find_profiles(unit)
        unit['char_profiles'] = unit_profiles
    
        # Get extra abilities for separate tables
        ignored_types = {"Unit", "Melee Weapons", "Ranged Weapons"}
        unit['extra_tables'] = {}

        for profile in unit.get("profiles", []):
            type_name = profile.get("typeName")
            if type_name and type_name not in ignored_types:
                unit['extra_tables'].setdefault(type_name, []).append(profile)

    sort_units_fields(output)

    return output


def find_rules(units: list[dict]) -> dict[str, tuple[str, str]]:
    output = {}

    def extract_rules(entry: dict):
        for rule in entry.get("rules", []):
            output[rule["id"]] = (rule["name"], rule["description"])

        for sub in entry.get("selections", []):
            extract_rules(sub)

    for unit in units:
        extract_rules(unit)
    
    return output


def find_profiles(unit: dict, is_recursion=False) -> list[dict]:
    output: list[dict] = []

    if unit['type'] == 'model' and not is_recursion:
        for profile in unit['profiles']:
            if profile['typeName'] == 'Unit':
                output.append(profile)
    elif is_recursion or unit['type'] == 'unit':
        # Recurse first through all selections
        for selection in unit.get('selections', []):
            output.extend(find_profiles(selection, is_recursion=True))
        
        # After recursion, collect any direct profiles at this level
        for profile in unit.get('profiles', []):
            if profile.get('typeName') == 'Unit':
                output.append(profile)

    # Combining same positions into one
    merged = []

    for profile in output:
        name = profile.get("name")
        chars = profile.get("characteristics", [])

        def compare_chars(char1: list, char2: list) -> bool:

            def find_char_line(char_list: list, name: str) -> dict:
                for line in char_list:
                    if line['name'] == name:
                        return line
                return {}
            
            for name in ('M', 'T', 'SV', 'W', 'LD', 'OC'):
                char1_line = find_char_line(char1, name)
                char2_line = find_char_line(char2, name)

                if char1_line.get('$text', '-100') != char2_line.get('$text', '-101'):
                    return False
            return True

        found = False
        for existing in merged:
            if (
                existing.get("name") == name and
                compare_chars(existing.get("characteristics"), chars)
            ):
                found = True
                break

        if not found:
            merged.append(profile.copy())

    return merged


def add_css(bg: str, primary: str, secondary: str, teritary: str, dark: str, light: str, contrast: str, text: str) -> None:
    """ 
    Writes a new css file for user-defined theme based on a template and input vars
    """

    print(user_data_dir('servogen'))
