import time
import tkinter as tk

from puzzle import CELL_COUNT, SIZE, SOLVED_BOARD, move_tile, new_shuffled_board


BACKGROUND = "#111827"
CARD = "#1F2937"
TILE = "#2563EB"
TILE_HOVER = "#3B82F6"
TEXT = "#F9FAFB"
MUTED = "#9CA3AF"
ACCENT = "#FBBF24"


class PuzzleApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("הפאזל 15")
        self.root.geometry("600x740")
        self.root.minsize(460, 600)
        self.root.configure(bg=BACKGROUND)

        self.board = SOLVED_BOARD
        self.starting_board = SOLVED_BOARD
        self.moves = 0
        self.started_at = time.monotonic()
        self.finished = False
        self.finished_at: float | None = None
        self.tiles: list[tk.Button] = []

        self._build_ui()
        self.new_game()
        self.root.bind("<Left>", lambda _event: self._move_from_blank(-1))
        self.root.bind("<Right>", lambda _event: self._move_from_blank(1))
        self.root.bind("<Up>", lambda _event: self._move_from_blank(-SIZE))
        self.root.bind("<Down>", lambda _event: self._move_from_blank(SIZE))
        self._update_clock()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=BACKGROUND)
        header.pack(fill="x", padx=32, pady=(28, 18))

        tk.Label(
            header,
            text="הפאזל 15",
            bg=BACKGROUND,
            fg=TEXT,
            font=("DejaVu Sans", 27, "bold"),
        ).pack()
        tk.Label(
            header,
            text="סדרו את המספרים לפי הסדר",
            bg=BACKGROUND,
            fg=MUTED,
            font=("DejaVu Sans", 12),
        ).pack(pady=(5, 0))

        card = tk.Frame(self.root, bg=CARD, padx=22, pady=22)
        card.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        stats = tk.Frame(card, bg=CARD)
        stats.pack(fill="x", pady=(0, 16))
        stats.grid_columnconfigure((0, 1), weight=1)

        self.moves_label = tk.Label(
            stats, text="", bg=CARD, fg=TEXT, font=("DejaVu Sans", 14, "bold")
        )
        self.moves_label.grid(row=0, column=0)
        self.clock_label = tk.Label(
            stats, text="00:00", bg=CARD, fg=TEXT, font=("DejaVu Sans", 14, "bold")
        )
        self.clock_label.grid(row=0, column=1)

        self.board_frame = tk.Frame(card, bg=CARD)
        self.board_frame.pack(fill="both", expand=True)
        for row in range(SIZE):
            self.board_frame.grid_rowconfigure(row, weight=1, uniform="board")
            self.board_frame.grid_columnconfigure(row, weight=1, uniform="board")

        for index in range(CELL_COUNT):
            button = tk.Button(
                self.board_frame,
                command=lambda tile_index=index: self._on_tile_click(tile_index),
                bg=TILE,
                fg=TEXT,
                activebackground=TILE_HOVER,
                activeforeground=TEXT,
                disabledforeground=TEXT,
                font=("DejaVu Sans", 20, "bold"),
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                cursor="hand2",
            )
            button.grid(
                row=index // SIZE,
                column=index % SIZE,
                sticky="nsew",
                padx=5,
                pady=5,
            )
            button.bind("<Enter>", lambda event: event.widget.configure(bg=TILE_HOVER))
            button.bind("<Leave>", lambda event: self._restore_tile_color(event.widget))
            self.tiles.append(button)

        self.message_label = tk.Label(
            card,
            text="",
            bg=CARD,
            fg=MUTED,
            font=("DejaVu Sans", 11),
            wraplength=420,
        )
        self.message_label.pack(pady=(15, 13))

        controls = tk.Frame(card, bg=CARD)
        controls.pack(fill="x")
        tk.Button(
            controls,
            text="משחק חדש",
            command=self.new_game,
            bg=ACCENT,
            fg="#111827",
            activebackground="#FCD34D",
            activeforeground="#111827",
            font=("DejaVu Sans", 12, "bold"),
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(side="right", padx=(8, 0))
        tk.Button(
            controls,
            text="התחלה מחדש",
            command=self.restart_game,
            bg="#374151",
            fg=TEXT,
            activebackground="#4B5563",
            activeforeground=TEXT,
            font=("DejaVu Sans", 11),
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=10,
            cursor="hand2",
        ).pack(side="right")

        tk.Label(
            self.root,
            text="אפשר להזיז אריחים בלחיצה או עם מקשי החצים",
            bg=BACKGROUND,
            fg=MUTED,
            font=("DejaVu Sans", 10),
        ).pack(pady=(0, 18))

    def _restore_tile_color(self, widget: tk.Button) -> None:
        widget.configure(bg=BACKGROUND if widget.cget("text") == "" else TILE)

    def _on_tile_click(self, tile_index: int) -> None:
        self._make_move(tile_index)

    def _move_from_blank(self, offset: int) -> str:
        blank_index = self.board.index(0)
        tile_index = blank_index + offset
        if (
            0 <= tile_index < CELL_COUNT
            and (abs(offset) != 1 or blank_index // SIZE == tile_index // SIZE)
        ):
            self._make_move(tile_index)
        return "break"

    def _make_move(self, tile_index: int) -> None:
        if self.finished:
            return

        updated = move_tile(self.board, tile_index)
        if updated == self.board:
            return

        self.board = updated
        self.moves += 1
        self._render_board()
        self.moves_label.configure(text=f"מהלכים: {self.moves}")
        if self.board == SOLVED_BOARD:
            self.finished = True
            self.finished_at = time.monotonic()
            self.message_label.configure(
                text=f"כל הכבוד! השלמתם את הפאזל ב־{self.moves} מהלכים.",
                fg=ACCENT,
                font=("DejaVu Sans", 12, "bold"),
            )

    def _render_board(self) -> None:
        for button, value in zip(self.tiles, self.board):
            button.configure(
                text="" if value == 0 else str(value),
                bg=BACKGROUND if value == 0 else TILE,
                cursor="arrow" if value == 0 else "hand2",
            )

    def new_game(self) -> None:
        self.board = new_shuffled_board()
        self.starting_board = self.board
        self._reset_game_state()

    def restart_game(self) -> None:
        self.board = self.starting_board
        self._reset_game_state()

    def _reset_game_state(self) -> None:
        self.moves = 0
        self.started_at = time.monotonic()
        self.finished = False
        self.finished_at = None
        self.moves_label.configure(text="מהלכים: 0")
        self.message_label.configure(
            text="הזיזו אריחים למקום הריק עד שהמספרים יהיו מסודרים.",
            fg=MUTED,
            font=("DejaVu Sans", 11),
        )
        self._render_board()

    def _update_clock(self) -> None:
        end_time = self.finished_at if self.finished_at is not None else time.monotonic()
        elapsed = int(end_time - self.started_at)
        minutes, seconds = divmod(elapsed, 60)
        self.clock_label.configure(text=f"זמן: {minutes:02d}:{seconds:02d}")
        self.root.after(250, self._update_clock)


def main() -> None:
    root = tk.Tk()
    PuzzleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
