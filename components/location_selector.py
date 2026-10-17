import customtkinter as ctk

class LocationSelector(ctk.CTkFrame):
    def __init__(self, master, label, values, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(self, text=label, text_color="#93A8C3", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        self.variable = ctk.StringVar(value=values[0] if values else "")
        self.menu = ctk.CTkOptionMenu(self, variable=self.variable, values=values or ["No locations"], height=38,
                                      fg_color="#252B32", button_color="#FFD22F", button_hover_color="#FFD22F",
                                      dropdown_fg_color="#11161C", text_color="#F1F6FF", font=("Segoe UI", 12))
        self.menu.pack(fill="x")
    def get(self): return self.variable.get()
    def set_values(self, values):
        self.menu.configure(values=values or ["No locations"])
        if self.variable.get() not in values and values: self.variable.set(values[0])
