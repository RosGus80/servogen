# Servogen - template generator for new recruit rosters

A **CLI tool** that transforms your **[NewRecruit.eu](https://newrecruit.eu)** rosters from raw json into clean, styled, and navigable **HTML** files — perfect for printing, sharing, or referencing during gameplay.

> ⚠️ This tool is currently in testing phase. If you face any issues, please copy the error message and contact me (preferably by opening an issue thread on Github), sharing your json file that caused the error

## Features

* Converts NewRecruit `.json` files into static HTML  
* Currently is only tested on WH40k and WH30k rosters, may display nonsense or cause errors on rosters from other games
* Highlights your force rules, selected units rules, adds hyperlinking to comfortly navigate through your list. Overall, does new recruit pretty output but better
* No server required — just open the HTML file in your browser  
* You can add your custom themes - see "Themes" in this README
* Powered by **[Jinja2](https://jinja.palletsprojects.com/)**


## Installation 
You would have to have a downloaded python on your computer. If you dont have one, get it from https://www.python.org/downloads/

Go to terminal and type `pip isntall git+https://github.com/RosGus80/servogen`

Also, if you face any issues while using the tool, first try updating the package using `pip --upgrade --force-reisntall git+https://github.com/RosGus80/servogen`

## Usage
After building your roster on new recruit, export it to .json (this option is available in the export options), then, in terminal, write `servogen -r path_to_json.json -o path_to_output`, and you'll get a ready-to-use html file - you can open it by double clicking.

It seems like when you open the file on IPhone file preview, the JS isn't working, so hyperlinking may not work properly. I will adress this issue later.

## Themes

You can add your custom themes and use it in your rosters. To define a new custom theme, use -at or --add-theme command. After that, pass pairs of keys-values like this: ```servogen -at name:new primary:#eeeeee ...``` etc. you have to always define name as it would be the name if your theme. Then you have 8 colors to change:
* background
* primary
* secondary
* teritary 
* dark
* light 
* contrast
* text 
* title

The names are verbose, but note that light and dark are actually interchangable - if you define a dark theme, "dark" color would be light. If you dont define some of the keys, the values would automatically be taken from the original light theme. 'Title' color is the color for unit titles in their cards. Leave blank if you want this text to be equivalent to the default color text
To use your new theme, render the template like this: ```servogen -r path.json -t name``` - use your defined theme name. 
Data of user created data is stored in your user data folder (e.g. on Mac Os it would be ...Application Support/servogen)

## Planned Features

* Interactive HTML (collapse/expand, custom filtering, mark models as dead)  
* Roster statistics and tactical summaries  

## License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** License.  
You are free to use, modify, and distribute it — just credit the original author if you modify it or use it commercially (you can leave a link to this github).  
[Read the full license here.](https://creativecommons.org/licenses/by/4.0/)
