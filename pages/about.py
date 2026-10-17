import customtkinter as ctk

class AboutPage(ctk.CTkFrame):
    def __init__(self,master,app):
        super().__init__(master,fg_color="transparent")
        ctk.CTkLabel(self,text="About Smart Campus Route Planner",font=("Segoe UI",24,"bold"),text_color="#F1F6FF").pack(anchor="w",pady=(0,14))
        card=ctk.CTkFrame(self,fg_color="#11161C",corner_radius=14,border_width=1,border_color="#2A313A")
        card.pack(fill="both",expand=True)
        sections=[
          ("Project Overview","A desktop route-planning demonstration for comparing paths between campus, home and nearby destinations."),
          ("Key Features","Multiple route priorities • Dijkstra Graph Explorer • Chandigarh University and nearby nodes • Saved places"),
          ("Graph Algorithms","Dijkstra: weighted shortest paths. Breadth-First Search: graph traversal and minimum-hop path. Floyd-Warshall: all-pairs shortest distances."),
          ("Technologies","Python 3 • CustomTkinter • JSON local storage • Custom graph algorithms • Tkinter Canvas vector illustrations • JSON local storage"),
          ("Data Limitations","Distances, times and costs are illustrative sample graph weights for Chandigarh University, Landran, Kharar, Mohali and Chandigarh-area destinations. The application does not fetch Google Maps, live road closures, GPS position or real-time traffic. Custom locations are stored locally.")
        ]
        for title,body in sections:
            ctk.CTkLabel(card,text=title,font=("Segoe UI",16,"bold"),text_color="#FFD22F").pack(anchor="w",padx=22,pady=(18,4))
            ctk.CTkLabel(card,text=body,font=("Segoe UI",12),text_color="#B5C9E2",wraplength=760,justify="left").pack(anchor="w",padx=22)
