# NewRecruit-templategen

A work-in-progress **CLI tool** that transforms your **[NewRecruit.eu](https://newrecruit.eu)** rosters from raw json into clean, styled, and navigable **HTML** files — perfect for printing, sharing, or referencing during gameplay.

> ⚠️ This tool is currently under development. If you face any issues, please copy the error message and contact me (preferably by opening an issue thread on Github), sharing your json file that caused the error

## Features

* Converts NewRecruit `.json` files into static HTML  
* Highlights your force rules, selected units rules, adds hyperlinking to comfortly navigate through your list  
* No server required — just open the HTML file in your browser  
* Powered by **[Jinja2](https://jinja.palletsprojects.com/)**


## Installation 
You will have to have a downloaded python on your computer. If you dont have one, get it from https://www.python.org/downloads/

Go to terminal and type `pip isntall git+https://github.com/RosGus80/servogen`

Also, if you face any issues, first try updating the package using `pip --upgrade --force-reisntall git+https://github.com/RosGus80/servogen`

## Usage
After building your roster on new recruit, export it to .json (this option is available in the export options), then, in terminal, write `servogen -r path_to_json.json -o path_to_output`, and you'll get a ready-to-use html file - you can open it by double clicking.

It seems like when you open the file on IPhone file preview, the JS isnt working, so hyperlinking may not work properly. I will adress this issue later.

## Planned Features

* Export to **print-ready PDF**  
* Interactive HTML (collapse/expand, custom filtering, mark models as dead)  
* Roster statistics and tactical summaries  
* Customisable color themes

## License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** License.  
You are free to use, modify, and distribute it — just please credit the original author.  
[Read the full license here.](https://creativecommons.org/licenses/by/4.0/)
