import tkinter as tk
from tkinter import ttk
def matrix_chain_order(d):
 n=len(d)-1;m=[[0]*(n+1) for _ in range(n+1)];s=[[0]*(n+1) for _ in range(n+1)]
 for l in range(2,n+1):
  for i in range(1,n-l+2):
   j=i+l-1;m[i][j]=10**18
   for k in range(i,j):
    c=m[i][k]+m[k+1][j]+d[i-1]*d[k]*d[j]
    if c<m[i][j]:m[i][j]=c;s[i][j]=k
 return m,s
def p(s,i,j):return f'A{i}' if i==j else f'({p(s,i,s[i][j])} x {p(s,s[i][j]+1,j)})'
dims=[1024,512,256,128,64];ops=['Resize','Noise Filter','Edge Detection','Compression']
r=tk.Tk();r.title('Image Processing Pipeline Optimizer');r.geometry('1200x700')
tk.Label(r,text='Image Processing Pipeline Optimizer',font=('Arial',22,'bold'),bg='#1565C0',fg='white').pack(fill='x')
t=ttk.Treeview(r,columns=('a','b'),show='headings');t.heading('a',text='Operation');t.heading('b',text='Matrix')
[t.insert('',tk.END,values=(ops[i],f'{dims[i]} x {dims[i+1]}')) for i in range(4)];t.pack(fill='x',padx=20,pady=10)
o=tk.Text(r,font=('Consolas',13));o.pack(fill='both',expand=True,padx=20,pady=10)
def run():
 m,s=matrix_chain_order(dims);n=4;o.delete('1.0','end');o.insert('end',f'Minimum Cost: {m[1][n]}\nOptimal Order: {p(s,1,n)}\n\nDP Cost Table\n')
 [o.insert('end','\t'.join('---' if j<i else str(m[i][j]) for j in range(1,n+1))+'\n') for i in range(1,n+1)]
tk.Button(r,text='Optimize Pipeline',command=run,font=('Arial',15),bg='green',fg='white').pack();run();r.mainloop()
