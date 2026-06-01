import tkinter as tk
from tkinter import filedialog, messagebox

from island_logic import (
    InputDataError,
    find_minimal_split_level,
    format_result,
    generate_simulation_states,
    read_island_map,
)


CANVAS_SIZE = 720
ANIMATION_DELAY_MS = 700

COMPONENT_COLORS = [
    "#7cb342",
    "#f9a825",
    "#8e7cc3",
    "#ef6c00",
    "#26a69a",
    "#c2185b",
    "#5c6bc0",
    "#9ccc65",
]


class IslandVisualizer:
    def __init__(self, root, grid, file_path):
        self.root = root
        self.grid = grid
        self.file_path = file_path
        self.states = []
        self.current_index = 0
        self.animation_job = None
        self.split_level = None

        self.root.title("Zalewanie wyspy")
        self.root.minsize(760, 860)

        self.file_label = tk.StringVar()
        self.level_label = tk.StringVar()
        self.parts_label = tk.StringVar()
        self.result_label = tk.StringVar()

        self._build_widgets()
        self.load_grid(grid, file_path)

    def _build_widgets(self):
        top_frame = tk.Frame(self.root, padx=10, pady=8)
        top_frame.pack(fill=tk.X)

        tk.Button(top_frame, text="Wczytaj plik", command=self.choose_file).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Poprzedni poziom", command=self.previous_level).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Nastepny poziom", command=self.next_level).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Start animacji", command=self.start_animation).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Stop animacji", command=self.stop_animation).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=3)

        info_frame = tk.Frame(self.root, padx=10)
        info_frame.pack(fill=tk.X)

        tk.Label(info_frame, textvariable=self.file_label, anchor="w").pack(fill=tk.X)
        tk.Label(info_frame, textvariable=self.level_label, anchor="w").pack(fill=tk.X)
        tk.Label(info_frame, textvariable=self.parts_label, anchor="w").pack(fill=tk.X)
        tk.Label(
            info_frame,
            textvariable=self.result_label,
            anchor="w",
            font=("Arial", 10, "bold"),
        ).pack(fill=tk.X, pady=(0, 8))

        self.canvas = tk.Canvas(
            self.root,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            background="#f4f1e8",
            highlightthickness=1,
            highlightbackground="#999999",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda event: self.draw_board())

    def load_grid(self, grid, file_path):
        self.stop_animation()
        self.grid = grid
        self.file_path = file_path
        self.states = generate_simulation_states(grid)
        self.current_index = 0
        self.split_level = find_minimal_split_level(grid)
        self.draw_board()

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Wybierz plik z mapa wyspy",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")],
        )

        if not path:
            return

        try:
            grid = read_island_map(path)
        except FileNotFoundError as error:
            messagebox.showerror("Blad", str(error))
            return
        except InputDataError as error:
            messagebox.showerror("Blad danych", str(error))
            return

        self.load_grid(grid, path)

    def previous_level(self):
        self.stop_animation()
        if self.current_index > 0:
            self.current_index -= 1
            self.draw_board()

    def next_level(self):
        self.stop_animation()
        if self.current_index < len(self.states) - 1:
            self.current_index += 1
            self.draw_board()

    def start_animation(self):
        self.stop_animation()
        self.animation_job = self.root.after(ANIMATION_DELAY_MS, self._animation_step)

    def _animation_step(self):
        if self.current_index < len(self.states) - 1:
            self.current_index += 1
            self.draw_board()
            self.animation_job = self.root.after(ANIMATION_DELAY_MS, self._animation_step)
        else:
            self.animation_job = None

    def stop_animation(self):
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

    def reset(self):
        self.stop_animation()
        self.current_index = 0
        self.draw_board()

    def draw_board(self):
        if not self.states:
            return

        self.canvas.delete("all")
        state = self.states[self.current_index]
        size = len(self.grid)
        canvas_width = max(self.canvas.winfo_width(), 1)
        canvas_height = max(self.canvas.winfo_height(), 1)
        cell_size = min(canvas_width, canvas_height) / size
        board_size = cell_size * size
        offset_x = (canvas_width - board_size) / 2
        offset_y = (canvas_height - board_size) / 2
        font_size = max(6, min(14, int(cell_size * 0.36)))

        for row in range(size):
            for column in range(size):
                x1 = offset_x + column * cell_size
                y1 = offset_y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                fill_color = self.get_cell_color(state, row, column)
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill_color,
                    outline="#2f2f2f",
                    width=1,
                )
                self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=str(self.grid[row][column]),
                    fill=self.get_text_color(fill_color),
                    font=("Arial", font_size, "bold"),
                )

        self.update_labels(state)

    def get_cell_color(self, state, row, column):
        if state.flooded[row][column]:
            if state.newly_flooded[row][column]:
                return "#8ecdf8"
            return "#2878c8"

        label = state.dry_labels[row][column]
        if state.dry_component_count >= 2 and label > 0:
            return COMPONENT_COLORS[(label - 1) % len(COMPONENT_COLORS)]

        return self.get_height_color(self.grid[row][column])

    def get_height_color(self, height):
        max_height = max(1, max(max(row) for row in self.grid))
        ratio = min(1.0, max(0.0, height / max_height))

        low = (112, 168, 82)
        high = (137, 92, 47)
        red = int(low[0] + (high[0] - low[0]) * ratio)
        green = int(low[1] + (high[1] - low[1]) * ratio)
        blue = int(low[2] + (high[2] - low[2]) * ratio)

        return f"#{red:02x}{green:02x}{blue:02x}"

    def get_text_color(self, fill_color):
        red = int(fill_color[1:3], 16)
        green = int(fill_color[3:5], 16)
        blue = int(fill_color[5:7], 16)
        brightness = (red * 299 + green * 587 + blue * 114) / 1000

        if brightness > 145:
            return "#111111"

        return "#ffffff"

    def update_labels(self, state):
        self.file_label.set(f"Plik: {self.file_path}")
        self.level_label.set(f"Aktualny poziom morza: {state.sea_level}")
        self.parts_label.set(f"Liczba suchych czesci wyspy: {state.dry_component_count}")
        self.result_label.set(format_result(self.split_level))


def run_visualizer(grid, file_path):
    root = tk.Tk()
    IslandVisualizer(root, grid, file_path)
    root.mainloop()
