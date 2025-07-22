#!/usr/bin/env python3

def main():
    import argparse
    import os
    from servogen.parse import render_html

    parser = argparse.ArgumentParser(
        prog='servogen',
        description='Tool for converting your New Recruit JSON rosters into readable '
                    'and navigable HTML pages – more elegant than New Recruit\'s own export!' \
                    'In order to render, use -r flag and specify a path to your json file after. ' \
                    'You can choose if you like your units\'s abilities collapsible or not - pass -c flag if you want them to collapse',
        usage='servogen -r roster.json output.html --collapsible'
    )

    parser.add_argument(
        '-r', '--render',
        nargs='+',
        metavar=('INPUT', 'OUTPUT'),
        help='Render a New Recruit JSON file into HTML. Optionally specify output path.'
    )

    parser.add_argument(
        '-c', '--collapsible',
        action='store_true',
        help='Enable collapsible sections for unit rules and abilities.'
    )

    args = parser.parse_args()

    if args.render:
        if len(args.render) < 1:
            parser.error("You must provide at least an input JSON file.")

        input_path = args.render[0]
        output_path = (
            args.render[1]
            if len(args.render) > 1
            else os.path.splitext(input_path)[0] + ".html"
        )

        render_html(input_path, output_path, collapse=args.collapsible)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
