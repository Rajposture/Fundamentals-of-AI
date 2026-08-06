# Exp 3 Breadth first search using heap and user input

from collections import deque

graph = {}

n = int(input("Enter number of nodes: "))
for i in range(n):
    node = input("Enter node name: ")
    neighbors = input(f"Enter neighbors of {node} separated by space: ").split()
    graph[node] = neighbors

start = input("Enter start node: ")

visited = []
q = deque()

q.append(start)
visited.append(start)

while q:
    curr = q.popleft()
    print(curr, end=" ")

    for nb in graph[curr]:
        if nb not in visited:
            visited.append(nb)
            q.append(nb)

print("\nBFS traversal done")