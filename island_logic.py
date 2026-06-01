from collections import deque
from dataclasses import dataclass
from pathlib import Path


class InputDataError(Exception):
    """Blad danych wejsciowych."""


@dataclass
class IslandState:
    sea_level: int
    flooded: list
    newly_flooded: list
    dry_labels: list
    dry_component_count: int


def read_island_map(file_path):
    """Wczytuje i sprawdza mape wyspy z pliku tekstowego."""
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie znaleziono pliku: {file_path}")

    if not lines:
        raise InputDataError("Plik jest pusty.")

    try:
        size = int(lines[0])
    except ValueError:
        raise InputDataError("Pierwsza linia musi zawierac liczbe calkowita n.")

    if size <= 0:
        raise InputDataError("Rozmiar macierzy n musi byc dodatni.")

    data_lines = lines[1:]
    if len(data_lines) != size:
        raise InputDataError(
            f"Zly rozmiar macierzy: oczekiwano {size} wierszy, "
            f"otrzymano {len(data_lines)}."
        )

    grid = []
    for row_index, line in enumerate(data_lines, start=1):
        values = line.split()

        if len(values) != size:
            raise InputDataError(
                f"Zly rozmiar macierzy: wiersz {row_index} ma {len(values)} "
                f"wartosci zamiast {size}."
            )

        row = []
        for column_index, value in enumerate(values, start=1):
            try:
                row.append(int(value))
            except ValueError:
                raise InputDataError(
                    f"Wartosc w wierszu {row_index}, kolumnie {column_index} "
                    f"nie jest liczba calkowita: {value}"
                )

        grid.append(row)

    return grid


def get_neighbors(row, column, size):
    """Zwraca sasiadow pola liczonych tylko bokami."""
    for row_delta, column_delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_row = row + row_delta
        next_column = column + column_delta

        if 0 <= next_row < size and 0 <= next_column < size:
            yield next_row, next_column


def simulate_flooding(grid, sea_level):
    """Symuluje zalewanie wyspy od brzegu mapy za pomoca BFS."""
    size = len(grid)
    flooded = [[False for _ in range(size)] for _ in range(size)]
    queue = deque()

    def add_start_cell(row, column):
        if not flooded[row][column] and grid[row][column] <= sea_level:
            flooded[row][column] = True
            queue.append((row, column))

    for index in range(size):
        add_start_cell(0, index)
        add_start_cell(size - 1, index)
        add_start_cell(index, 0)
        add_start_cell(index, size - 1)

    # BFS: morze startuje tylko z pol brzegowych i przechodzi dalej
    # wylacznie przez pola osiagalne bokiem oraz nie wyzsze od poziomu wody.
    while queue:
        row, column = queue.popleft()

        for next_row, next_column in get_neighbors(row, column, size):
            if flooded[next_row][next_column]:
                continue
            if grid[next_row][next_column] > sea_level:
                continue

            flooded[next_row][next_column] = True
            queue.append((next_row, next_column))

    return flooded


def label_dry_components(flooded):
    """Liczy suche komponenty i nadaje im etykiety za pomoca DFS."""
    size = len(flooded)
    labels = [[0 for _ in range(size)] for _ in range(size)]
    component_id = 0

    for row in range(size):
        for column in range(size):
            if flooded[row][column] or labels[row][column] != 0:
                continue

            component_id += 1
            labels[row][column] = component_id
            stack = [(row, column)]

            # DFS: przechodzimy tylko po suchych polach, laczac pola bokami.
            while stack:
                current_row, current_column = stack.pop()

                for next_row, next_column in get_neighbors(current_row, current_column, size):
                    if flooded[next_row][next_column] or labels[next_row][next_column] != 0:
                        continue

                    labels[next_row][next_column] = component_id
                    stack.append((next_row, next_column))

    return component_id, labels


def count_dry_areas(flooded):
    dry_component_count, _ = label_dry_components(flooded)
    return dry_component_count


def get_max_height(grid):
    return max(max(row) for row in grid)


def get_newly_flooded(current_flooded, previous_flooded):
    size = len(current_flooded)
    newly_flooded = [[False for _ in range(size)] for _ in range(size)]

    if previous_flooded is None:
        return newly_flooded

    for row in range(size):
        for column in range(size):
            newly_flooded[row][column] = (
                current_flooded[row][column] and not previous_flooded[row][column]
            )

    return newly_flooded


def analyze_level(grid, sea_level, previous_flooded=None):
    flooded = simulate_flooding(grid, sea_level)
    dry_component_count, dry_labels = label_dry_components(flooded)
    newly_flooded = get_newly_flooded(flooded, previous_flooded)

    return IslandState(
        sea_level=sea_level,
        flooded=flooded,
        newly_flooded=newly_flooded,
        dry_labels=dry_labels,
        dry_component_count=dry_component_count,
    )


def generate_simulation_states(grid):
    """Generuje stany dla poziomow morza od 0 do maksymalnej wysokosci."""
    max_height = max(0, get_max_height(grid))
    previous_flooded = None
    states = []

    for sea_level in range(0, max_height + 1):
        state = analyze_level(grid, sea_level, previous_flooded)
        states.append(state)
        previous_flooded = state.flooded

    return states


def find_minimal_split_level(grid):
    """Zwraca minimalny poziom morza dzielacy wyspe albo None."""
    for state in generate_simulation_states(grid):
        if state.dry_component_count >= 2:
            return state.sea_level

    return None


def format_result(split_level):
    if split_level is None:
        return "Wyspa nie zostanie podzielona."

    return f"Minimalny wzrost poziomu morza: {split_level} stopy"
