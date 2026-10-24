import customtkinter as ctk

BG = "#07090D"
CARD = "#11161C"
GOLD = "#FFD22F"
TEXT = "#F1F6FF"
MUTED = "#B5C9E2"
BORDER = "#2A313A"


class TheoryPage(ctk.CTkFrame):
    """Concise project theory and algorithm reference."""
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text="Theory & Algorithms", font=("Segoe UI", 26, "bold"),
                     text_color=TEXT).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(self, text="A quick reference for the algorithms used in this project.",
                     font=("Segoe UI", 12), text_color=MUTED).pack(anchor="w", pady=(0, 14))

        body = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        body.pack(fill="both", expand=True)
        sections = [
            ("Weighted Graph",
             "The campus network is represented as a graph. Each location is a node and each connection is an edge. "
             "Edges store sample distance, time and cost values, which can be used as route weights."),
            ("Dijkstra's Algorithm",
             "Dijkstra finds a minimum-weight path from a start node to a destination when edge weights are non-negative. "
             "In this project, the selected weight can represent distance, travel time or estimated cost."),
            ("Breadth-First Search (BFS)",
             "BFS explores the graph level by level. It finds a path with the fewest edges (hops) in an unweighted graph. "
             "That path is not necessarily the shortest by distance or time."),
            ("A* Search",
             "A* combines the cost already travelled with a heuristic estimate of the remaining cost. "
             "It can guide the search toward the destination. The result depends on the graph weights and heuristic."),
            ("Floyd–Warshall Algorithm",
             "Floyd–Warshall computes shortest-path distances between every pair of nodes. It is useful when many "
             "start/destination combinations need to be queried, though it uses more time and memory than a single-source search."),
            ("Project Data",
             "Distances, times and prices in this demonstration are sample estimates, not live road or traffic data. "
             "The application does not use live GPS or Google Maps. User-added places are stored locally.")
        ]
        for title, description in sections:
            card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=13,
                                border_width=1, border_color=BORDER)
            card.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(card, text=title, text_color=GOLD,
                         font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=18, pady=(14, 5))
            ctk.CTkLabel(card, text=description, text_color=MUTED,
                         font=("Segoe UI", 12), justify="left", anchor="w",
                         wraplength=900).pack(fill="x", anchor="w", padx=18, pady=(0, 15))
