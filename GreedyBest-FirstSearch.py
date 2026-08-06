# Exp 5 Greedy-BEST first search using heap and user input

import heapq

graph = {}
heuristic = {}

n = int(input("Enter number of nodes: "))
for i in range(n):
    node = input("Enter node name: ")
    neighbors = input(f"Enter neighbors of {node} separated by space: ").split()
    graph[node] = neighbors

for node in graph:
    h = int(input(f"Enter heuristic value for {node}: "))
    heuristic[node] = h

start = input("Enter start node: ")
goal = input("Enter goal node: ")

visited = []
pq = []
heapq.heappush(pq, (heuristic[start], start))

while pq:
    h_val, curr = heapq.heappop(pq)

    if curr in visited:
        continue

    print(curr, end=" ")
    visited.append(curr)

    if curr == goal:
        print("\nGoal reached")
        break

    for nb in graph[curr]:
        if nb not in visited:
            heapq.heappush(pq, (heuristic[nb], nb))