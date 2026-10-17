import customtkinter as ctk
import tkinter as tk
import math
from components.location_selector import LocationSelector
from components.route_card import RouteCard

class OfflineRouteMap(ctk.CTkFrame):
    """Stylized offline road-map canvas. All artwork is drawn locally; no network/API needed."""
    def __init__(self, master):
        super().__init__(master, fg_color="#10151B", corner_radius=14, border_width=1, border_color="#2A313A")
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=12, pady=(9,0))
        ctk.CTkLabel(bar, text="ROUTE MAP  /  OFFLINE PREVIEW", text_color="#FFD22F",
                     font=("Segoe UI", 10, "bold")).pack(side="left")
        self.zoom = 1.0
        ctk.CTkButton(bar, text="−", width=28, height=25, fg_color="#272D34",
                      command=lambda:self.change_zoom(.85)).pack(side="right", padx=2)
        ctk.CTkButton(bar, text="+", width=28, height=25, fg_color="#272D34",
                      command=lambda:self.change_zoom(1.18)).pack(side="right", padx=2)
        self.canvas = tk.Canvas(self, bg="#102F4A", highlightthickness=0, height=255)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", lambda e:self.draw())
        self.start_name, self.end_name = "College", "Home"
        self.path = []
        self.draw()
    def change_zoom(self, factor):
        self.zoom = max(.75, min(1.65, self.zoom*factor)); self.draw()
    def set_route(self, start, end, path=None):
        self.start_name, self.end_name = start, end
        self.path = path or []
        self.draw()
    def draw(self):
        c=self.canvas
        c.delete("all")
        w=max(c.winfo_width(),420); h=max(c.winfo_height(),220)
        c.create_rectangle(0,0,w,h,fill="#102F4A",outline="")
        # park / green areas
        parks=[(.04,.10,.23,.30),(.70,.08,.94,.24),(.07,.72,.25,.91),(.75,.69,.96,.91),(.38,.38,.53,.54)]
        for x1,y1,x2,y2 in parks:
            c.create_oval(x1*w,y1*h,x2*w,y2*h,fill="#164A4C",outline="")
        # block grid / minor streets
        spacing=max(28,int(46*self.zoom))
        for x in range(-20,w+spacing,spacing):
            c.create_line(x,0,x,h,fill="#28506A",width=2)
        for y in range(-20,h+spacing,spacing):
            c.create_line(0,y,w,y,fill="#28506A",width=2)
        # major roads
        roads=[[(0,.26),(w*.24,.31),(w*.48,.25),(w*.75,.32),(w,.22)],
               [(0,.63),(w*.22,.58),(w*.49,.67),(w*.76,.57),(w,.66)],
               [(w*.18,0),(w*.26,h*.26),(w*.38,h*.51),(w*.30,h),(w*.30,h)],
               [(w*.69,0),(w*.63,h*.28),(w*.70,h*.52),(w*.62,h)]]
        for pts in roads:
            coords=[]
            for x,y in pts: coords.extend([x,y])
            c.create_line(*coords,fill="#547086",width=5,smooth=True)
            c.create_line(*coords,fill="#7991A2",width=1,smooth=True)
        # local road / route line
        start=(w*.18,h*.22); end=(w*.80,h*.76)
        route=[start,(w*.28,h*.34),(w*.43,h*.40),(w*.49,h*.53),(w*.65,h*.49),(w*.72,h*.64),end]
        if self.path and len(self.path)>1:
            # deterministic waypoint shifts based on route labels
            seed=sum(ord(ch) for ch in (self.start_name+self.end_name))
            route=[start]
            for i in range(1,6):
                x=w*(.18+.62*i/6); y=h*(.22+.54*i/6)+math.sin(i+seed%5)*h*.07
                route.append((x,y))
            route.append(end)
        flat=[v for point in route for v in point]
        c.create_line(*flat,fill="#06182A",width=10,smooth=True)
        c.create_line(*flat,fill="#FFD22F",width=5,smooth=True)
        # endpoint pins
        for (x,y),col,label,anchor in [(start,"#39D98A",self.start_name,"nw"),(end,"#FB7185",self.end_name,"se")]:
            c.create_oval(x-9,y-9,x+9,y+9,fill=col,outline="#F1F6FF",width=2)
            c.create_text(x+13,y-10 if anchor=="nw" else y+12,text=label[:27],fill="#F1F6FF",
                          font=("Segoe UI",9,"bold"),anchor="nw" if anchor=="nw" else "se")
        c.create_text(12,h-10,text="Illustrative local road artwork · not geographic/live map data",
                      fill="#93A8C3",font=("Segoe UI",8),anchor="sw")

class PlanRoutePage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent"); self.app=app; self.results=[]
        ctk.CTkLabel(self,text="Plan Your Route",font=("Segoe UI",24,"bold"),text_color="#F1F6FF").pack(anchor="w",pady=(0,4))
        ctk.CTkLabel(self,text="Compare options on a local offline map. All figures are demonstration estimates.",text_color="#93A8C3").pack(anchor="w",pady=(0,14))
        body=ctk.CTkFrame(self,fg_color="transparent"); body.pack(fill="both",expand=True)
        form=ctk.CTkFrame(body,fg_color="#11161C",corner_radius=14,border_width=1,border_color="#2A313A",width=260)
        form.pack(side="left",fill="y",padx=(0,12)); form.pack_propagate(False)
        names=app.store.place_names()
        self.start=LocationSelector(form,"FROM",names); self.start.pack(fill="x",padx=13,pady=(15,10))
        self.end=LocationSelector(form,"TO",names); self.end.pack(fill="x",padx=13,pady=10)
        ctk.CTkLabel(form,text="TRAVEL MODE",text_color="#93A8C3",font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(9,5))
        self.mode=ctk.StringVar(value=app.store.preferences.get("travel_mode","Bike"))
        ctk.CTkSegmentedButton(form,values=["Bike","Car","Bus","Walk"],variable=self.mode,selected_color="#FFD22F").pack(fill="x",padx=13)
        ctk.CTkLabel(form,text="ROUTE PRIORITY",text_color="#93A8C3",font=("Segoe UI",10,"bold")).pack(anchor="w",padx=13,pady=(15,5))
        self.priority=ctk.StringVar(value=app.store.preferences.get("priority","Fastest"))
        ctk.CTkSegmentedButton(form,values=["Fastest","Shortest","Lowest Cost"],variable=self.priority,selected_color="#FFD22F").pack(fill="x",padx=13)
        ctk.CTkButton(form,text="→  Find Routes",height=39,command=self.calculate).pack(fill="x",padx=13,pady=17)
        self.status=ctk.CTkLabel(form,text="Offline mode · no API key required",text_color="#718BAA",wraplength=220,justify="left")
        self.status.pack(anchor="w",padx=13,pady=(0,12))
        right=ctk.CTkFrame(body,fg_color="transparent"); right.pack(side="left",fill="both",expand=True)
        self.map=OfflineRouteMap(right); self.map.pack(fill="x")
        ctk.CTkLabel(right,text="Route Options",font=("Segoe UI",18,"bold"),text_color="#F1F6FF").pack(anchor="w",pady=(13,7))
        self.results_frame=ctk.CTkFrame(right,fg_color="transparent"); self.results_frame.pack(fill="both",expand=True)
        self.calculate()
    def calculate(self):
        try:
            self.results=self.app.router.compare(self.start.get(),self.end.get(),self.mode.get())
            for w in self.results_frame.winfo_children(): w.destroy()
            if not self.results:
                self.status.configure(text="No connected route found. Choose different locations.")
                self.map.set_route(self.start.get(),self.end.get()); return
            priority={"Fastest":"time","Shortest":"distance","Lowest Cost":"cost"}[self.priority.get()]
            chosen=min(self.results,key=lambda r:r[priority])
            self.map.set_route(self.start.get(),self.end.get(),chosen.get("path"))
            for item in self.results:
                card=RouteCard(self.results_frame,item["title"],item["distance"],item["minutes"],item["cost"],
                    recommended=item is chosen,on_select=lambda r=item:self.app.open_route(r,self.start.get(),self.end.get(),self.mode.get()))
                card.pack(fill="x",pady=4)
            self.status.configure(text=f"{len(self.results)} options calculated locally.\nNo live traffic or external map service.")
        except Exception as exc:
            self.app.notify("Route calculation failed",str(exc))
