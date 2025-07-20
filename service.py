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


