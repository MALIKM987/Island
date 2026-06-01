from pathlib import Path
import sys

from island_logic import InputDataError, read_island_map
from visualizer import run_visualizer


DEFAULT_GRID = [
    [8, 5, 7, 3, 1],
    [5, 5, 6, 7, 3],
    [1, 4, 2, 4, 4],
    [2, 3, 5, 5, 6],
    [2, 3, 2, 4, 4],
]


def get_application_directory():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def load_start_map():
    app_directory = get_application_directory()
    candidates = [
        Path.cwd() / "input.txt",
        app_directory / "input.txt",
    ]

    for candidate in candidates:
        if not candidate.exists():
            continue

        try:
            return read_island_map(candidate), str(candidate)
        except (FileNotFoundError, InputDataError):
            break

    return DEFAULT_GRID, "wbudowany przyklad - uzyj przycisku Wczytaj plik"


def main():
    grid, file_path = load_start_map()
    run_visualizer(grid, file_path)


if __name__ == "__main__":
    main()
