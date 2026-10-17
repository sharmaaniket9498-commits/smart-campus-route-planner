import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox

class SavedPlacesPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master,fg_color="transparent"); self.app=app
        top=ctk.CTkFrame(self,fg_color="transparent"); top.pack(fill="x",pady=(0,14))
        ctk.CTkLabel(top,text="Saved Places",font=("Segoe UI",24,"bold"),text_color="#F1F6FF").pack(side="left")
        ctk.CTkButton(top,text="+ Add New Place",command=self.add).pack(side="right")
        self.grid=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.grid.pack(fill="both",expand=True)
        self.refresh()
    def refresh(self):
        for w in self.grid.winfo_children(): w.destroy()
        for i,p in enumerate(self.app.store.places):
            card=ctk.CTkFrame(self.grid,fg_color="#11161C",corner_radius=13,border_width=1,border_color="#2A313A")
            card.grid(row=i//3,column=i%3,sticky="nsew",padx=5,pady=5)
            category=p.get("category","Place")
            # Draw icons with Canvas primitives rather than Unicode glyphs, which can
            # render as question marks on Windows systems with missing symbol fonts.
            icon_canvas = tk.Canvas(card, width=34, height=34, bg="#11161C", highlightthickness=0, bd=0)
            icon_canvas.pack(anchor="w", padx=13, pady=(12,3))
            self._draw_place_icon(icon_canvas, category)
            ctk.CTkLabel(card,text=p["name"],font=("Segoe UI",13,"bold"),text_color="#F1F6FF",wraplength=180).pack(anchor="w",padx=13)
            ctk.CTkLabel(card,text=f'{p.get("category","Place")}  ·  {p.get("area","Custom location")}',font=("Segoe UI",10),text_color="#93A8C3",wraplength=180).pack(anchor="w",padx=13,pady=(4,12))
            row=ctk.CTkFrame(card,fg_color="transparent"); row.pack(fill="x",padx=10,pady=(0,8))
            ctk.CTkButton(row,text="From",width=58,height=28,command=lambda n=p["name"]:self.use(n,"from")).pack(side="left",padx=2)
            ctk.CTkButton(row,text="To",width=45,height=28,fg_color="#252B32",command=lambda n=p["name"]:self.use(n,"to")).pack(side="left",padx=2)
            ctk.CTkButton(row,text="Edit",width=45,height=28,fg_color="#252B32",command=lambda x=p:self.edit(x)).pack(side="left",padx=2)
            ctk.CTkButton(row,text="×",width=28,height=28,fg_color="#7F1D35",hover_color="#B42343",command=lambda x=p:self.delete(x)).pack(side="right",padx=2)
        for c in range(3): self.grid.grid_columnconfigure(c,weight=1)
    @staticmethod
    def _draw_place_icon(canvas, category):
        c = canvas
        c.delete("all")
        yellow = "#FFD22F"
        cat = (category or "").lower()
        if "home" in cat:
            c.create_polygon(4,16,17,5,30,16,fill="",outline=yellow,width=2)
            c.create_rectangle(8,16,26,30,outline=yellow,width=2)
            c.create_rectangle(14,21,20,30,outline=yellow,width=2)
        elif "college" in cat or "university" in cat:
            c.create_polygon(3,11,17,4,31,11,fill="",outline=yellow,width=2)
            c.create_line(6,13,28,13,fill=yellow,width=2)
            for x in (8,14,20,26): c.create_line(x,14,x,27,fill=yellow,width=2)
            c.create_line(4,29,30,29,fill=yellow,width=2)
        elif "hospital" in cat:
            c.create_rectangle(6,5,28,30,outline=yellow,width=2)
            c.create_rectangle(14,9,20,23,fill=yellow,outline=yellow)
            c.create_rectangle(10,13,24,19,fill=yellow,outline=yellow)
        elif "airport" in cat or "transit" in cat:
            c.create_line(17,4,17,30,fill=yellow,width=2)
            c.create_line(5,13,29,20,fill=yellow,width=2)
            c.create_line(17,15,7,25,fill=yellow,width=2)
            c.create_line(17,15,27,25,fill=yellow,width=2)
        elif "lake" in cat:
            for y in (10,17,24): c.create_line(4,y,10,y-3,17,y,24,y-3,30,y,fill=yellow,width=2,smooth=True)
        elif "shopping" in cat or "market" in cat:
            c.create_rectangle(7,13,27,29,outline=yellow,width=2)
            c.create_line(5,13,29,13,fill=yellow,width=2)
            c.create_arc(9,4,25,19,start=180,extent=180,style="arc",outline=yellow,width=2)
        elif "city" in cat or "town" in cat:
            c.create_rectangle(5,13,14,30,outline=yellow,width=2)
            c.create_rectangle(18,6,29,30,outline=yellow,width=2)
            for x,y in ((8,17),(11,17),(8,22),(21,11),(25,11),(21,17),(25,17),(21,23),(25,23)):
                c.create_rectangle(x,y,x+2,y+2,fill=yellow,outline=yellow)
        else:
            c.create_oval(6,5,28,27,outline=yellow,width=2)
            c.create_oval(13,12,21,20,fill=yellow,outline=yellow)
            c.create_line(17,26,17,32,fill=yellow,width=2)

    def add(self):
        name=simpledialog.askstring("Add place","Location name:",parent=self)
        if not name or not name.strip(): return
        area=simpledialog.askstring("Add place","City or area:",parent=self) or "Custom location"
        category=simpledialog.askstring("Add place","Category (e.g. Home, College):",parent=self) or "Place"
        self.app.store.add_place(name.strip(),category,area.strip()); self.refresh(); self.app.refresh_shared()
    def edit(self,p):
        name=simpledialog.askstring("Edit place","Location name:",initialvalue=p["name"],parent=self)
        if not name or not name.strip(): return
        area=simpledialog.askstring("Edit place","City or area:",initialvalue=p.get("area",""),parent=self) or p.get("area","")
        category=simpledialog.askstring("Edit place","Category:",initialvalue=p.get("category","Place"),parent=self) or p.get("category","Place")
        self.app.store.update_place(p["id"],name.strip(),category,area); self.refresh(); self.app.refresh_shared()
    def delete(self,p):
        if messagebox.askyesno("Delete place",f'Delete "{p["name"]}"?',parent=self):
            self.app.store.delete_place(p["id"]); self.refresh(); self.app.refresh_shared()
    def use(self,name,which):
        self.app.pending_location=(which,name); self.app.show_page("Plan Route")
