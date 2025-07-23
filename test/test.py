import os
from servogen.parse import render_html

dir: str = './test/json'

for file in os.listdir(dir):
    full_path = os.path.join(dir, file)

    render_html(full_path, f'./test/outputs/{file.split('.')[0]}.html')

