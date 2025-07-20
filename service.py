import json
from pprint import pprint

def json_load(path: str):
    with open(path, 'r') as file:
        return json.load(file)
    

def bundle_css(html_path: str, css_path: str) -> None:
    """Function that takes a css file that was previously linked by href and 
    explicitly puts it into the html file into <style> tag so that we can 
    double-click open it"""
    pass


def find_units(json_roster: dict) -> list:
    selections = json_roster['forces'][0]['selections']
    output = []

    for selection in selections:
        try:
            if selection['type'].lower() in ('unit', 'model'):
                output.append(selection)
        except KeyError:
            continue
    
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


