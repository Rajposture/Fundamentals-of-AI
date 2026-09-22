import heapq

graph = {}

n = int(input("Enter number of nodes: "))

for i in range(n):
    node = input("Enter node name: ")
    neighbors = input(f"Enter neighbors of {node}: ").split()
    graph[node] = neighbors

start = input("Enter start node: ")

visited = set()
heap = []
count = 0

heapq.heappush(heap, (-count, start))
visited.add(start)

while heap:
    _, curr = heapq.heappop(heap)
    print(curr, end=" ")

    for nb in reversed(graph[curr]):
        if nb not in visited:
            count += 1
            visited.add(nb)
            heapq.heappush(heap, (-count, nb))

print("\nDFS traversal done")