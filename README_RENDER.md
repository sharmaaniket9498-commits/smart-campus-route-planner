# Smart Campus Route Planner — Docker + Render Web Version

This repository now includes a web entry point (`webapp.py`) while retaining the original CustomTkinter desktop application (`app.py`) and its routing algorithm modules.

## Deploy on Render with Docker

1. Push these changes to the existing GitHub repository's `main` branch.
2. Open https://dashboard.render.com/ and choose **New + → Web Service**.
3. Connect the existing `sharmaaniket9498-commits/smart-campus-route-planner` repository.
4. Choose **Docker** as the runtime (Render should detect the included `Dockerfile`).
5. Use branch `main`; leave the Dockerfile path as `./Dockerfile`; choose the Free plan if available.
6. Click **Create Web Service** and wait for the build/deploy to finish. Open the `onrender.com` URL Render provides.

Alternatively, use **New + → Blueprint** and select this repository to use `render.yaml`.

## Features

- Home dashboard with navigation only (no theory text on Home)
- Route planning using the project's Dijkstra implementation and sample weights
- Graph Explorer with a highlighted route; no algorithm comparison panel
- Saved custom places stored in the current browser's local storage
- Separate Theory page covering Dijkstra, BFS, A*, Floyd–Warshall and weighted graphs
- Docker deployment and `/health` endpoint

All distances, times and costs are illustrative estimates. No live traffic, GPS or map provider is used. Saved custom places are local to each browser and do not sync between devices.
