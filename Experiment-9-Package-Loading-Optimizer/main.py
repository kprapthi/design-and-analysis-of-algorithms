import tkinter as tk
from tkinter import ttk, messagebox
import time
import math

# ---------- Original DAA Algorithms ----------
def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []
    for item in items:
        placed = False
        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break
        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])
    return bin_contents


def first_fit_decreasing(items, capacity=1.0):
    return first_fit(sorted(items, reverse=True), capacity)


def best_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)
    bins = []
    bin_contents = []
    for item in sorted_items:
        best_idx = -1
        best_space = float("inf")
        for i, space in enumerate(bins):
            if space >= item and space - item < best_space:
                best_space = space - item
                best_idx = i
        if best_idx >= 0:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])
    return bin_contents


class PackingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Package Loading Optimizer")
        self.geometry("1180x760")
        self.minsize(920, 620)
        self.configure(bg="#0f172a")

        self.items_var = tk.StringVar(
            value="0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5"
        )
        self.capacity_var = tk.StringVar(value="1.0")
        self.status_var = tk.StringVar(value="Ready")
        self.total_var = tk.StringVar(value="—")
        self.lower_var = tk.StringVar(value="—")
        self.best_var = tk.StringVar(value="—")
        self.waste_var = tk.StringVar(value="—")

        self.results = {}
        self.current_method = "Best Fit Decreasing"

        self.setup_style()
        self.build_ui()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(13, 9))
        style.configure("TEntry", font=("Segoe UI", 11), padding=7)
        style.configure(
            "Treeview", rowheight=34, font=("Segoe UI", 10),
            background="#111827", fieldbackground="#111827",
            foreground="#e5e7eb"
        )
        style.configure(
            "Treeview.Heading", font=("Segoe UI", 10, "bold"),
            background="#1e293b", foreground="#f8fafc"
        )

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = tk.Frame(self, bg="#111827", padx=28, pady=20)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        tk.Label(
            header, text="Package Loading Optimizer",
            bg="#111827", fg="#f8fafc",
            font=("Segoe UI", 23, "bold")
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header, text="Compare approximation strategies for packing packages into fixed-capacity containers",
            bg="#111827", fg="#94a3b8",
            font=("Segoe UI", 10)
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        actions = tk.Frame(header, bg="#111827")
        actions.grid(row=0, column=1, rowspan=2, sticky="e")
        ttk.Button(actions, text="Optimize", command=self.optimize).pack(side="left", padx=5)
        ttk.Button(actions, text="Reset", command=self.reset).pack(side="left", padx=5)

        body = tk.Frame(self, bg="#0f172a", padx=24, pady=20)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(1, weight=1)

        input_panel = tk.Frame(body, bg="#111827", padx=18, pady=18)
        input_panel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        input_panel.grid_columnconfigure(1, weight=1)

        tk.Label(input_panel, text="Input", bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

        tk.Label(input_panel, text="Package sizes", bg="#111827", fg="#cbd5e1",
                 font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(12, 0))
        self.items_entry = ttk.Entry(input_panel, textvariable=self.items_var)
        self.items_entry.grid(row=1, column=1, sticky="ew", padx=12, pady=(12, 0))
        tk.Label(input_panel, text="e.g. 0.5, 0.7, 0.3", bg="#111827", fg="#64748b",
                 font=("Segoe UI", 9)).grid(row=1, column=2, sticky="w", pady=(12, 0))

        tk.Label(input_panel, text="Container capacity", bg="#111827", fg="#cbd5e1",
                 font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", pady=10)
        self.capacity_entry = ttk.Entry(input_panel, textvariable=self.capacity_var, width=14)
        self.capacity_entry.grid(row=2, column=1, sticky="w", padx=12, pady=10)
        tk.Label(input_panel, text="Each package must fit within this capacity",
                 bg="#111827", fg="#64748b", font=("Segoe UI", 9)).grid(
                     row=2, column=2, sticky="w")

        cards = tk.Frame(body, bg="#0f172a")
        cards.grid(row=0, column=2, sticky="nsew", padx=(12, 0))
        self._card(cards, 0, "TOTAL LOAD", self.total_var)
        self._card(cards, 1, "LOWER BOUND", self.lower_var)
        self._card(cards, 2, "BEST RESULT", self.best_var)
        self._card(cards, 3, "UNUSED SPACE", self.waste_var)

        left = tk.Frame(body, bg="#111827", padx=18, pady=18)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left.grid_rowconfigure(2, weight=1)
        left.grid_columnconfigure(0, weight=1)

        tk.Label(left, text="Algorithm Comparison", bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(left, text="Fewer containers and less unused capacity are better.",
                 bg="#111827", fg="#94a3b8", font=("Segoe UI", 9)).grid(
                     row=1, column=0, sticky="w", pady=(3, 12))

        table_frame = tk.Frame(left, bg="#111827")
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("method", "bins", "util", "time"),
            show="headings"
        )
        for col, heading in [
            ("method", "Method"), ("bins", "Containers"),
            ("util", "Utilization"), ("time", "Time")
        ]:
            self.tree.heading(col, text=heading)
        self.tree.column("method", width=170)
        self.tree.column("bins", width=85, anchor="center")
        self.tree.column("util", width=100, anchor="center")
        self.tree.column("time", width=100, anchor="center")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        right = tk.Frame(body, bg="#111827", padx=18, pady=18)
        right.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(10, 0))
        right.grid_rowconfigure(2, weight=1)
        right.grid_columnconfigure(0, weight=1)

        tk.Label(right, text="Loading Plan", bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 15, "bold")).grid(row=0, column=0, sticky="w")

        selector = tk.Frame(right, bg="#111827")
        selector.grid(row=1, column=0, sticky="ew", pady=(8, 12))
        tk.Label(selector, text="View:", bg="#111827", fg="#cbd5e1",
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        self.method_box = ttk.Combobox(
            selector,
            values=["First Fit", "First Fit Decreasing", "Best Fit Decreasing"],
            state="readonly", width=25
        )
        self.method_box.set("Best Fit Decreasing")
        self.method_box.pack(side="left", padx=8)
        self.method_box.bind("<<ComboboxSelected>>", lambda e: self.show_plan())

        plan_frame = tk.Frame(right, bg="#111827")
        plan_frame.grid(row=2, column=0, sticky="nsew")
        plan_frame.grid_rowconfigure(0, weight=1)
        plan_frame.grid_columnconfigure(0, weight=1)

        self.plan_text = tk.Text(
            plan_frame, wrap="none",
            bg="#0b1220", fg="#cbd5e1",
            insertbackground="#fff", relief="flat",
            font=("Consolas", 10), padx=14, pady=12
        )
        self.plan_text.grid(row=0, column=0, sticky="nsew")
        yscroll = ttk.Scrollbar(plan_frame, orient="vertical", command=self.plan_text.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.plan_text.configure(yscrollcommand=yscroll.set)

        footer = tk.Frame(self, bg="#0b1220", padx=24, pady=8)
        footer.grid(row=2, column=0, sticky="ew")
        tk.Label(footer, textvariable=self.status_var, bg="#0b1220", fg="#94a3b8",
                 font=("Segoe UI", 9)).pack(side="left")
        tk.Label(footer, text="DAA core: FF • FFD • BFD approximation strategies",
                 bg="#0b1220", fg="#64748b", font=("Segoe UI", 9)).pack(side="right")

    def _card(self, parent, row, title, variable):
        card = tk.Frame(parent, bg="#111827", padx=14, pady=10)
        card.grid(row=row, column=0, sticky="ew", pady=3)
        tk.Label(card, text=title, bg="#111827", fg="#64748b",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(card, textvariable=variable, bg="#111827", fg="#f8fafc",
                 font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(2, 0))

    def parse_input(self):
        raw = self.items_var.get().strip()
        if not raw:
            raise ValueError("Enter at least one package size.")
        try:
            items = [float(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            raise ValueError("Package sizes must be numbers separated by commas.")

        try:
            capacity = float(self.capacity_var.get().strip())
        except ValueError:
            raise ValueError("Container capacity must be a number.")

        if capacity <= 0:
            raise ValueError("Container capacity must be greater than zero.")
        if not items:
            raise ValueError("Enter at least one package size.")
        if any(x <= 0 for x in items):
            raise ValueError("Package sizes must be greater than zero.")
        if any(x > capacity for x in items):
            raise ValueError("Every package must be less than or equal to the container capacity.")
        if len(items) > 200:
            raise ValueError("Use at most 200 package sizes for this mini-project.")

        return items, capacity

    def optimize(self):
        try:
            items, capacity = self.parse_input()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.status_var.set("Optimizing loading plans...")
        self.update_idletasks()

        methods = [
            ("First Fit", first_fit),
            ("First Fit Decreasing", first_fit_decreasing),
            ("Best Fit Decreasing", best_fit_decreasing),
        ]

        self.results.clear()
        for name, func in methods:
            start = time.perf_counter()
            bins = func(items, capacity)
            elapsed = time.perf_counter() - start
            self.results[name] = (bins, elapsed)

        total = sum(items)
        lower_bound = math.ceil(total / capacity - 1e-12)
        best_count = min(len(v[0]) for v in self.results.values())
        best_method = next(k for k, v in self.results.items() if len(v[0]) == best_count)

        best_bins = self.results[best_method][0]
        unused = best_count * capacity - total
        utilization = total / (best_count * capacity) * 100

        self.total_var.set(f"{total:.2f}")
        self.lower_var.set(str(lower_bound))
        self.best_var.set(f"{best_count} ({best_method})")
        self.waste_var.set(f"{unused:.2f}  ({utilization:.1f}% used)")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, (bins, elapsed) in self.results.items():
            util = total / (len(bins) * capacity) * 100
            self.tree.insert(
                "", "end",
                values=(name, len(bins), f"{util:.1f}%", f"{elapsed * 1000:.3f} ms")
            )

        self.show_plan()
        self.status_var.set("Optimization complete.")

    def show_plan(self):
        if not self.results:
            return
        method = self.method_box.get()
        if method not in self.results:
            return

        bins, elapsed = self.results[method]
        try:
            items, capacity = self.parse_input()
        except ValueError:
            return

        total = sum(items)
        self.plan_text.delete("1.0", "end")
        self.plan_text.insert(
            "end",
            f"{method}\n"
            f"{'=' * 72}\n"
            f"Containers required: {len(bins)}    "
            f"Capacity: {capacity:g}    "
            f"Execution: {elapsed * 1000:.3f} ms\n\n"
        )

        for i, contents in enumerate(bins, 1):
            used = sum(contents)
            remaining = capacity - used
            util = used / capacity * 100
            sizes = ", ".join(f"{x:g}" for x in contents)
            bar_len = max(0, min(40, round(util / 2.5)))
            bar = "█" * bar_len + "░" * (40 - bar_len)
            self.plan_text.insert(
                "end",
                f"Container {i:>3}: [{sizes}]\n"
                f"             Used {used:.2f} / {capacity:g}  |  "
                f"Remaining {remaining:.2f}  |  {util:.1f}%\n"
                f"             {bar}\n\n"
            )

    def reset(self):
        self.items_var.set("0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5")
        self.capacity_var.set("1.0")
        self.results.clear()
        self.total_var.set("—")
        self.lower_var.set("—")
        self.best_var.set("—")
        self.waste_var.set("—")
        self.status_var.set("Ready")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.plan_text.delete("1.0", "end")
        self.plan_text.insert("1.0", "Enter package sizes and click Optimize.")


if __name__ == "__main__":
    app = PackingApp()
    app.mainloop()
