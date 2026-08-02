import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            return (low, comparisons) if arr[low] == target else (-1, comparisons)
        if arr[high] == arr[low]:
            return (low, comparisons) if arr[low] == target else (-1, comparisons)
        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1, comparisons

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []
    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        start = time.perf_counter()
        for _ in range(100):
            _, is_comp = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            _, bs_comp = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append((size, is_time, bs_time, is_comp, bs_comp))
    return results

def run_search():
    try:
        arr = list(map(int, entry_array.get().split(",")))
        target = int(entry_target.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter comma-separated integers and a valid target.")
        return

    if arr != sorted(arr):
        messagebox.showerror("Invalid Array", "Interpolation Search requires a sorted array.")
        return

    index, comparisons = interpolation_search(arr, target)
    result_label.config(
        text=(f"Target {target} found at index {index}." if index != -1
              else f"Target {target} was not found.")
        + f"\nComparisons: {comparisons}"
    )

def run_performance():
    performance_table.delete(*performance_table.get_children())
    for size, is_time, bs_time, is_comp, bs_comp in performance_analysis():
        performance_table.insert("", "end",
            values=(size, f"{is_time:.4f}", f"{bs_time:.4f}", is_comp, bs_comp))

root = tk.Tk()
root.title("Interpolation Search - Performance Analysis")
root.geometry("950x650")
root.resizable(False, False)

ttk.Label(root, text="Interpolation Search",
          font=("Segoe UI", 22, "bold")).pack(pady=(20, 5))
ttk.Label(root, text="Implementation and Performance Analysis",
          font=("Segoe UI", 11)).pack(pady=(0, 20))

search_frame = ttk.LabelFrame(root, text="Search")
search_frame.pack(fill="x", padx=30, pady=10)

ttk.Label(search_frame, text="Sorted Array:").grid(row=0, column=0, padx=10, pady=15, sticky="w")
entry_array = ttk.Entry(search_frame, width=75)
entry_array.insert(0, "2,5,10,15,23,35,48,60,75,90,105,120")
entry_array.grid(row=0, column=1, padx=10, pady=15)

ttk.Label(search_frame, text="Target:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_target = ttk.Entry(search_frame, width=20)
entry_target.insert(0, "35")
entry_target.grid(row=1, column=1, padx=10, pady=10, sticky="w")

ttk.Button(search_frame, text="Search", command=run_search).grid(row=2, column=1, padx=10, pady=15, sticky="w")

result_label = ttk.Label(search_frame, text="Enter values and click Search.", font=("Segoe UI", 11))
result_label.grid(row=3, column=1, padx=10, pady=(0, 15), sticky="w")

performance_frame = ttk.LabelFrame(root, text="Performance Comparison")
performance_frame.pack(fill="both", expand=True, padx=30, pady=15)

columns=("size","is_time","bs_time","is_comp","bs_comp")
performance_table=ttk.Treeview(performance_frame, columns=columns, show="headings", height=8)
headers={"size":"Input Size","is_time":"Interpolation Time (ms)","bs_time":"Binary Time (ms)",
         "is_comp":"IS Comparisons","bs_comp":"BS Comparisons"}

for col in columns:
    performance_table.heading(col, text=headers[col])
    performance_table.column(col, width=100 if col=="size" else 170, anchor="center")

performance_table.pack(padx=15, pady=15)
ttk.Button(performance_frame, text="Run Performance Analysis",
           command=run_performance).pack(pady=(0, 15))

root.mainloop()
