import time
import customtkinter as ctk
import tkinter as tk
from algorithms.dijkstra import dijkstra
from algorithms.bfs import bfs
from algorithms.astar import astar

BG="#0B0F14"; CARD="#11161C"; GOLD="#FFD22F"; GREEN="#39D98A"; RED="#FF6B6B"
TEXT="#F4F6FA"; MUTED="#9BA9B8"; BORDER="#2A313A"

class GraphCanvas(ctk.CTkFrame):
    """Interactive schematic campus graph with animated highlighted route."""
    def __init__(self, master, on_node_click=None):
        super().__init__(master, fg_color=BG, corner_radius=14, border_width=1, border_color=BORDER)
        self.canvas=tk.Canvas(self,bg=BG,highlightthickness=0,height=330,cursor="hand2")
        self.canvas.pack(fill="both",expand=True,padx=7,pady=7)
        self.canvas.bind("<Configure>",lambda e:self.draw()); self.canvas.bind("<Button-1>",self._click)
        self.graph={}; self.path=[]; self.visible_edges=0; self.start=None; self.end=None; self.positions={}; self.on_node_click=on_node_click
    def set_graph(self,graph,start,end,path,animate=True):
        self.graph=graph; self.start=start; self.end=end; self.path=path or []; self.visible_edges=0 if animate else max(0,len(self.path)-1); self.draw()
        if animate and len(self.path)>1: self._animate_next(0)
    def _animate_next(self,index):
        if index>=len(self.path)-1: return
        self.visible_edges=index+1; self.draw(); self.after(180,lambda:self._animate_next(index+1))
    def _click(self,event):
        if not self.positions:return
        w=max(self.canvas.winfo_width(),650); h=max(self.canvas.winfo_height(),300); closest=None; best=24**2
        for name,(nx,ny) in self.positions.items():
            d=(event.x-nx*w)**2+(event.y-ny*h)**2
            if d<best:closest=name;best=d
        if closest and self.on_node_click:self.on_node_click(closest)
    def draw(self):
        c=self.canvas;c.delete("all");w=max(c.winfo_width(),650);h=max(c.winfo_height(),300)
        c.create_rectangle(0,0,w,h,fill=BG,outline="")
        for x in range(0,w,44):c.create_line(x,0,x,h,fill="#151B22")
        for y in range(0,h,44):c.create_line(0,y,w,y,fill="#151B22")
        pos={"Chandigarh University":(.14,.18),"GCD Dhaliara College":(.20,.38),"Landran":(.32,.36),"Kharar Bus Stand":(.14,.58),"North Country Mall":(.36,.66),"Home (Kharar)":(.48,.83),"Mohali":(.56,.43),"ISB Mohali":(.70,.60),"Shaheed Bhagat Singh Airport":(.83,.83),"Chandigarh":(.77,.29),"PGI Chandigarh":(.90,.18),"Sector 22 Market":(.65,.14),"Elante Mall":(.48,.11),"Sukhna Lake":(.96,.40)}
        for node in self.graph:pos.setdefault(node,(.1+.8*(sum(map(ord,node))%97/97),.1+.8*((sum(map(ord,node))*7)%89/89)))
        self.positions=pos; drawn=set()
        for a,edges in self.graph.items():
            for b,e in edges.items():
                key=tuple(sorted((a,b)))
                if key in drawn or a not in pos or b not in pos:continue
                drawn.add(key); p1=(pos[a][0]*w,pos[a][1]*h);p2=(pos[b][0]*w,pos[b][1]*h)
                path_edge=False
                for i in range(min(self.visible_edges,len(self.path)-1)):
                    if (a,b)==(self.path[i],self.path[i+1]) or (b,a)==(self.path[i],self.path[i+1]):path_edge=True;break
                c.create_line(*p1,*p2,fill=GOLD if path_edge else "#34404B",width=4 if path_edge else 1.2)
                if w>800:
                    mx=(p1[0]+p2[0])/2;my=(p1[1]+p2[1])/2;c.create_text(mx,my,text=f"{e['distance']:.1f}",fill=GOLD if path_edge else "#91A0AF",font=("Segoe UI",7))
        for node,(nx,ny) in pos.items():
            x,y=nx*w,ny*h;color=GREEN if node==self.start else RED if node==self.end else GOLD if node in self.path[:self.visible_edges+1] else "#34404B"
            r=9 if node in (self.start,self.end) else 6 if node in self.path else 5
            c.create_oval(x-r,y-r,x+r,y+r,fill=color,outline="#F7F8FA",width=1)
            label=node.replace("Shaheed Bhagat Singh ","")
            c.create_text(x+10,y-9,text=label,fill=TEXT if node in (self.start,self.end) or node in self.path else "#B8C3CE",anchor="w",font=("Segoe UI",8,"bold" if node in (self.start,self.end) or node in self.path else "normal"))
        c.create_rectangle(10,10,268,35,fill="#151A20",outline="#343B43")
        c.create_oval(19,19,28,28,fill=GREEN,outline="");c.create_text(34,24,text="START",fill=TEXT,anchor="w",font=("Segoe UI",8,"bold"))
        c.create_oval(90,19,99,28,fill=RED,outline="");c.create_text(105,24,text="DESTINATION",fill=TEXT,anchor="w",font=("Segoe UI",8,"bold"))
        c.create_text(12,h-9,text="SCHEMATIC CAMPUS NETWORK · EDGE WEIGHTS ARE SAMPLE ESTIMATES",fill=MUTED,font=("Segoe UI",8),anchor="sw")

class GraphExplorerPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent");self.app=app;self.next_pick="start";self.last_results=[]
        header=ctk.CTkFrame(self,fg_color="transparent");header.pack(fill="x",pady=(0,9))
        ctk.CTkLabel(header,text="Graph Explorer",font=("Segoe UI",25,"bold"),text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(header,text="Choose two locations, compare algorithms, and watch the selected route animate.",text_color=MUTED).pack(anchor="w",pady=(3,0))
        controls=ctk.CTkFrame(self,fg_color=CARD,corner_radius=13,border_width=1,border_color=BORDER);controls.pack(fill="x",pady=(0,8))
        names=list(app.router.base.keys())
        self.start=ctk.StringVar(value="Landran" if "Landran" in names else names[0]);self.end=ctk.StringVar(value="Chandigarh University" if "Chandigarh University" in names else names[-1])
        self.weight=ctk.StringVar(value="distance");self.mode=ctk.StringVar(value="Bike");self.algorithm=ctk.StringVar(value="Dijkstra")
        def label(txt):ctk.CTkLabel(controls,text=txt,text_color=MUTED,font=("Segoe UI",9,"bold")).pack(side="left",padx=(8,3),pady=9)
        label("START");self.start_box=ctk.CTkComboBox(controls,values=names,variable=self.start,width=155,command=self._dropdown_changed);self.start_box.pack(side="left",padx=3,pady=8)
        label("DEST");self.end_box=ctk.CTkComboBox(controls,values=names,variable=self.end,width=155,command=self._dropdown_changed);self.end_box.pack(side="left",padx=3,pady=8)
        label("MODE");ctk.CTkComboBox(controls,values=["Walk","Bike","Car","Bus"],variable=self.mode,width=78,command=lambda _:self.run_algorithm()).pack(side="left",padx=3,pady=8)
        label("OPTIMIZE");ctk.CTkComboBox(controls,values=["distance","time","cost"],variable=self.weight,width=90,command=lambda _:self.run_algorithm()).pack(side="left",padx=3,pady=8)
        label("ALGORITHM");ctk.CTkComboBox(controls,values=["Dijkstra","BFS","A*"],variable=self.algorithm,width=95,command=lambda _:self.run_algorithm()).pack(side="left",padx=3,pady=8)
        ctk.CTkButton(controls,text="Find Route →",command=self.run_algorithm,fg_color=GOLD,hover_color="#E6B91F",text_color="#151515",font=("Segoe UI",10,"bold"),width=105).pack(side="left",padx=5,pady=8)
        ctk.CTkButton(controls,text="Reset",command=self.reset_selection,fg_color="#29313A",hover_color="#394653",text_color=TEXT,width=58).pack(side="left",padx=3,pady=8)
        self.pick_label=ctk.CTkLabel(controls,text="NEXT: START",text_color=GOLD,font=("Segoe UI",9,"bold"));self.pick_label.pack(side="right",padx=10)
        self.graph_canvas=GraphCanvas(self,on_node_click=self.select_node);self.graph_canvas.pack(fill="both",expand=True)
        bottom=ctk.CTkFrame(self,fg_color="transparent");bottom.pack(fill="x",pady=(8,0))
        self.summary=ctk.CTkFrame(bottom,fg_color=CARD,corner_radius=12,border_width=1,border_color=BORDER);self.summary.pack(side="left",fill="both",expand=True,padx=(0,6))
        self.steps=ctk.CTkFrame(bottom,fg_color=CARD,corner_radius=12,border_width=1,border_color=BORDER);self.steps.pack(side="left",fill="both",expand=True,padx=(6,0))
        self.run_algorithm()
    def _dropdown_changed(self,_=None):self.next_pick="start";self._update_pick_label();self.run_algorithm()
    def _update_pick_label(self):self.pick_label.configure(text=f"NEXT: {self.next_pick.upper()}")
    def reset_selection(self):
        names=list(self.app.router.base.keys());self.start.set(names[0]);self.end.set(names[1] if len(names)>1 else names[0]);self.next_pick="start";self._update_pick_label();self.run_algorithm()
    def select_node(self,node):
        if self.next_pick=="start":
            if node==self.end.get():self.app.notify("Choose another start","Start and destination must be different.");return
            self.start.set(node);self.next_pick="destination"
        else:
            if node==self.start.get():self.app.notify("Choose another destination","Start and destination must be different.");return
            self.end.set(node);self.next_pick="start"
        self._update_pick_label();self.run_algorithm()
    def refresh_graph(self):self.run_algorithm()
    def _metrics(self,graph,path):
        dist=mins=cost=0.0
        for a,b in zip(path,path[1:]):
            e=graph[a][b];dist+=float(e.get("distance",0));mins+=float(e.get("time",0));cost+=float(e.get("cost",0))
        return dist,mins,cost
    def run_algorithm(self):
        try:
            start=self.start.get().strip();end=self.end.get().strip();weight=self.weight.get();mode=self.mode.get()
            if not start or not end:self.app.notify("Missing location","Choose a start and destination.");return
            if start==end:self.app.notify("Invalid route","Start and destination must be different.");return
            graph=self.app.router.graph(mode)
            algorithms={"Dijkstra":lambda:dijkstra(graph,start,end,weight),"BFS":lambda:bfs(graph,start,end),"A*":lambda:astar(graph,start,end,weight)}
            comparisons=[]
            for name,fn in algorithms.items():
                t0=time.perf_counter();result=fn();elapsed=(time.perf_counter()-t0)*1000
                if result:
                    path=result["path"];dist,mins,cost=self._metrics(graph,path)
                    comparisons.append({"name":name,"path":path,"distance":dist,"minutes":mins,"cost":cost,"visited":result.get("visited_nodes",0),"ms":elapsed,"weight":result.get("weight",0)})
            selected=next((r for r in comparisons if r["name"]==self.algorithm.get()),None)
            if not selected:self.app.notify("No route","No connected path exists between these locations.");return
            self.last_results=comparisons;self.graph_canvas.set_graph(graph,start,end,selected["path"],animate=True)
            for panel in (self.summary,self.steps):
                for child in panel.winfo_children():child.destroy()
            dist,mins,cost=selected["distance"],selected["minutes"],selected["cost"]
            ctk.CTkLabel(self.summary,text=f"{self.algorithm.get().upper()} ROUTE RESULT",text_color=GOLD,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(9,3))
            ctk.CTkLabel(self.summary,text=f"{dist:.1f} km  ·  {round(mins)} min  ·  ₹{cost:.0f}",text_color=TEXT,font=("Segoe UI",16,"bold")).pack(anchor="w",padx=13)
            ctk.CTkLabel(self.summary,text=f"{selected['visited']} nodes visited  ·  {selected['ms']:.3f} ms  ·  {mode}",text_color=MUTED,font=("Segoe UI",9)).pack(anchor="w",padx=13,pady=(2,4))
            ctk.CTkLabel(self.summary,text="STEP-BY-STEP DIRECTIONS",text_color=GOLD,font=("Segoe UI",9,"bold")).pack(anchor="w",padx=13,pady=(3,2))
            directions="\n".join(f"{i+1}. {a} → {b}" for i,(a,b) in enumerate(zip(selected["path"],selected["path"][1:]))) or f"You are already at {start}."
            ctk.CTkLabel(self.summary,text=directions,wraplength=500,justify="left",text_color="#C1CAD3",font=("Segoe UI",9)).pack(anchor="w",padx=13,pady=(0,8))
            ctk.CTkLabel(self.steps,text="ALGORITHM COMPARISON",text_color=GOLD,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(9,4))
            ctk.CTkLabel(self.steps,text="Algorithm     Distance     Stops     Visited     Time",text_color=MUTED,font=("Consolas",9,"bold")).pack(anchor="w",padx=13)
            for r in comparisons:
                marker="▶ " if r["name"]==self.algorithm.get() else "   "
                row=f"{marker}{r['name']:<9} {r['distance']:>6.1f} km  {len(r['path'])-1:>3}       {r['visited']:>3}     {r['ms']:.3f}ms"
                ctk.CTkLabel(self.steps,text=row,text_color=GOLD if r["name"]==self.algorithm.get() else TEXT,font=("Consolas",9),anchor="w").pack(anchor="w",padx=13,pady=2)
            note="BFS minimizes number of edges, not distance. Dijkstra and A* optimize the selected weight."
            ctk.CTkLabel(self.steps,text=note,text_color=MUTED,font=("Segoe UI",9),wraplength=500,justify="left").pack(anchor="w",padx=13,pady=(6,2))
            ctk.CTkLabel(self.steps,text="Sample estimates only — not live traffic or verified road data.",text_color=GOLD,font=("Segoe UI",9)).pack(anchor="w",padx=13,pady=(2,8))
        except Exception as exc:self.app.notify("Route calculation error",str(exc))
