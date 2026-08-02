
import tkinter as tk
from tkinter import ttk,messagebox
import random

comparison_count=0
def min_max_dc(arr,l,h):
    global comparison_count
    if l==h:return arr[l],arr[l]
    if h==l+1:
        comparison_count+=1
        return (arr[l],arr[h]) if arr[l]<arr[h] else (arr[h],arr[l])
    m=(l+h)//2
    lmn,lmx=min_max_dc(arr,l,m);rmn,rmx=min_max_dc(arr,m+1,h)
    comparison_count+=2
    return (lmn if lmn<rmn else rmn,lmx if lmx>rmx else rmx)
def naive(arr):
    mn=mx=arr[0];c=0
    for x in arr[1:]:
        c+=1
        if x<mn: mn=x
        c+=1
        if x>mx: mx=x
    return mn,mx,c
students=[("Alice",91),("Bob",78),("Charlie",65),("David",99),("Emma",83),("Frank",56),("Grace",88),("Helen",74),("Isha",95),("John",69),("Kevin",81),("Lily",72),("Mia",90),("Noah",61),("Olivia",86)]
def analyze():
    global comparison_count
    vals=[m for _,m in students]
    comparison_count=0
    mn,mx=min_max_dc(vals,0,len(vals)-1);dc=comparison_count
    _,_,nv=naive(vals)
    top=next(s for s in students if s[1]==mx);low=next(s for s in students if s[1]==mn)
    out.config(state="normal");out.delete("1.0","end")
    out.insert("end",f"🏆 TOP SCORER\n{top[0]} - {top[1]} Marks\n\n")
    out.insert("end",f"📉 LOWEST SCORER\n{low[0]} - {low[1]} Marks\n\n")
    out.insert("end",f"Divide & Conquer Comparisons : {dc}\nNaive Comparisons : {nv}\nComparisons Saved : {nv-dc}\n\n")
    out.insert("end","Performance Analysis\nSize\tDC\tNaive\tFormula\n")
    for s in [10,100,1000,10000]:
        arr=[random.randint(1,10000) for _ in range(s)]
        comparison_count=0;min_max_dc(arr,0,s-1);d=comparison_count;_,_,n=naive(arr)
        out.insert("end",f"{s}\t{d}\t{n}\t{3*s//2-2}\n")
    out.config(state="disabled")
r=tk.Tk();r.title("Student Marks Analyzer")
try:r.state("zoomed")
except:r.geometry("1200x700")
r.configure(bg="#eef5ff")
tk.Label(r,text="Student Marks Analyzer",font=("Arial",24,"bold"),bg="#0d47a1",fg="white",pady=12).pack(fill="x")
tree=ttk.Treeview(r,columns=("n","m"),show="headings",height=15)
tree.heading("n",text="Student");tree.heading("m",text="Marks")
for s,m in students: tree.insert("",tk.END,values=(s,m))
tree.pack(fill="x",padx=20,pady=15)
tk.Button(r,text="Analyze Marks",font=("Arial",15,"bold"),bg="#2e7d32",fg="white",command=analyze).pack(pady=10)
out=tk.Text(r,font=("Consolas",14),height=18)
out.pack(fill="both",expand=True,padx=20,pady=15)
analyze()
r.mainloop()
