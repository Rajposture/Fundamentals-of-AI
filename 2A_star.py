# Exp 6 A* Search using heap and user input

import heapq

graph = {}
heuristic = {}

n = int(input("Enter number of nodes: "))
for i in range(n):
    node = input("Enter node name: ")
    edges = input(f"Enter neighbors of {node} with cost like B,4 C,2 : ").split()
    edge_list = []

    for e in edges:
        name, cost = e.split(",")
        edge_list.append((name, int(cost)))

    graph[node] = edge_list

for node in graph:
    h = int(input(f"Enter heuristic value for {node}: "))
    heuristic[node] = h

start = input("Enter start node: ")
goal = input("Enter goal node: ")

g_cost = {start: 0}
pq = []
heapq.heappush(pq, (heuristic[start], start))
visited = []

while pq:
    f_val, curr = heapq.heappop(pq)

    if curr in visited:
        continue

    print(curr, end=" ")
    visited.append(curr)

    if curr == goal:
        print("\nGoal reached with cost", g_cost[curr])
        break

    for nb, cost in graph[curr]:
        new_g = g_cost[curr] + cost

        if nb not in g_cost or new_g < g_cost[nb]:
            g_cost[nb] = new_g
            f = new_g + heuristic[nb]
            heapq.heappush(pq, (f, nb))