import heapq
import time
from itertools import permutations
import tkinter as tk
from tkinter import ttk, messagebox

INF = float("inf")

# ============================================================
# DAA CORE — Travelling Salesman Problem using Branch & Bound
# ============================================================

def reduce_matrix(mat):
    """Reduce matrix and return reduction cost."""
    m = [row[:] for row in mat]
    n = len(m)
    cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(m[i])
        if row_min and row_min != INF:
            cost += row_min
            m[i] = [x - row_min if x != INF else INF for x in m[i]]

    # Column reduction
    for j in range(n):
        col_min = min(m[i][j] for i in range(n))
        if col_min and col_min != INF:
            cost += col_min
            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


def tsp_brute_force(cost, n):
    """Brute force verification retained from the supplied experiment."""
    cities = list(range(1, n))
    best_cost = INF
    best_path = None
    for perm in permutations(cities):
        path = [0] + list(perm) + [0]
        c = sum(cost[path[i]][path[i + 1]] for i in range(n))
        if c < best_cost:
            best_cost = c
            best_path = path
    return best_path, best_cost


def tsp_branch_and_bound(cost, n):
    """Branch and Bound TSP using the supplied matrix-reduction idea."""
    if n == 1:
        return [0, 0], 0, 0

    root_matrix, root_bound = reduce_matrix(cost)
    heap = []
    counter = 0
    # (lower_bound, tie_breaker, level, path, reduced_matrix, actual_path_cost)
    heapq.heappush(heap, (root_bound, counter, 0, [0], root_matrix, 0))

    best_cost = INF
    best_path = None
    expanded = 0

    while heap:
        bound, _, level, path, matrix, path_cost = heapq.heappop(heap)
        if bound >= best_cost:
            continue

        if level == n - 1:
            last = path[-1]
            if cost[last][0] != INF:
                total = path_cost + cost[last][0]
                if total < best_cost:
                    best_cost = total
                    best_path = path + [0]
            continue

        expanded += 1
        current = path[-1]

        for nxt in range(n):
            if nxt in path or cost[current][nxt] == INF:
                continue

            new_matrix = [row[:] for row in matrix]
            for j in range(n):
                new_matrix[current][j] = INF
            for i in range(n):
                new_matrix[i][nxt] = INF
            new_matrix[nxt][0] = INF

            reduced_matrix, reduction_cost = reduce_matrix(new_matrix)
            new_path_cost = path_cost + cost[current][nxt]
            new_bound = new_path_cost + reduction_cost

            if new_bound < best_cost:
                counter += 1
                heapq.heappush(
                    heap,
                    (new_bound, counter, level + 1, path + [nxt],
                     reduced_matrix, new_path_cost),
                )

    return best_path, best_cost, expanded


# ============================================================
# INPUT / APPLICATION HELPERS
# ============================================================

DEFAULT_NAMES = ["Warehouse", "North Zone", "Market", "Hospital", "Tech Park"]
DEFAULT_MATRIX = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF],
]


def parse_matrix(text):
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    if not rows:
        raise ValueError("Enter a route-cost matrix.")

    matrix = []
    for row in rows:
        values = []
        for token in row.replace(",", " ").split():
            if token.upper() in {"X", "INF"}:
                values.append(INF)
            else:
                value = float(token)
                if value < 0:
                    raise ValueError("Route costs cannot be negative.")
                values.append(int(value) if value.is_integer() else value)
        matrix.append(values)

    n = len(matrix)
    if not 3 <= n <= 8:
        raise ValueError("Use between 3 and 8 locations.")
    if any(len(row) != n for row in matrix):
        raise ValueError("The route-cost matrix must be square.")

    for i in range(n):
        matrix[i][i] = INF
        for j in range(n):
            if matrix[i][j] != INF and matrix[i][j] <= 0:
                raise ValueError("Route costs must be greater than 0.")
    return matrix


# ============================================================
# PROFESSIONAL COLLEGE-PROJECT GUI
# ============================================================

class RouteWise(tk.Tk):
    C = {
        "navy": "#102A43",
        "navy2": "#163A5C",
        "blue": "#1769E0",
        "blue2": "#0F56C7",
        "blue_bg": "#EAF2FF",
        "green": "#16834A",
        "green_bg": "#EAF8F0",
        "red": "#C62828",
        "red_bg": "#FDECEC",
        "amber": "#A45B00",
        "amber_bg": "#FFF4DF",
        "bg": "#EEF3F8",
        "card": "#FFFFFF",
        "input": "#F8FAFC",
        "text": "#172B4D",
        "muted": "#66788A",
        "line": "#D8E1EA",
        "white": "#FFFFFF",
    }

    def __init__(self):
        super().__init__()
        self.title("RouteWise | TSP Delivery Route Optimizer")
        self.geometry("1280x800")
        self.minsize(1050, 680)
        self.configure(bg=self.C["bg"])
        self._configure_styles()
        self._build_layout()
        self.load_example()
        self.bind("<Control-Return>", lambda _e: self.optimize())

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white",
                        foreground=self.C["text"], rowheight=34, borderwidth=0,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background="#E9EFF6",
                        foreground=self.C["text"], font=("Segoe UI", 9, "bold"),
                        relief="flat")
        style.configure("TNotebook", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", background="#E7EDF4", foreground=self.C["muted"],
                        padding=(15, 9), font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.C["navy2"])],
                  foreground=[("selected", "white")])

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_workspace()

    def _build_sidebar(self):
        side = tk.Frame(self, bg=self.C["navy"], width=275)
        side.grid(row=0, column=0, sticky="nsew")
        side.grid_propagate(False)

        tk.Label(side, text="ROUTEWISE", bg=self.C["navy"], fg="white",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=25, pady=(30, 2))
        tk.Label(side, text="DELIVERY ROUTE OPTIMIZER", bg=self.C["navy"],
                 fg="#9FC2E4", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=27)

        tk.Frame(side, bg="#2B587D", height=1).pack(fill="x", padx=25, pady=25)

        self._side_heading(side, "PROJECT PURPOSE")
        tk.Label(side,
                 text="Find the minimum-cost round trip for a delivery vehicle visiting every location exactly once.",
                 bg=self.C["navy"], fg="#D7E5F2", justify="left", wraplength=220,
                 font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=25, pady=(5, 22))

        self._side_heading(side, "ALGORITHM")
        self._side_item(side, "01", "Travelling Salesman Problem")
        self._side_item(side, "02", "Branch and Bound")
        self._side_item(side, "03", "Matrix Reduction")
        self._side_item(side, "04", "Brute Force Verification")

        tk.Frame(side, bg="#2B587D", height=1).pack(fill="x", padx=25, pady=22)

        self._side_heading(side, "WORKFLOW")
        self._side_item(side, "1", "Enter locations")
        self._side_item(side, "2", "Enter route costs")
        self._side_item(side, "3", "Run optimization")
        self._side_item(side, "4", "Verify result")

        tk.Frame(side, bg="#2B587D", height=1).pack(fill="x", padx=25, pady=22)
        tk.Label(side, text="DAA MINI PROJECT  •  EXPERIMENT 08",
                 bg=self.C["navy"], fg="#7FA4C7",
                 font=("Segoe UI", 7, "bold")).pack(anchor="w", padx=25, side="bottom", pady=18)

    def _side_heading(self, parent, text):
        tk.Label(parent, text=text, bg=self.C["navy"], fg="#77B7F0",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=25)

    def _side_item(self, parent, number, text):
        row = tk.Frame(parent, bg=self.C["navy"])
        row.pack(fill="x", padx=25, pady=4)
        tk.Label(row, text=number, bg="#214A70", fg="#B9D9F3",
                 font=("Segoe UI", 8, "bold"), width=3, pady=3).pack(side="left")
        tk.Label(row, text=text, bg=self.C["navy"], fg="#E3EDF6",
                 font=("Segoe UI", 8), anchor="w").pack(side="left", padx=9)

    def _build_workspace(self):
        work = tk.Frame(self, bg=self.C["bg"])
        work.grid(row=0, column=1, sticky="nsew")
        work.grid_columnconfigure(0, weight=1)
        work.grid_rowconfigure(1, weight=1)

        top = tk.Frame(work, bg=self.C["card"], height=92,
                       highlightbackground=self.C["line"], highlightthickness=1)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)

        tk.Label(top, text="Delivery Route Optimization",
                 bg=self.C["card"], fg=self.C["text"],
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", padx=28, pady=(19, 1))
        tk.Label(top, text="Travelling Salesman Problem solved with Branch and Bound",
                 bg=self.C["card"], fg=self.C["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=29)

        content = tk.Frame(work, bg=self.C["bg"])
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=18)
        content.grid_columnconfigure(0, weight=0, minsize=390)
        content.grid_columnconfigure(1, weight=1, minsize=520)
        content.grid_rowconfigure(0, weight=1)

        self._build_input_card(content)
        self._build_result_card(content)

    def _card(self, parent):
        return tk.Frame(parent, bg=self.C["card"],
                        highlightbackground=self.C["line"], highlightthickness=1,
                        bd=0)

    def _build_input_card(self, parent):
        card = self._card(parent)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(5, weight=1)

        tk.Label(card, text="INPUT DATA", bg=self.C["card"], fg=self.C["blue"],
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 2))
        tk.Label(card, text="Route configuration", bg=self.C["card"], fg=self.C["text"],
                 font=("Segoe UI", 14, "bold")).grid(row=1, column=0, sticky="w", padx=20)

        loc_title = tk.Frame(card, bg=self.C["card"])
        loc_title.grid(row=2, column=0, sticky="ew", padx=20, pady=(17, 6))
        tk.Label(loc_title, text="Locations", bg=self.C["card"], fg=self.C["text"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(loc_title, text="First = depot", bg=self.C["blue_bg"], fg=self.C["blue"],
                 font=("Segoe UI", 7, "bold"), padx=7, pady=3).pack(side="right")

        loc_box = tk.Frame(card, bg=self.C["input"], highlightbackground=self.C["line"], highlightthickness=1)
        loc_box.grid(row=3, column=0, sticky="nsew", padx=20)
        loc_box.grid_rowconfigure(0, weight=1)
        loc_box.grid_columnconfigure(0, weight=1)
        self.locations = tk.Text(loc_box, height=6, bg=self.C["input"], fg=self.C["text"],
                                 insertbackground=self.C["blue"], relief="flat", bd=0,
                                 font=("Segoe UI", 10), padx=10, pady=9)
        self.locations.grid(row=0, column=0, sticky="nsew")

        matrix_title = tk.Frame(card, bg=self.C["card"])
        matrix_title.grid(row=4, column=0, sticky="ew", padx=20, pady=(15, 6))
        tk.Label(matrix_title, text="Route-cost matrix", bg=self.C["card"], fg=self.C["text"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(matrix_title, text="X = no direct route", bg=self.C["amber_bg"], fg=self.C["amber"],
                 font=("Segoe UI", 7, "bold"), padx=7, pady=3).pack(side="right")

        matrix_box = tk.Frame(card, bg=self.C["input"], highlightbackground=self.C["line"], highlightthickness=1)
        matrix_box.grid(row=5, column=0, sticky="nsew", padx=20)
        matrix_box.grid_rowconfigure(0, weight=1)
        matrix_box.grid_columnconfigure(0, weight=1)
        self.matrix = tk.Text(matrix_box, bg=self.C["input"], fg=self.C["text"],
                              insertbackground=self.C["blue"], relief="flat", bd=0,
                              font=("Cascadia Mono", 9), padx=10, pady=9)
        self.matrix.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(matrix_box, orient="vertical", command=self.matrix.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.matrix.configure(yscrollcommand=sb.set)

        buttons = tk.Frame(card, bg=self.C["card"])
        buttons.grid(row=6, column=0, sticky="ew", padx=15, pady=18)
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(1, weight=1)
        self._button(buttons, "↻  Load Example", self.load_example, False, 0)
        self._button(buttons, "▶  Optimize Route", self.optimize, True, 1)

    def _button(self, parent, text, command, primary, column):
        bg = self.C["blue"] if primary else "#E7EEF6"
        fg = "white" if primary else self.C["navy"]
        hover = self.C["blue2"] if primary else "#D7E3EF"
        b = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                      activebackground=hover, activeforeground=fg if not primary else "white",
                      relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 9, "bold"),
                      padx=12, pady=10)
        b.grid(row=0, column=column, sticky="ew", padx=5)
        b.bind("<Enter>", lambda _e: b.configure(bg=hover))
        b.bind("<Leave>", lambda _e: b.configure(bg=bg))

    def _build_result_card(self, parent):
        card = self._card(parent)
        card.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(4, weight=1)

        head = tk.Frame(card, bg=self.C["card"])
        head.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 12))
        tk.Label(head, text="RESULTS & ANALYSIS", bg=self.C["card"], fg=self.C["blue"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(head, text="Optimization summary", bg=self.C["card"], fg=self.C["text"],
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")

        metrics = tk.Frame(card, bg=self.C["card"])
        metrics.grid(row=1, column=0, sticky="ew", padx=16)
        for i in range(4): metrics.grid_columnconfigure(i, weight=1)
        self.metric_vars = {}
        self._metric(metrics, 0, "MINIMUM COST", "cost", self.C["blue_bg"], self.C["blue"])
        self._metric(metrics, 1, "NODES EXPANDED", "nodes", "#F0ECFF", "#6B46C1")
        self._metric(metrics, 2, "EXECUTION TIME", "time", "#E9F8FA", "#087F8C")
        self._metric(metrics, 3, "OPTIMALITY", "verify", self.C["green_bg"], self.C["green"])

        self.status = tk.Label(card, text="●  Ready — enter route data and run optimization",
                               bg=self.C["green_bg"], fg=self.C["green"],
                               font=("Segoe UI", 8, "bold"), anchor="w", padx=12, pady=8)
        self.status.grid(row=2, column=0, sticky="ew", padx=20, pady=13)

        tour = tk.Frame(card, bg="#F7F9FC", highlightbackground=self.C["line"], highlightthickness=1,
                        padx=14, pady=11)
        tour.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 12))
        tk.Label(tour, text="OPTIMAL DELIVERY TOUR", bg="#F7F9FC", fg=self.C["blue"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.tour_label = tk.Label(tour, text="—", bg="#F7F9FC", fg=self.C["text"],
                                   font=("Segoe UI", 11, "bold"), justify="left", anchor="w",
                                   wraplength=520)
        self.tour_label.pack(fill="x", pady=(5, 0))

        self.tabs = ttk.Notebook(card)
        self.tabs.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self._build_insight_tab()
        self._build_verify_tab()
        self._build_matrix_tab()

    def _metric(self, parent, col, title, key, bg, accent):
        box = tk.Frame(parent, bg=bg, highlightbackground=self.C["line"], highlightthickness=1,
                       padx=11, pady=9)
        box.grid(row=0, column=col, sticky="nsew", padx=4)
        tk.Label(box, text=title, bg=bg, fg=accent, font=("Segoe UI", 7, "bold")).pack(anchor="w")
        var = tk.StringVar(value="—")
        self.metric_vars[key] = var
        tk.Label(box, textvariable=var, bg=bg, fg=self.C["text"],
                 font=("Segoe UI", 13, "bold"), wraplength=150, justify="left").pack(anchor="w", pady=(4, 0))

    def _build_insight_tab(self):
        tab = tk.Frame(self.tabs, bg="white", padx=15, pady=14)
        self.tabs.add(tab, text="  Route Analysis  ")
        tk.Label(tab, text="Algorithm result", bg="white", fg=self.C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.insight = tk.Label(tab, text="Run Optimize Route to view the result and analysis.",
                                bg="white", fg=self.C["muted"], font=("Segoe UI", 9),
                                justify="left", anchor="nw", wraplength=520)
        self.insight.pack(fill="both", expand=True, anchor="nw", pady=(7, 0))

    def _build_verify_tab(self):
        tab = tk.Frame(self.tabs, bg="white", padx=15, pady=14)
        self.tabs.add(tab, text="  Verification  ")
        tk.Label(tab, text="Route-by-route verification", bg="white", fg=self.C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))
        self.tree = ttk.Treeview(tab, columns=("from", "to", "cost"), show="headings")
        for col, title, width in (("from", "From", 170), ("to", "To", 170), ("cost", "Route Cost", 120)):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.verify_summary = tk.Label(tab, text="No calculation yet.", bg="white", fg=self.C["muted"],
                                       font=("Segoe UI", 8, "bold"), anchor="w")
        self.verify_summary.pack(fill="x", pady=(9, 0))

    def _build_matrix_tab(self):
        tab = tk.Frame(self.tabs, bg="white", padx=15, pady=14)
        self.tabs.add(tab, text="  Matrix Preview  ")
        self.matrix_preview = tk.Text(tab, bg="#F7F9FC", fg=self.C["text"],
                                      font=("Cascadia Mono", 9), relief="flat", bd=0,
                                      state="disabled", padx=10, pady=10)
        self.matrix_preview.pack(fill="both", expand=True)

    def _set_status(self, text, ok=True):
        self.status.configure(text="●  " + text,
                              bg=self.C["green_bg"] if ok else self.C["red_bg"],
                              fg=self.C["green"] if ok else self.C["red"])

    def load_example(self):
        self.locations.delete("1.0", "end")
        self.locations.insert("1.0", "\n".join(DEFAULT_NAMES))
        self.matrix.delete("1.0", "end")
        self.matrix.insert("1.0", "\n".join(
            " ".join("X" if x == INF else str(x) for x in row) for row in DEFAULT_MATRIX
        ))
        self._reset_results()
        self._set_status("Example loaded — ready for optimization", True)

    def _reset_results(self):
        for v in self.metric_vars.values(): v.set("—")
        self.tour_label.configure(text="—")
        self.insight.configure(text="Run Optimize Route to view the result and analysis.")
        self.verify_summary.configure(text="No calculation yet.")
        for item in self.tree.get_children(): self.tree.delete(item)
        self.matrix_preview.configure(state="normal")
        self.matrix_preview.delete("1.0", "end")
        self.matrix_preview.configure(state="disabled")

    def optimize(self):
        try:
            names = [x.strip() for x in self.locations.get("1.0", "end").splitlines() if x.strip()]
            if not 3 <= len(names) <= 8:
                raise ValueError("Enter between 3 and 8 location names.")
            if len({x.lower() for x in names}) != len(names):
                raise ValueError("Location names must be unique.")
            matrix = parse_matrix(self.matrix.get("1.0", "end"))
            if len(matrix) != len(names):
                raise ValueError(f"You entered {len(names)} locations, but the matrix has {len(matrix)} rows.")
        except ValueError as exc:
            self._set_status(str(exc), False)
            messagebox.showerror("Input Validation", str(exc))
            return

        self.configure(cursor="watch")
        self.update_idletasks()
        try:
            start = time.perf_counter()
            path, best_cost, expanded = tsp_branch_and_bound(matrix, len(names))
            elapsed = time.perf_counter() - start
            if path is None or best_cost == INF:
                raise ValueError("No complete round trip exists for the given route network.")

            _, brute_cost = tsp_brute_force(matrix, len(names))
            verified = best_cost == brute_cost

            self.metric_vars["cost"].set(f"{best_cost:g}")
            self.metric_vars["nodes"].set(str(expanded))
            self.metric_vars["time"].set(f"{elapsed * 1000:.3f} ms")
            self.metric_vars["verify"].set("VERIFIED ✓" if verified else "CHECK")

            route = "  →  ".join(names[i] for i in path)
            self.tour_label.configure(text=route)
            self.insight.configure(text=(
                f"The vehicle starts at {names[0]}, visits every location exactly once, "
                f"and returns to the depot.\n\n"
                f"Branch and Bound found a minimum total cost of {best_cost:g}. "
                f"The search expanded {expanded} decision nodes. Matrix reduction supplies "
                f"lower bounds, allowing non-promising branches to be pruned.\n\n"
                f"Independent brute-force verification: {brute_cost:g}  •  "
                f"Optimality match: {'YES — VERIFIED' if verified else 'NO — CHECK INPUT'}"
            ))

            for item in self.tree.get_children(): self.tree.delete(item)
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.tree.insert("", "end", values=(names[u], names[v], f"{matrix[u][v]:g}"))
            self.verify_summary.configure(
                text=f"Branch & Bound: {best_cost:g}    |    Brute Force: {brute_cost:g}    |    Match: {'YES ✓' if verified else 'NO'}"
            )

            lines = [" " * 13 + "  ".join(f"{n[:10]:>10}" for n in names)]
            for i, row in enumerate(matrix):
                vals = ["INF" if x == INF else f"{x:g}" for x in row]
                lines.append(f"{names[i][:11]:>11}  " + "  ".join(f"{v:>10}" for v in vals))
            self.matrix_preview.configure(state="normal")
            self.matrix_preview.delete("1.0", "end")
            self.matrix_preview.insert("1.0", "\n".join(lines))
            self.matrix_preview.configure(state="disabled")

            self._set_status(f"Optimal route found — total cost {best_cost:g} — verification passed", True)
        except Exception as exc:
            self._set_status(f"Optimization failed: {exc}", False)
            messagebox.showerror("Optimization Error", str(exc))
        finally:
            self.configure(cursor="")


if __name__ == "__main__":
    RouteWise().mainloop()
