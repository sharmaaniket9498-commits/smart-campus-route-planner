import customtkinter as ctk
import tkinter as tk
import math

class RouteDetailsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master,fg_color="transparent"); self.app=app; self.route=None
        head=ctk.CTkFrame(self,fg_color="transparent"); head.pack(fill="x")
        ctk.CTkButton(head,text="← Back",width=90,fg_color="#252B32",command=lambda:app.show_page("Plan Route")).pack(side="left")
        ctk.CTkLabel(head,text="Route Details",font=("Segoe UI",24,"bold"),text_color="#F1F6FF").pack(side="left",padx=16)
        self.content=ctk.CTkFrame(self,fg_color="#11161C",corner_radius=14,border_width=1,border_color="#2A313A")
        self.content.pack(fill="both",expand=True,pady=14)
    def load(self, route, start, end, mode):
        self.route=route; self.start=start; self.end=end; self.mode=mode
        for w in self.content.winfo_children(): w.destroy()
        ctk.CTkLabel(self.content,text=f"{start}   →   {end}",font=("Segoe UI",20,"bold"),text_color="#F1F6FF").pack(anchor="w",padx=20,pady=(18,4))
        ctk.CTkLabel(self.content,text=f"{route['distance']:.1f} km     ·     {route['minutes']} min     ·     ₹ {route['cost']:.0f}     ·     {mode}",
                     font=("Segoe UI",14),text_color="#FFD22F").pack(anchor="w",padx=20,pady=5)
        mapbox=ctk.CTkFrame(self.content,fg_color="#102F4A",corner_radius=12,height=245)
        mapbox.pack(fill="x",padx=18,pady=12); mapbox.pack_propagate(False)
        canvas=tk.Canvas(mapbox,bg="#102F4A",highlightthickness=0,height=245); canvas.pack(fill="both",expand=True)
        def draw(event=None):
            canvas.delete("all"); w=max(canvas.winfo_width(),450); h=max(canvas.winfo_height(),200)
            for x in range(0,w,45): canvas.create_line(x,0,x,h,fill="#28506A",width=1)
            for y in range(0,h,38): canvas.create_line(0,y,w,y,fill="#28506A",width=1)
            pts=[(w*.12,h*.2),(w*.27,h*.35),(w*.4,h*.29),(w*.52,h*.58),(w*.69,h*.48),(w*.84,h*.78)]
            flat=[v for p in pts for v in p]
            canvas.create_line(*flat,fill="#06182A",width=10,smooth=True)
            canvas.create_line(*flat,fill="#FFD22F",width=5,smooth=True)
            for (x,y),col,label in [(pts[0],"#39D98A",start),(pts[-1],"#FB7185",end)]:
                canvas.create_oval(x-8,y-8,x+8,y+8,fill=col,outline="#F1F6FF",width=2)
                canvas.create_text(x+12,y-8,text=label,fill="#F1F6FF",anchor="nw",font=("Segoe UI",10,"bold"))
            canvas.create_text(12,h-10,text="Offline schematic map · route is illustrative",fill="#93A8C3",anchor="sw",font=("Segoe UI",9))
        canvas.bind("<Configure>",draw); draw()
        ctk.CTkLabel(self.content,text="Route Summary & Directions",font=("Segoe UI",16,"bold"),text_color="#F1F6FF").pack(anchor="w",padx=20,pady=(3,4))
        path=route.get("path",[start,end])
        direction_text="   →   ".join(path)
        ctk.CTkLabel(self.content,text=direction_text,wraplength=850,justify="left",text_color="#B5C9E2").pack(anchor="w",padx=20,pady=4)
        ctk.CTkLabel(self.content,text="Estimated values are based on sample graph data. Live traffic and GPS are not connected.",
                     text_color="#93A8C3",wraplength=800).pack(anchor="w",padx=20,pady=5)
        row=ctk.CTkFrame(self.content,fg_color="transparent"); row.pack(anchor="w",padx=20,pady=12)
        ctk.CTkButton(row,text="↗  Share Summary",fg_color="#252B32",command=self.share).pack(side="left")
    def share(self):
        text=f"{self.start} → {self.end}\n{self.route['distance']:.1f} km | {self.route['minutes']} min | ₹{self.route['cost']:.0f} estimated"
        self.clipboard_clear(); self.clipboard_append(text); self.app.notify("Copied","Route summary copied to clipboard.")
