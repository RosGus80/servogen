from jinja2 import Environment, FileSystemLoader
from service import json_load, bundle_css, find_units, find_rules


roster: dict = json_load('roster.json')['roster']


environment = Environment(loader=FileSystemLoader('templates/'))
template = environment.get_template('main.html')


def find_detachment() -> dict | None:
    """
    finds a dict of detachment info. Could be always on 
    roster['forces'][0]['selections'][1], but i wouldnt bet on it. 
    """

    for entry in roster['forces'][0]['selections']:
        if entry['name'] == 'Detachment':
            return entry
    return None
        

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
faction_rule_name: str = roster['forces'][0]['rules'][0]['name']
faction_rule_description: str = roster['forces'][0]['rules'][0]['description']

detach_entry: dict | None = find_detachment()
if detach_entry is None:
    detachment_name = 'No detachment'
    detachment_description = ''
else:
    detachment_name: str = detach_entry['selections'][0]['name']
    detachment_description: str = detach_entry['selections'][0]['profiles'][0]['characteristics'][0]['$text']

units = find_units(roster)
rules = find_rules(units)

content = template.render(
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
    file.write(content)

bundle_css('outputs/out.html', 'css/style.css')
