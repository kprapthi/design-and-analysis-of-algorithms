
import tkinter as tk
from tkinter import messagebox,scrolledtext
import random
def naive_search(text, pattern):
    n,m=len(text),len(pattern);matches=[];c=0
    for i in range(n-m+1):
        j=0
        while j<m:
            c+=1
            if text[i+j]!=pattern[j]: break
            j+=1
        if j==m: matches.append(i)
    return matches,c
def compute_lps(pattern):
    m=len(pattern);lps=[0]*m;length=0;i=1
    while i<m:
        if pattern[i]==pattern[length]:
            length+=1;lps[i]=length;i+=1
        elif length!=0:length=lps[length-1]
        else:lps[i]=0;i+=1
    return lps
def kmp_search(text,pattern):
    n,m=len(text),len(pattern);lps=compute_lps(pattern);matches=[];c=0;i=j=0
    while i<n:
        c+=1
        if pattern[j]==text[i]: i+=1;j+=1
        if j==m: matches.append(i-j);j=lps[j-1]
        elif i<n and pattern[j]!=text[i]:
            if j!=0:j=lps[j-1]
            else:i+=1
    return matches,c
def rabin_karp(text,pattern,q=101):
    n,m=len(text),len(pattern);d=256
    h=pow(d,m-1,q);ph=th=0;matches=[];c=0
    for i in range(m):
        ph=(d*ph+ord(pattern[i]))%q;th=(d*th+ord(text[i]))%q
    for s in range(n-m+1):
        if ph==th:
            for k in range(m):
                c+=1
                if text[s+k]!=pattern[k]:break
            else:matches.append(s)
        if s<n-m:
            th=(d*(th-ord(text[s])*h)+ord(text[s+m]))%q
            if th<0: th+=q
    return matches,c
def run():
    t=e1.get();p=e2.get()
    if not t or not p: messagebox.showerror("Error","Enter both Text and Pattern");return
    if len(p)>len(t): messagebox.showerror("Error","Pattern longer than text");return
    out.delete("1.0","end")
    for name,f in [("Naive",naive_search),("KMP",kmp_search),("Rabin-Karp",rabin_karp)]:
        m,c=f(t,p);out.insert("end",f"{name}: Matches={m} Comparisons={c}\n")
    tl=''.join(random.choices("ABCD",k=10000));patterns=['AB','ABCD','ABCDAB','ABCDABCD']
    out.insert("end","\nPattern\tNaive\tKMP\tRK\n")
    for pp in patterns:
        _,a=naive_search(tl,pp);_,b=kmp_search(tl,pp);_,cc=rabin_karp(tl,pp)
        out.insert("end",f"{pp}\t{a}\t{b}\t{cc}\n")
root=tk.Tk();root.title("String Matching Comparison")
tk.Label(root,text="Text").pack();e1=tk.Entry(root,width=60);e1.pack()
tk.Label(root,text="Pattern").pack();e2=tk.Entry(root,width=60);e2.pack()
tk.Button(root,text="Run Analysis",command=run).pack(pady=5)
out=scrolledtext.ScrolledText(root,width=80,height=20);out.pack()
root.mainloop()
