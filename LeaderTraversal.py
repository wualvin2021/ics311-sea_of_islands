# note that this code also uses plantableResources.py attributes to function 
#
# Scoring weights
X = 1.0  # population importance
Y = 1.0  # recency importance

def get_priority_score(island, current_time):
    pop = attributes[island]["population"]
    recency = current_time - last_visit[island]
    return X * pop + Y * recency

def leader_traversal(start_island, max_steps=15):
    current_island = start_island
    current_time = 0
    path = [current_island]

    for _ in range(max_steps):
        last_visit[current_island] = current_time
        neighbors = graph[current_island]
        heap = []

        # Score each neighbor and push into heap
        for neighbor, travel_time in neighbors.items():
            score = get_priority_score(neighbor, current_time)
            efficiency = score / travel_time
            heapq.heappush(heap, (-efficiency, travel_time, neighbor))

        if not heap:
            # Restart from most overdue island
            most_overdue = max(last_visit.items(), key=lambda x: current_time - x[1])[0]
            print(f"\n[Restarting from overdue island: {most_overdue}]")
            current_island = most_overdue
            current_time += 1  # small time to "restart"
            path.append(current_island)
            continue

        # Travel to next best island
        _, travel_time, next_island = heapq.heappop(heap)
        current_time += travel_time
        current_island = next_island
        path.append(current_island)

    return path

# Run the leader traversal
tour = leader_traversal("Oahu")

# Print the result
print("\nLeader Tour Sequence:")
for i, island in enumerate(tour, 1):
    print(f"{i}. {island}")

