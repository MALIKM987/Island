import argparse
import sys

from island_logic import InputDataError, find_minimal_split_level, format_result, read_island_map


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        description="Zadanie grafowe nr 14: zalewanie wyspy."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="input.txt",
        help="Plik tekstowy z mapa wyspy. Domyslnie: input.txt",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Uruchom tryb graficzny Tkinter.",
    )

    return parser.parse_args(arguments)


def run_text_mode(input_file):
    grid = read_island_map(input_file)
    split_level = find_minimal_split_level(grid)
    print(format_result(split_level))


def run_gui_mode(input_file):
    grid = read_island_map(input_file)

    try:
        from visualizer import run_visualizer
    except ImportError as error:
        print(f"Blad: nie mozna uruchomic GUI Tkinter: {error}", file=sys.stderr)
        return 1

    run_visualizer(grid, input_file)
    return 0


def main(arguments=None):
    args = parse_arguments(arguments if arguments is not None else sys.argv[1:])

    try:
        if args.gui:
            return run_gui_mode(args.input_file)

        run_text_mode(args.input_file)
        return 0
    except FileNotFoundError as error:
        print(f"Blad: {error}", file=sys.stderr)
        return 1
    except InputDataError as error:
        print(f"Blad danych: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
