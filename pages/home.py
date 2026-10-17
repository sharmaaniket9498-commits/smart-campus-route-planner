import customtkinter as ctk
import tkinter as tk

class CampusIllustration(ctk.CTkFrame):
    """Locally drawn vector campus scene. No photo, AI image, backend or network access."""
    def __init__(self, master):
        super().__init__(master, fg_color="#141A20", corner_radius=14)
        self.canvas = tk.Canvas(self, height=260, bg="#141A20", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=4, pady=4)
        self.canvas.bind("<Configure>", self.draw)
        self.draw()
    def draw(self, event=None):
        c=self.canvas; c.delete("all")
        w=max(c.winfo_width(),380); h=max(c.winfo_height(),240)
        # evening sky and distant hills
        c.create_rectangle(0,0,w,h,fill="#141A20",outline="")
        c.create_oval(w*.73,-h*.18,w*.91,h*.24,fill="#174A78",outline="")
        c.create_polygon(0,h*.62,w*.13,h*.25,w*.23,h*.48,w*.34,h*.18,w*.47,h*.52,w*.61,h*.28,w*.77,h*.55,w*.91,h*.33,w,h*.55,w,h*.82,0,h*.82,fill="#1C5276",outline="")
        c.create_polygon(0,h*.70,w*.18,h*.46,w*.28,h*.65,w*.44,h*.40,w*.61,h*.67,w*.80,h*.44,w,h*.67,w,h,0,h,fill="#174A56",outline="")
        # campus lawn
        c.create_rectangle(0,h*.75,w,h,fill="#123E4A",outline="")
        # campus building facade
        bx1,by1,bx2,by2=w*.22,h*.40,w*.78,h*.83
        c.create_rectangle(bx1,by1,bx2,by2,fill="#B66F4B",outline="#E6B28C",width=2)
        c.create_polygon(bx1-w*.025,by1,bx2+w*.025,by1,bx2-w*.02,by1-h*.09,bx1+w*.02,by1-h*.09,fill="#263E59",outline="#E6B28C",width=2)
        c.create_rectangle(w*.45,h*.29,w*.55,h*.40,fill="#DDA27B",outline="#F1C5A2",width=2)
        # columns and windows
        for i in range(7):
            x=bx1+w*.045+i*w*.075
            c.create_rectangle(x,h*.47,x+w*.032,h*.80,fill="#E9C19A",outline="#8A523F")
            for yy in (h*.49,h*.59,h*.69):
                c.create_rectangle(x+w*.005,yy,x+w*.027,yy+h*.035,fill="#2A313A",outline="#F4C99F")
        c.create_rectangle(w*.45,h*.70,w*.55,h*.83,fill="#163451",outline="#E9C19A",width=2)
        # foreground path and campus lights
        c.create_polygon(w*.43,h,w*.57,h,w*.53,h*.82,w*.47,h*.82,fill="#C9B99B",outline="")
        for x in (w*.12,w*.87):
            c.create_line(x,h*.60,x,h*.82,fill="#B5C9E2",width=2)
            c.create_oval(x-4,h*.57,x+4,h*.61,fill="#F8D477",outline="")
        c.create_text(w*.5,h*.93,text="CAMPUS ROUTE NETWORK  •  LOCAL VECTOR ART",fill="#C4D8E9",font=("Segoe UI",9,"bold"))

class HomePage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        hero = ctk.CTkFrame(self, fg_color="#141A20", corner_radius=18,
                            border_width=1, border_color="#3B3420")
        hero.pack(fill="x", pady=(0, 16))
        hero.grid_columnconfigure(0, weight=5); hero.grid_columnconfigure(1, weight=4)
        left = ctk.CTkFrame(hero, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(26, 12), pady=24)
        ctk.CTkLabel(left, text="SMART CAMPUS ROUTE PLANNER", text_color="#FFD22F",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ctk.CTkLabel(left, text="Find the Best Route\nAcross Chandigarh & Mohali", justify="left",
                     font=("Segoe UI", 27, "bold"), text_color="#F1F6FF").pack(anchor="w", pady=(12, 7))
        ctk.CTkLabel(left, text="Smart. Fast. Reliable.", font=("Segoe UI", 17, "bold"),
                     text_color="#FFD22F").pack(anchor="w")
        ctk.CTkLabel(left, text="Explore nearby locations and watch Dijkstra's algorithm find a lowest-weight path across the sample road network.",
                     justify="left", text_color="#B5C9E2", font=("Segoe UI", 12),
                     wraplength=450).pack(anchor="w", pady=(8, 16))
        buttons=ctk.CTkFrame(left,fg_color="transparent"); buttons.pack(anchor="w")
        ctk.CTkButton(buttons, text="↗  Plan Your Route", width=165, height=39,
                      command=lambda: app.show_page("Plan Route")).pack(side="left",padx=(0,8))
        ctk.CTkButton(buttons, text="⌘  Explore Graph", width=155, height=39, fg_color="#272D34",
                      command=lambda: app.show_page("Graph Explorer")).pack(side="left")
        right = CampusIllustration(hero)
        right.grid(row=0, column=1, sticky="nsew", padx=(4, 18), pady=18)
        cards = ctk.CTkFrame(self, fg_color="transparent"); cards.pack(fill="x")
        # Feature icons are drawn with Canvas primitives instead of font glyphs,
        # so they render consistently on Windows even when symbol fonts are missing.
        features = [("routes","Multiple Routes","Compare distance, time and cost","#39D98A"),
                    ("graph","Offline Road Graph","Visualize connected places","#FFD22F"),
                    ("algorithm","Dijkstra Explorer","Highlight shortest weighted path","#A78BFA"),
                    ("privacy","Local & Private","No API, backend or AI photos","#FB7185")]
        for icon, title, desc, color in features:
            card=ctk.CTkFrame(cards, fg_color="#11161C", corner_radius=13, border_width=1, border_color="#2A313A")
            card.pack(side="left", expand=True, fill="both", padx=(0,9), pady=4)
            icon_canvas = tk.Canvas(card, width=34, height=34, bg="#11161C", highlightthickness=0, bd=0)
            icon_canvas.pack(anchor="w", padx=14, pady=(10,4))
            self._draw_feature_icon(icon_canvas, icon, color)
            ctk.CTkLabel(card,text=title,text_color="#F1F6FF",font=("Segoe UI",13,"bold")).pack(anchor="w",padx=14)
            ctk.CTkLabel(card,text=desc,text_color="#93A8C3",font=("Segoe UI",10),wraplength=150,justify="left").pack(anchor="w",padx=14,pady=(5,13))
        ctk.CTkLabel(self, text=f"WORKSPACE  ·  {len(app.store.places)} saved places  ·  Sample graph data",
                     text_color="#718BAA", font=("Segoe UI", 11)).pack(anchor="w", pady=(14,0))

    @staticmethod
    def _draw_feature_icon(canvas, kind, color):
        """Draw compact, crisp vector icons with native Canvas primitives."""
        c = canvas
        c.delete("all")
        common = {"fill": color, "width": 2, "capstyle": tk.ROUND, "joinstyle": tk.ROUND}
        if kind == "routes":
            c.create_oval(3, 13, 10, 20, outline=color, width=2)
            c.create_oval(24, 4, 31, 11, outline=color, width=2)
            c.create_oval(24, 23, 31, 30, outline=color, width=2)
            c.create_line(10, 15, 17, 10, 24, 7, **common)
            c.create_line(10, 18, 17, 24, 24, 26, **common)
        elif kind == "graph":
            pts = [(5, 6), (27, 7), (16, 17), (6, 28), (28, 27)]
            for a, b in [(0,2),(1,2),(2,3),(2,4),(3,4)]:
                c.create_line(*pts[a], *pts[b], **common)
            for x, y in pts:
                c.create_oval(x-3, y-3, x+3, y+3, fill="#11161C", outline=color, width=2)
        elif kind == "algorithm":
            # Three ordered nodes with a highlighted shortest-path line.
            c.create_line(5, 25, 16, 15, 28, 6, fill=color, width=3, capstyle=tk.ROUND, joinstyle=tk.ROUND)
            for x, y in [(5,25),(16,15),(28,6)]:
                c.create_oval(x-3, y-3, x+3, y+3, fill="#11161C", outline=color, width=2)
            c.create_line(5, 6, 10, 6, fill=color, width=2)
            c.create_line(5, 6, 5, 11, fill=color, width=2)
        elif kind == "privacy":
            c.create_polygon(17, 3, 28, 7, 27, 18, 17, 29, 7, 18, 6, 7, fill="", outline=color, width=2)
            c.create_line(11, 16, 15, 20, 23, 11, fill=color, width=2, capstyle=tk.ROUND, joinstyle=tk.ROUND)
