# Alana Wesly, ICS 311 Assignment 5 - a Sea of Islands
# Algorithms for plantable resources to be shared across islands 
import heapq

# adjacency list for islands and their weighted edges for travel times
graph = {
    "Oahu": {"Molokai": 1, "Lanai": 3, "Maui": 4},
    "Molokai": {"Hawaii": 8},
    "Lanai": {"Hawaii": 6},
    "Maui": {"Hawaii": 5},
    "Hawaii": {},
    "Kauai": {},
    "Niihau": {}
}

# adjacency list of islands resources / attributes
attributes = {
    "Oahu": {"population": 1000, "resources": ["uala"], "experiences": ["surfing"]},
    "Molokai": {"population": 300, "resources": [], "experiences": ["fishing"]},
    "Lanai": {"population": 200, "resources": [], "experiences": ["hiking"]},
    "Maui": {"population": 600, "resources": [], "experiences": ["snorkeling"]},
    "Hawaii": {"population": 800, "resources": [], "experiences": ["volcano tours"]},
    "Kauai": {"population": 500, "resources": [], "experiences": ["gardens"]},
    "Niihau": {"population": 50, "resources": [], "experiences": ["shell collecting"]}
}

#  find the shortest routes with Dijkstra's Algorithm
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph[node].items():
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                heapq.heappush(heap, (dist[neighbor], neighbor))
    return dist

# make route order queue
def build_delivery_queue(distances, source):
    queue = []
    for island, dist in distances.items():
        if island != source and dist < float('inf'):
            heapq.heappush(queue, (dist, island))
    return queue

# use min order heap to assign routes to canoes
def assign_deliveries(queue, canoes_available, distances):
    delivery_log = []
    canoe_heap = [(0, i) for i in range(canoes_available)]  # (available_time, canoe_id)
    heapq.heapify(canoe_heap)

    while queue:
        travel_time, island = heapq.heappop(queue)
        available_time, canoe_id = heapq.heappop(canoe_heap)
        delivery_log.append((canoe_id, island, travel_time))
        return_time = available_time + 2 * travel_time
        heapq.heappush(canoe_heap, (return_time, canoe_id))

    return delivery_log

# example testing 
# set the source island and number of canoes
source_island = "Oahu"
canoes = 2
# use the algorithms
distances = dijkstra(graph, source_island)
delivery_queue = build_delivery_queue(distances, source_island)
delivery_plan = assign_deliveries(delivery_queue, canoes, distances)
# print the result
print(delivery_plan)
