import tkinter as tk
from tkinter import ttk, messagebox
import time

# ---------- N-Queens Backtracking Algorithm ----------
def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]
        if placed == col:  # Same column
            return False
        if abs(prev_row - row) == abs(placed - col):  # Diagonal
            return False
    return True


def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo
                backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]


# ---------- GUI ----------
class QueensApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("N-Queens Placement Optimizer")
        self.geometry("1120x720")
        self.minsize(900, 600)
        self.configure(bg="#0f172a")

        self.n_var = tk.StringVar(value="8")
        self.status_var = tk.StringVar(value="Ready")
        self.summary_var = tk.StringVar(value="Enter a board size and click Solve.")
        self.time_var = tk.StringVar(value="—")
        self.backtrack_var = tk.StringVar(value="—")
        self.solution_var = tk.StringVar(value="—")
        self.current_solution = None
        self.current_index = 0
        self.solutions = []

        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        style.configure("TCombobox", font=("Segoe UI", 11))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10),
                        background="#111827", fieldbackground="#111827",
                        foreground="#e5e7eb")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#1e293b", foreground="#f8fafc")
        style.map("TButton", background=[("active", "#334155")])

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self, bg="#111827", padx=28, pady=20)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        tk.Label(header, text="N-Queens Placement Optimizer",
                 bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 22, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="Backtracking-based conflict-free placement planner",
                 bg="#111827", fg="#94a3b8",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=(4, 0))

        controls = tk.Frame(header, bg="#111827")
        controls.grid(row=0, column=1, rowspan=2, sticky="e")

        tk.Label(controls, text="Board Size (N)", bg="#111827", fg="#cbd5e1",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        self.n_entry = ttk.Combobox(controls, textvariable=self.n_var,
                                    values=[str(i) for i in range(4, 13)],
                                    width=6, state="normal")
        self.n_entry.pack(side="left", padx=6)
        ttk.Button(controls, text="Solve", command=self.solve).pack(side="left", padx=6)
        ttk.Button(controls, text="Clear", command=self.clear).pack(side="left", padx=6)

        body = tk.Frame(self, bg="#0f172a", padx=24, pady=20)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(1, weight=1)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)

        # Summary cards
        cards = tk.Frame(body, bg="#0f172a")
        cards.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        for i in range(3):
            cards.grid_columnconfigure(i, weight=1)

        self._card(cards, 0, "SOLUTIONS FOUND", self.solution_var)
        self._card(cards, 1, "BACKTRACK STEPS", self.backtrack_var)
        self._card(cards, 2, "EXECUTION TIME", self.time_var)

        # Board
        left = tk.Frame(body, bg="#111827", padx=18, pady=18)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        tk.Label(left, text="Placement Preview", bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(left, textvariable=self.summary_var, bg="#111827", fg="#94a3b8",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="e")

        self.board_canvas = tk.Canvas(left, bg="#0b1220", highlightthickness=0)
        self.board_canvas.grid(row=1, column=0, sticky="nsew", pady=(15, 0))
        self.board_canvas.bind("<Configure>", lambda e: self.draw_board())

        nav = tk.Frame(left, bg="#111827")
        nav.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(nav, text="◀ Previous", command=self.previous_solution).pack(side="left")
        ttk.Button(nav, text="Next ▶", command=self.next_solution).pack(side="left", padx=8)
        self.index_label = tk.Label(nav, text="No solution selected",
                                    bg="#111827", fg="#cbd5e1",
                                    font=("Segoe UI", 10, "bold"))
        self.index_label.pack(side="right")

        # Analysis / table
        right = tk.Frame(body, bg="#111827", padx=18, pady=18)
        right.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right.grid_rowconfigure(2, weight=1)
        right.grid_columnconfigure(0, weight=1)

        tk.Label(right, text="Solution Details", bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")

        tk.Label(right, text="Each row represents a queen; the value is its column position.",
                 bg="#111827", fg="#94a3b8", font=("Segoe UI", 9)).grid(
                     row=1, column=0, sticky="w", pady=(3, 12))

        table_frame = tk.Frame(right, bg="#111827")
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, columns=("row", "column"), show="headings")
        self.tree.heading("row", text="Queen / Row")
        self.tree.heading("column", text="Placed Column")
        self.tree.column("row", width=120, anchor="center")
        self.tree.column("column", width=140, anchor="center")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tk.Label(right, text="Performance", bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 12, "bold")).grid(row=3, column=0, sticky="w", pady=(15, 5))
        self.performance = tk.Text(right, height=6, wrap="word",
                                   bg="#0b1220", fg="#cbd5e1",
                                   insertbackground="#fff", relief="flat",
                                   font=("Consolas", 9), padx=12, pady=10)
        self.performance.grid(row=4, column=0, sticky="ew")
        self.performance.insert("1.0", "Solve the board to view performance analysis.")
        self.performance.configure(state="disabled")

        footer = tk.Frame(self, bg="#0b1220", padx=24, pady=8)
        footer.grid(row=2, column=0, sticky="ew")
        tk.Label(footer, textvariable=self.status_var, bg="#0b1220", fg="#94a3b8",
                 font=("Segoe UI", 9)).pack(side="left")
        tk.Label(footer, text="Algorithm: Backtracking", bg="#0b1220", fg="#64748b",
                 font=("Segoe UI", 9)).pack(side="right")

    def _card(self, parent, col, title, variable):
        card = tk.Frame(parent, bg="#111827", padx=16, pady=13)
        card.grid(row=0, column=col, sticky="ew", padx=6)
        tk.Label(card, text=title, bg="#111827", fg="#64748b",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(card, textvariable=variable, bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(3, 0))

    def solve(self):
        try:
            n = int(self.n_var.get().strip())
            if n < 4 or n > 12:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Board Size",
                                 "Enter an integer N between 4 and 12.")
            return

        self.status_var.set(f"Solving {n}-Queens...")
        self.update_idletasks()

        start = time.perf_counter()
        solutions, backtracks = solve_n_queens(n)
        elapsed = time.perf_counter() - start

        self.solutions = solutions
        self.current_index = 0
        self.solution_var.set(f"{len(solutions):,}")
        self.backtrack_var.set(f"{backtracks:,}")
        self.time_var.set(f"{elapsed * 1000:.2f} ms")
        self.summary_var.set(
            f"{n} queens placed on an {n}×{n} board with no row, column or diagonal conflicts."
        )
        self.status_var.set("Solved successfully.")
        self.update_details()
        self.draw_board()

    def update_details(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.solutions:
            self.index_label.config(text="No solution")
            return

        self.current_solution = self.solutions[self.current_index]
        for row, col in enumerate(self.current_solution, start=1):
            self.tree.insert("", "end", values=(row, col + 1))

        self.index_label.config(
            text=f"Solution {self.current_index + 1} of {len(self.solutions):,}"
        )

        n = len(self.current_solution)
        self.performance.configure(state="normal")
        self.performance.delete("1.0", "end")
        self.performance.insert(
            "1.0",
            f"Board size: {n} × {n}\n"
            f"Solutions found: {len(self.solutions):,}\n"
            f"Backtrack steps: {self.backtrack_var.get()}\n"
            f"Measured execution time: {self.time_var.get()}\n\n"
            "The solver explores candidate queen positions row by row and "
            "undoes a placement whenever it cannot lead to a valid arrangement."
        )
        self.performance.configure(state="disabled")

    def draw_board(self):
        self.board_canvas.delete("all")
        if not self.current_solution:
            self.board_canvas.create_text(
                self.board_canvas.winfo_width() // 2,
                self.board_canvas.winfo_height() // 2,
                text="Choose a board size and click Solve",
                fill="#64748b", font=("Segoe UI", 12, "bold")
            )
            return

        n = len(self.current_solution)
        w = max(self.board_canvas.winfo_width(), 200)
        h = max(self.board_canvas.winfo_height(), 200)
        size = min(w, h) - 20
        cell = size / n
        x0 = (w - size) / 2
        y0 = (h - size) / 2

        for r in range(n):
            for c in range(n):
                x1, y1 = x0 + c * cell, y0 + r * cell
                x2, y2 = x1 + cell, y1 + cell
                fill = "#1e293b" if (r + c) % 2 == 0 else "#334155"
                self.board_canvas.create_rectangle(x1, y1, x2, y2,
                                                   fill=fill, outline="#475569")
                if self.current_solution[r] == c:
                    self.board_canvas.create_text(
                        (x1 + x2) / 2, (y1 + y2) / 2,
                        text="♛", fill="#f8fafc",
                        font=("Segoe UI Symbol", max(14, int(cell * 0.55)), "bold")
                    )

    def next_solution(self):
        if self.solutions:
            self.current_index = (self.current_index + 1) % len(self.solutions)
            self.update_details()
            self.draw_board()

    def previous_solution(self):
        if self.solutions:
            self.current_index = (self.current_index - 1) % len(self.solutions)
            self.update_details()
            self.draw_board()

    def clear(self):
        self.solutions = []
        self.current_solution = None
        self.current_index = 0
        self.solution_var.set("—")
        self.backtrack_var.set("—")
        self.time_var.set("—")
        self.summary_var.set("Enter a board size and click Solve.")
        self.status_var.set("Ready")
        self.index_label.config(text="No solution selected")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.performance.configure(state="normal")
        self.performance.delete("1.0", "end")
        self.performance.insert("1.0", "Solve the board to view performance analysis.")
        self.performance.configure(state="disabled")
        self.draw_board()


if __name__ == "__main__":
    app = QueensApp()
    app.mainloop()
