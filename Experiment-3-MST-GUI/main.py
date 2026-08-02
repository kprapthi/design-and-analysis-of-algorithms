
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import heapq

class UnionFind:
    def __init__(self,n):
        self.parent=list(range(n)); self.rank=[0]*n
    def find(self,x):
        if self.parent[x]!=x: self.parent[x]=self.find(self.parent[x])
        return self.parent[x]
    def union(self,x,y):
        rx,ry=self.find(x),self.find(y)
        if rx==ry: return False
        if self.rank[rx]<self.rank[ry]: rx,ry=ry,rx
        self.parent[ry]=rx
        if self.rank[rx]==self.rank[ry]: self.rank[rx]+=1
        return True

def kruskal(n,edges):
    uf=UnionFind(n); mst=[]; cost=0
    for w,u,v in sorted(edges):
        if uf.union(u,v):
            mst.append((u,v,w)); cost+=w
    return mst,cost

def prim(n,adj):
    key=[10**9]*n; parent=[-1]*n; vis=[False]*n
    pq=[(0,0)]; key[0]=0; mst=[]; cost=0
    while pq:
        w,u=heapq.heappop(pq)
        if vis[u]: continue
        vis[u]=True
        if parent[u]!=-1:
            mst.append((parent[u],u,w)); cost+=w
        for v,wt in adj.get(u,[]):
            if not vis[v] and wt<key[v]:
                key[v]=wt; parent[v]=u
                heapq.heappush(pq,(wt,v))
    return mst,cost

def run():
    try:
        n=int(vertices.get())
        edges=[]; adj={}
        for line in edgebox.get("1.0","end").strip().splitlines():
            w,u,v=map(int,line.split())
            edges.append((w,u,v))
            adj.setdefault(u,[]).append((v,w))
            adj.setdefault(v,[]).append((u,w))
    except:
        messagebox.showerror("Invalid Input","Enter vertices and edges as:\nweight u v")
        return
    output.delete("1.0","end")
    for title,(mst,cost) in [("Kruskal",kruskal(n,edges)),("Prim",prim(n,adj))]:
        output.insert("end",f"{title}'s Minimum Spanning Tree\n")
        output.insert("end","-"*38+"\n")
        for u,v,w in mst:
            output.insert("end",f"Edge ({u} - {v})   Weight = {w}\n")
        output.insert("end",f"\nTotal MST Cost = {cost}\n\n")

root=tk.Tk()
root.title("Minimum Spanning Tree Visualizer")
root.geometry("760x620")
root.resizable(False,False)

ttk.Label(root,text="Minimum Spanning Tree using Kruskal's and Prim's Algorithms",
          font=("Segoe UI",14,"bold")).pack(pady=10)

frm=ttk.Frame(root,padding=10); frm.pack(fill="x")

ttk.Label(frm,text="Number of Vertices:").grid(row=0,column=0,sticky="w")
vertices=ttk.Entry(frm,width=10)
vertices.insert(0,"7")
vertices.grid(row=0,column=1,padx=5)

ttk.Label(frm,text="Enter Edges (weight u v):").grid(row=1,column=0,columnspan=2,sticky="w",pady=(10,5))

edgebox=scrolledtext.ScrolledText(frm,width=55,height=10,font=("Consolas",10))
edgebox.grid(row=2,column=0,columnspan=2)
edgebox.insert("end","7 0 1\n5 0 3\n8 1 2\n9 1 3\n7 1 4\n5 2 4\n15 3 4\n6 3 5\n8 4 5\n9 4 6\n11 5 6")

ttk.Button(root,text="Run MST Algorithms",command=run).pack(pady=10)

ttk.Label(root,text="Results",font=("Segoe UI",11,"bold")).pack()

output=scrolledtext.ScrolledText(root,width=85,height=16,font=("Consolas",10))
output.pack(padx=10,pady=5)

root.mainloop()
