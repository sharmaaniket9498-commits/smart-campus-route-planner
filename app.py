import json, math, uuid, os
import customtkinter as ctk
from tkinter import messagebox
from components.sidebar import Sidebar
from pages.home import HomePage
from pages.plan_route import PlanRoutePage
from pages.route_details import RouteDetailsPage
from pages.saved_places import SavedPlacesPage
from pages.about import AboutPage
from pages.graph_explorer import GraphExplorerPage
from algorithms.dijkstra import dijkstra
from algorithms.bfs import bfs
from algorithms.floyd_warshall import floyd_warshall

APP_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_FILE=os.path.join(APP_DIR,"campus_data.json")
DEFAULT_DATA={"saved_places":[],"preferences":{"travel_mode":"Bike","priority":"Fastest","show_estimates":True}}

class DataStore:
    def __init__(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(DEFAULT_DATA,f,indent=2)
        try:
            with open(DATA_FILE,encoding="utf-8") as f: self.data=json.load(f)
        except (OSError,json.JSONDecodeError):
            self.data=DEFAULT_DATA.copy(); self.save()
        self.data.setdefault("saved_places",[]); self.data.setdefault("preferences",{})
        for k,v in DEFAULT_DATA["preferences"].items(): self.data["preferences"].setdefault(k,v)
    @property
    def places(self): return self.data["saved_places"]
    @property
    def preferences(self): return self.data["preferences"]
    def save(self):
        tmp=DATA_FILE+".tmp"
        with open(tmp,"w",encoding="utf-8") as f: json.dump(self.data,f,indent=2,ensure_ascii=False)
        os.replace(tmp,DATA_FILE)
    def place_names(self): return [p["name"] for p in self.places]
    def add_place(self,name,category,area):
        self.places.append({"id":uuid.uuid4().hex[:10],"name":name,"category":category,"area":area,"lat":None,"lon":None}); self.save()
    def update_place(self,pid,name,category,area):
        for p in self.places:
            if p["id"]==pid: p.update(name=name,category=category,area=area); break
        self.save()
    def delete_place(self,pid): self.data["saved_places"]=[p for p in self.places if p["id"]!=pid]; self.save()

class Router:
    """A demonstration graph; values are illustrative, not live road data."""
    def __init__(self,store):
        self.store=store
        # Demonstration weights only; they are not verified road distances.
        self.base={
          "Chandigarh University":{"Landran":(8.0,16,18),"Kharar Bus Stand":(10.5,22,22),"North Country Mall":(7.0,14,16),"Mohali":(18.0,34,35)},
          "Landran":{"Chandigarh University":(8.0,16,18),"Mohali":(10.0,20,22),"ISB Mohali":(7.0,14,16),"Kharar Bus Stand":(11.0,23,24)},
          "Kharar Bus Stand":{"Chandigarh University":(10.5,22,22),"Landran":(11.0,23,24),"North Country Mall":(5.5,12,12),"Home (Kharar)":(4.0,9,9)},
          "North Country Mall":{"Chandigarh University":(7.0,14,16),"Kharar Bus Stand":(5.5,12,12),"Home (Kharar)":(8.0,16,18),"Mohali":(14.0,27,30)},
          "Home (Kharar)":{"Kharar Bus Stand":(4.0,9,9),"North Country Mall":(8.0,16,18),"Chandigarh":(12.8,24,34),"Mohali":(8.7,18,24),"PGI Chandigarh":(16.1,30,42)},
          "Mohali":{"Chandigarh University":(18.0,34,35),"Landran":(10.0,20,22),"Home (Kharar)":(8.7,18,24),"Chandigarh":(6.9,14,20),"PGI Chandigarh":(10.4,22,30),"Shaheed Bhagat Singh Airport":(9.0,18,24),"ISB Mohali":(6.0,12,14)},
          "ISB Mohali":{"Landran":(7.0,14,16),"Mohali":(6.0,12,14),"Shaheed Bhagat Singh Airport":(12.0,22,28)},
          "Shaheed Bhagat Singh Airport":{"Mohali":(9.0,18,24),"ISB Mohali":(12.0,22,28),"Chandigarh":(18.0,32,48)},
          "Chandigarh":{"Home (Kharar)":(12.8,24,34),"Mohali":(6.9,14,20),"PGI Chandigarh":(5.1,12,18),"Sector 22 Market":(2.2,7,10),"Elante Mall":(7.5,16,22),"Sukhna Lake":(8.0,18,0),"Shaheed Bhagat Singh Airport":(18.0,32,48)},
          "PGI Chandigarh":{"Home (Kharar)":(16.1,30,42),"Chandigarh":(5.1,12,18),"Mohali":(10.4,22,30),"Sector 22 Market":(4.4,11,16),"Sukhna Lake":(6.0,14,0)},
          "Sector 22 Market":{"Chandigarh":(2.2,7,10),"PGI Chandigarh":(4.4,11,16),"Elante Mall":(6.5,14,20)},
          "Elante Mall":{"Chandigarh":(7.5,16,22),"Sector 22 Market":(6.5,14,20),"Sukhna Lake":(10.0,22,0)},
          "Sukhna Lake":{"Chandigarh":(8.0,18,0),"PGI Chandigarh":(6.0,14,0),"Elante Mall":(10.0,22,0)}
        }
    def graph(self,mode):
        factor={"Bike":1.0,"Car":0.82,"Bus":1.18,"Walk":2.8}.get(mode,1.0)
        graph={}
        for node,edges in self.base.items():
            graph[node]={}
            for other,(dist,mins,cost) in edges.items():
                graph[node][other]={"distance":dist,"time":max(1,mins*factor),"cost":cost*({"Bike":1,"Car":1.5,"Bus":0.55,"Walk":0}[mode])}
        # Custom locations connect to the nearest known sample node with clearly estimated weights.
        known=set(graph)
        for p in self.store.places:
            name=p["name"]
            if name not in graph:
                graph[name]={}
                if known:
                    nearest=min(known,key=lambda n: abs(len(n)-len(name))+sum(a!=b for a,b in zip(n.lower(),name.lower()))*.2)
                    graph[name][nearest]={"distance":5.0,"time":12*factor,"cost":8.0}
                    graph[nearest][name]={"distance":5.0,"time":12*factor,"cost":8.0}
        return graph
    def compare(self,start,end,mode):
        if start==end: raise ValueError("Choose two different locations.")
        g=self.graph(mode)
        if start not in g or end not in g: return []
        options=[]
        for key,title in [("time","Fastest Route"),("distance","Shortest Distance"),("cost","Lowest Cost")]:
            result=dijkstra(g,start,end,key)
            if result:
                path=result["path"]; distance=minutes=cost=0
                for a,b in zip(path,path[1:]):
                    e=g[a][b]; distance+=e["distance"]; minutes+=e["time"]; cost+=e["cost"]
                options.append({"title":title,"path":path,"distance":distance,"minutes":int(round(minutes)),"cost":cost})
        return options

class SmartCampusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark"); ctk.set_default_color_theme("blue")
        self.title("Smart Campus Route Planner"); self.geometry("1280x800"); self.minsize(980,650)
        self.configure(fg_color="#07090D")
        self.store=DataStore(); self.router=Router(self.store); self.pending_location=None; self.pending_route=None
        self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(0,weight=1)
        self.sidebar=Sidebar(self,self.show_page,"Home"); self.sidebar.grid(row=0,column=0,sticky="ns")
        self.main=ctk.CTkFrame(self,fg_color="#07090D",corner_radius=0); self.main.grid(row=0,column=1,sticky="nsew",padx=18,pady=14)
        self.main.grid_rowconfigure(1,weight=1); self.main.grid_columnconfigure(0,weight=1)
        top=ctk.CTkFrame(self.main,fg_color="transparent"); top.grid(row=0,column=0,sticky="ew",pady=(0,14))
        ctk.CTkLabel(top,text="Smart Campus  /  Route Planner",text_color="#718BAA",font=("Segoe UI",11)).pack(side="left")
        ctk.CTkLabel(top,text=f'◉  {self.store.preferences.get("profile_name","Campus User")}',text_color="#B5C9E2",font=("Segoe UI",11,"bold")).pack(side="right")
        self.stage=ctk.CTkFrame(self.main,fg_color="transparent"); self.stage.grid(row=1,column=0,sticky="nsew")
        self.pages={}
        for name,cls in [("Home",HomePage),("Plan Route",PlanRoutePage),("Route Details",RouteDetailsPage),
                         ("Saved Places",SavedPlacesPage),("Graph Explorer",GraphExplorerPage),("About",AboutPage)]:
            self.pages[name]=cls(self.stage,self)
        self.show_page("Home")
    def show_page(self,name):
        if name not in self.pages: return
        for p in self.pages.values(): p.pack_forget()
        self.pages[name].pack(fill="both",expand=True)
        self.sidebar.set_active(name if name!="Route Details" else "Plan Route")
        if name=="Graph Explorer": self.pages[name].refresh_graph()
        if name=="Saved Places": self.pages[name].refresh()
        if name=="Plan Route":
            page=self.pages[name]
            page.start.set_values(self.store.place_names()); page.end.set_values(self.store.place_names())
            if self.pending_location:
                which,loc=self.pending_location; (page.start if which=="from" else page.end).variable.set(loc); self.pending_location=None
            if self.pending_route:
                h=self.pending_route
                if h["start"] in self.store.place_names(): page.start.variable.set(h["start"])
                if h["end"] in self.store.place_names(): page.end.variable.set(h["end"])
                page.mode.set(h["mode"]); self.pending_route=None
    def open_route(self,route,start,end,mode):
        self.pages["Route Details"].load(route,start,end,mode); self.show_page("Route Details")
    def refresh_shared(self):
        if "Plan Route" in self.pages:
            p=self.pages["Plan Route"]; p.start.set_values(self.store.place_names()); p.end.set_values(self.store.place_names())
    def notify(self,title,message): messagebox.showinfo(title,message,parent=self)
if __name__=="__main__":
    try: SmartCampusApp().mainloop()
    except Exception as exc:
        try: messagebox.showerror("Smart Campus Route Planner",f"Application could not start:\n{exc}")
        except Exception: print(f"Application could not start: {exc}")
