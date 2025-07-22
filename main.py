from jinja2 import Environment, FileSystemLoader
from service import json_load, bundle_css, find_units, find_rules, normalise_markup, load_prefs, find_faction_rule


roster: dict = json_load('ALL(1).json')['roster']
prefs = load_prefs()


environment = Environment(loader=FileSystemLoader('templates/'))
template = environment.get_template('main.html')


def find_detachment() -> dict:
    """
    finds a dict of detachment info. Could be always on 
    roster['forces'][0]['selections'][1], but i wouldnt bet on it. 
    """

    for entry in roster['forces'][0]['selections']:
        if entry['name'] == 'Detachment':
            return entry
    return {}
        

# All the env vars for template

"""
roster['name'] - roster name
roster['generatedBy'] - newrecruit link

roster['costs'][0]['name'] - cost value name (pts)
roster['costs'][0]['value'] - cost amount (1000)
roster['costLimits'][0]['value'] - cost limit amount

roster['forces'][0]['catalogueName'] - faction name
roster['forces'][0]['rules'][0]['name'] - faction rule name
roster['forces'][0]['rules'][0]['description'] - factiopn rule description
"""

nr_link: str = roster['generatedBy']
roster_name: str = roster['name']
cost_string: str = roster['costs'][0]['name']
cost_value: int = roster['costs'][0]['value']
cost_limit: int = roster['costLimits'][0]['value']

faction_name: str = roster['forces'][0]['catalogueName']
faction_rule_name, faction_rule_description = find_faction_rule(roster)

detach_entry: dict = find_detachment()

if 'selections' not in detach_entry.keys():
    detachment_name = 'No detachment'
    detachment_description = ''
else:
    detachment_name: str = detach_entry['selections'][0]['name']

    if 'profiles' in detach_entry['selections'][0].keys():
        detachment_description: str = detach_entry['selections'][0]['profiles'][0]['characteristics'][0]['$text']
    elif 'rules' in detach_entry['selections'][0].keys():
        detachment_description: str = detach_entry['selections'][0]['rules'][0]['description']
    else:
        detachment_description: str = 'Unknown json structure, wtf'

units = find_units(roster)
rules = find_rules(units)

content = template.render(
    prefs=prefs,

    roster_name=roster_name,
    cost_string=cost_string,
    cost_value=cost_value,
    cost_limit=cost_limit,
    newrecruit_link=nr_link,

    faction_name=faction_name,
    faction_rule_name=faction_rule_name,
    faction_rule_description=faction_rule_description,

    detachment_name=detachment_name,
    detachment_description=detachment_description,

    units=units,
    
    rules=rules,
)


with open("outputs/out.html", "w") as file:
    normalised_content: str = normalise_markup(content)
    file.write(normalised_content)

# bundle_css('outputs/out.html', 'css/style.css')
