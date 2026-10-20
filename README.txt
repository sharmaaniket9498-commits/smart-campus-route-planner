## 🌐 Live Demo

**Live Website:** ## 🌐 Live Demo

[🚀 Open Smart Campus Route Planner](https://campus-route-planner-alpha.vercel.app/)

Try the deployed web version here: https://campus-route-planner-alpha.vercel.app/

> Note: The live website is the deployed web version. The Python CustomTkinter desktop application runs separately on Windows.




SMART CAMPUS ROUTE PLANNER — Python Desktop Application
========================================================

Features
--------
- Modern dark dashboard built with CustomTkinter.
- Home, Plan Route, Route Details, Saved Places, Graph Explorer and About screens. Settings has been removed.
- Route comparison by fastest, shortest distance and lowest estimated cost.
- Dijkstra, Breadth-First Search and Floyd-Warshall implementations.
- Local JSON persistence for saved places and preferences.
- Add, edit and delete custom places.
- Share route summary by copying it to the clipboard.

Requirements
------------
Windows 10/11 and Python 3.10+ recommended.

Quick start
-----------
1. Extract the ZIP to a writable folder.
2. Double-click RUN_APP.bat.
3. The launcher creates a virtual environment, installs dependencies, and starts the app.

Manual start
------------
python -m pip install -r requirements.txt
python app.py

Data and accuracy notes
-----------------------
All distances, times and prices are illustrative sample estimates. This project does not
connect to Google Maps, live traffic, GPS, or live road data. The map area is a schematic
route preview. Custom locations are connected to the sample graph with estimated links.

Project structure
-----------------
app.py                  Application shell, storage, and route service
components/             Sidebar, route cards, location selector
pages/                  Individual application screens
algorithms/             Dijkstra, BFS, Floyd-Warshall
campus_data.json        Persistent local sample data
requirements.txt        Python dependencies
RUN_APP.bat             Windows startup helper

LOCAL VISUAL ASSETS
-------------------
assets/images/campus_hero.png is bundled locally and used by the home screen.
The route map is drawn locally on a Canvas, with zoom controls and route markers.
No API key, backend, or network connection is required for map previews.

GRAPH EXPLORER UPDATE
---------------------
The Graph Explorer visualizes a schematic weighted graph and highlights Dijkstra's shortest path.
Included nodes: Chandigarh University, Landran, Kharar Bus Stand, North Country Mall, Home (Kharar),
Mohali, ISB Mohali, Shaheed Bhagat Singh Airport, Chandigarh, PGI Chandigarh, Sector 22 Market,
Elante Mall and Sukhna Lake. Weights are demonstration estimates, not verified road data.
No AI-generated college photos are included; the home hero is a locally drawn vector illustration.

ICON RENDERING NOTE
Feature-card and saved-place icons are drawn locally using Tkinter Canvas
shapes rather than Unicode symbol fonts, preventing missing-glyph question marks
on Windows. To ensure you run this version, close the app and extract this ZIP
into a new folder before launching RUN_APP.bat.

ICON FIX / FRESH INSTALL
This build uses Canvas-drawn vector shapes for the Home feature-card icons; it does not use question-mark or emoji glyphs for those icons.
For the updated UI, extract this ZIP into a NEW folder (do not merge into an old extracted folder), then run RUN_APP.bat from that new folder. Python cache folders are intentionally excluded from the ZIP.
Route History has been removed from this build. Route details can still be shared by copying the summary to the clipboard.

GRAPH EXPLORER — ENHANCED BUILD
-------------------------------
- Click graph nodes in sequence to set START, then DESTINATION; dropdowns are also available.
- Reset button restores a default start/destination pair. Same-location routes are rejected.
- Select Walk, Bike, Car or Bus sample mode and optimize by distance, time or estimated cost.
- Compare Dijkstra, BFS and A* with route distance, stop count, visited nodes and execution time.
- The selected route animates edge-by-edge on the schematic graph.
- Step-by-step directions and an algorithm comparison panel are displayed with each result.
- BFS minimizes hops/edges, so it may not minimize distance, time or cost. Dijkstra and A* optimize
  the selected weight. Execution-time figures are local demonstration measurements and can vary.
- This remains a schematic graph, not a geographically accurate campus map; accessibility constraints
  such as stairs are not represented because the sample graph has no accessibility metadata.
