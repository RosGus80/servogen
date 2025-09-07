#!/usr/bin/env python3

def main():
    import argparse
    import os
    from servogen.parse import render_html
    from servogen.service import add_css, parse_theme

    parser = argparse.ArgumentParser(
        prog='servogen',
        description='Tool for converting your New Recruit JSON rosters into readable '
                    'and navigable HTML pages – more elegant than New Recruit\'s own export! '
                    'Use -r flag to specify input JSON file. Use -o to specify output HTML file. '
                    'If no -o is provided, output will be saved next to input file with .html extension. '
                    'Use -c to enable collapsible sections.',
        usage='servogen -r roster.json [-o output.html] [--collapsible] [--dark]'
    )

    parser.add_argument(
        '-r', '--render',
        metavar='INPUT',
        help='Path to the New Recruit JSON file to render into HTML.'
    )

    parser.add_argument(
        '-o', '--output',
        metavar='OUTPUT',
        help='Path to output HTML file. If selected, saved next to input with .html extension.'
    )

    parser.add_argument(
        '-c', '--collapsible',
        action='store_true',
        help='Enable collapsible sections for unit rules and abilities.'
    )

    parser.add_argument(
        '-t', '--theme',
        metavar='THEME',
        help='Pass a theme name to use this theme in new render (servogen -r file.json -t dark)'
    )

    parser.add_argument(
        '-at', '--add-theme', 
        nargs='+',
        type=str,
        help='Add a theme, e.g. --add-theme name:light primary:#ffffff'
    )

    args = parser.parse_args()

    if args.add_theme: 
        theme = parse_theme(args.add_theme)
        
        if 'name' not in theme.keys():
            raise ValueError('You have to provide a theme name (example: name:new)')

        add_css(theme['name'], theme.get('background', '#ffffff'), theme.get('primary', '#649699'), theme.get('secondary', '#2a856a'), theme.get('teritary', '#e0e0e0'), theme.get('dark', '#193341'), theme.get('light', '#efefef'), theme.get('contrast', '#c75040'), theme.get('text', '#000000'), theme.get('title', ''))
        return None

    input_path = args.render
    if args.output:
        output_path = args.output
    else:
        input_dir = os.path.dirname(input_path)
        input_basename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(input_dir, input_basename + ".html")

    theme_name: str | None = None if args.theme is None else args.theme
    render_html(input_path, output_path, collapse=args.collapsible, theme=theme_name)

 
if __name__ == '__main__':
    main()
