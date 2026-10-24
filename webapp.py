from flask import Flask, render_template, request, jsonify
from algorithms.dijkstra import dijkstra
from algorithms.bfs import bfs
from algorithms.astar import astar
from algorithms.floyd_warshall import floyd_warshall

app = Flask(__name__)

# Demonstration graph weights only; these are sample estimates, not live traffic/road data.
BASE = {
 "Chandigarh University":{"Landran":(8.0,16,18),"Kharar Bus Stand":(10.5,22,22),"North Country Mall":(7.0,14,16),"Mohali":(18.0,34,35)},
 "Landran":{"Chandigarh University":(8.0,16,18),"Mohali":(10.0,20,22),"ISB Mohali":(7.0,14,16),"Kharar Bus Stand":(11.0,23,24)},
 "Kharar Bus Stand":{"Chandigarh University":(10.5,22,22),"Landran":(11.0,23,24),"North Country Mall":(5.5,12,12),"Home (Kharar)":(4.0,9,9)},
 "North Country Mall":{"Chandigarh University":(7.0,14,16),"Kharar Bus Stand":(5.5,12,12),"Home (Kharar)":(8.0,16,18),"Mohali":(14.0,27,30)},
 "Home (Kharar)":{"Kharar Bus Stand":(4.0,9,9),"North Country Mall":(8.0,16,18),"Chandigarh":(12.8,24,34),"Mohali":(8.7,18,24),"PGI Chandigarh":(16.1,30,42)},
 "Mohali":{"Chandigarh University":(18.0,34,35),"Landran":(10.0,20,22),"Home (Kharar)":(8.7,18,24),"Chandigarh":(6.9,14,20),"PGI Chandigarh":(10.4,22,30),"Shaheed Bhagat Singh Airport":(9.0,18,24),"ISB Mohali":(6.0,12,14)},
 "ISB Mohali":{"Landran":(7.0,14,16),"Mohali":(6.0,12,14),"Shaheed Bhagat Singh Airport":(12.0,22,28)},
 "Shaheed Bhagat Singh Airport":{"Mohali":(9.0,18,24),"ISB Mohali":(12.0,22,28),"Chandigarh":(18.0,32,48)},
 "Chandigarh":{"Home (Kharar)":(12.8,24,34),"Mohali":(6.9,14,20),"PGI Chandigarh":(5.1,12,18),"Sector 22 Market":(2.2,7,10),"Elante Mall":(7.5,16,22),"Sukhna Lake":(8.0,18,0),"Shaheed Bhagat Singh Airport":(18.0,32,48)},
 "PGI Chandigarh":{"Home (Kharar)":(16.1,30,42),"Chandigarh":(5.1,12,18),"Mohali":(10.4,22,30),"Sector 22 Market":(4.4,11,16),"Sukhna Lake":(6.0,14,0)},
 "Sector 22 Market":{"Chandigarh":(2.2,7,10),"PGI Chandigarh":(4.4,11,16),"Elante Mall":(6.5,14,20)},
 "Elante Mall":{"Chandigarh":(7.5,16,22),"Sector 22 Market":(6.5,14,20),"Sukhna Lake":(10.0,22,0)},
 "Sukhna Lake":{"Chandigarh":(8.0,18,0),"PGI Chandigarh":(6.0,14,0),"Elante Mall":(10.0,22,0)}
}

@app.get('/')
def index():
    return render_template('index.html', locations=sorted(BASE))

@app.post('/api/route')
def route():
    data = request.get_json(force=True)
    start, end = data.get('start'), data.get('end')
    mode = data.get('mode', 'Bike')
    priority = data.get('priority', 'Fastest')
    if start not in BASE or end not in BASE:
        return jsonify(error='Please select two locations from the list.'), 400
    if start == end:
        return jsonify(error='Start and destination must be different.'), 400
    factor = {'Bike':1.0,'Car':0.82,'Bus':1.18,'Walk':2.8}.get(mode, 1.0)
    cost_factor = {'Bike':1,'Car':1.5,'Bus':0.55,'Walk':0}.get(mode, 1)
    graph = {node:{} for node in BASE}
    for node, edges in BASE.items():
        for other, (distance, minutes, cost) in edges.items():
            graph[node][other] = {'distance':distance,'time':max(1,minutes*factor),'cost':cost*cost_factor}
    weight = {'Fastest':'time','Shortest Distance':'distance','Lowest Cost':'cost'}.get(priority,'time')
    result = dijkstra(graph, start, end, weight)
    if not result:
        return jsonify(error='No route found between these locations.'), 404
    path = result['path']; total = {'distance':0.0,'time':0.0,'cost':0.0}
    for a,b in zip(path,path[1:]):
        for k in total: total[k] += graph[a][b][k]
    return jsonify(start=start,end=end,path=path,distance=round(total['distance'],1),minutes=round(total['time']),cost=round(total['cost']),visited=result['visited_nodes'],priority=priority,mode=mode)

@app.get('/health')
def health():
    return {'status':'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= int(__import__('os').environ.get('PORT', 5000)))
