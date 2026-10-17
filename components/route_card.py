import customtkinter as ctk

class RouteCard(ctk.CTkFrame):
    def __init__(self, master, title, distance, duration, cost, recommended=False, on_select=None, accent="#FFD22F"):
        super().__init__(master, fg_color="#11161C", corner_radius=14, border_width=1, border_color="#2A313A")
        top = ctk.CTkFrame(self, fg_color="transparent"); top.pack(fill="x", padx=14, pady=(12, 5))
        ctk.CTkLabel(top, text=title, font=("Segoe UI", 14, "bold"), text_color="#F1F6FF").pack(side="left")
        if recommended:
            ctk.CTkLabel(top, text="RECOMMENDED", fg_color="#087F68", text_color="#E6FFF8",
                         corner_radius=6, font=("Segoe UI", 9, "bold"), padx=7, pady=4).pack(side="right")
        ctk.CTkLabel(self, text=f"◉  {distance:.1f} km     ◷  {duration} min     ₹ {cost:.0f}",
                     text_color="#B7C9DF", font=("Segoe UI", 11)).pack(anchor="w", padx=14, pady=(4, 12))
        ctk.CTkButton(self, text="View Details", height=32, corner_radius=8, fg_color=accent,
                      hover_color="#0861D8", command=on_select).pack(fill="x", padx=12, pady=(0, 12))
