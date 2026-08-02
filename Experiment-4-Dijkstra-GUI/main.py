
import tkinter as tk
from tkinter import ttk,messagebox
import heapq

graph={
"City Hospital":[("Railway Station",4),("Bus Stand",2)],
"Railway Station":[("Shopping Mall",5),("Accident Spot",9)],
"Bus Stand":[("Shopping Mall",3),("Green Park",4)],
"Green Park":[("Accident Spot",6)],
"Shopping Mall":[("Accident Spot",2),("School",4)],
"School":[("Accident Spot",3)],
"Accident Spot":[]
}
def dijkstra(g,s):
 d={n:float("inf") for n in g};p={n:None for n in g};d[s]=0;h=[(0,s)];v=set()
 while h:
  _,u=heapq.heappop(h)
  if u in v: continue
  v.add(u)
  for x,w in g[u]:
   if d[u]+w<d[x]:
    d[x]=d[u]+w;p[x]=u;heapq.heappush(h,(d[x],x))
 return d,p
def path(prev,s,t):
 r=[];n=t
 while n is not None:r.append(n);n=prev[n]
 r=r[::-1]
 return r if r and r[0]==s else []
def run():
 s=src.get();t=dst.get()
 if s==t: messagebox.showerror("Input","Choose different locations.");return
 d,p=dijkstra(graph,s);pa=path(p,s,t)
 out.delete("1.0","end")
 if not pa: out.insert("end","No route available.");return
 out.insert("end",f"🚑 EMERGENCY ROUTE\n\nHospital : {s}\nEmergency : {t}\n\nFastest Route:\n")
 out.insert("end"," → ".join(pa))
 out.insert("end",f"\n\nEstimated Travel Time : {d[t]} minutes\n")
 out.insert("end","\nStatus: Route calculated successfully using Dijkstra's Algorithm.")
root=tk.Tk();root.title("Emergency Ambulance Route Finder")
try: root.state("zoomed")
except: root.geometry("1200x700")
root.configure(bg="#eaf4ff")
tk.Label(root,text="Emergency Ambulance Route Finder",font=("Arial",24,"bold"),bg="#1565c0",fg="white",pady=15).pack(fill="x")
f=tk.Frame(root,bg="#eaf4ff");f.pack(pady=25)
loc=list(graph.keys())
tk.Label(f,text="Hospital",font=("Arial",15),bg="#eaf4ff").grid(row=0,column=0,padx=10,pady=10)
src=ttk.Combobox(f,values=loc,font=("Arial",14),state="readonly",width=28);src.current(0);src.grid(row=0,column=1)
tk.Label(f,text="Emergency Location",font=("Arial",15),bg="#eaf4ff").grid(row=1,column=0,padx=10,pady=10)
dst=ttk.Combobox(f,values=loc,font=("Arial",14),state="readonly",width=28);dst.current(len(loc)-1);dst.grid(row=1,column=1)
tk.Button(root,text="Find Fastest Route",font=("Arial",15,"bold"),bg="#2e7d32",fg="white",command=run).pack(pady=10)
out=tk.Text(root,font=("Consolas",15),height=18,width=80,bg="white")
out.pack(padx=30,pady=20,fill="both",expand=True)
run()
root.mainloop()
