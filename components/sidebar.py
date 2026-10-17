import customtkinter as ctk

NAV = [("⌂","Home"),("↗","Plan Route"),("◎","Graph Explorer"),("▤","Saved Places"),("ⓘ","About")]

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate, active="Home"):
        super().__init__(master, width=190, corner_radius=0, fg_color="#090D12")
        self.pack_propagate(False)
        brand = ctk.CTkFrame(self, fg_color="transparent"); brand.pack(fill="x", padx=16, pady=(20, 24))
        ctk.CTkLabel(brand, text="◆", text_color="#FFD22F", font=("Segoe UI", 27, "bold")).pack(side="left")
        ctk.CTkLabel(brand, text="Smart Campus\nRoute Planner", justify="left",
                     font=("Segoe UI", 13, "bold"), text_color="#F1F6FF").pack(side="left", padx=8)
        self.buttons = {}
        for icon, name in NAV:
            btn = ctk.CTkButton(self, text=f"{icon}   {name}", anchor="w", height=38, corner_radius=8,
                fg_color="#FFD22F" if name == active else "transparent",
                hover_color="#272D34", text_color="#F1F6FF", font=("Segoe UI Symbol", 12),
                command=lambda n=name: navigate(n))
            btn.pack(fill="x", padx=10, pady=3); self.buttons[name] = btn
        ctk.CTkLabel(self, text="SMART ROUTES\nBETTER JOURNEYS", text_color="#6E8BAE",
                     font=("Segoe UI", 10, "bold"), justify="left").pack(side="bottom", anchor="w", padx=20, pady=20)
    def set_active(self, active):
        for name, btn in self.buttons.items():
            btn.configure(fg_color="#FFD22F" if name == active else "transparent")
