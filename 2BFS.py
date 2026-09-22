import heapq

graph = {}

n = int(input("Enter number of nodes: "))

for i in range(n):
    node = input("Enter node name: ")
    neighbors = input("Enter neighbors separated by space: ").split()
    graph[node] = neighbors

start = input("Enter start node: ")

visited = []
heap = []

heapq.heappush(heap, start)
visited.append(start)

while heap:
    curr = heapq.heappop(heap)
    print(curr, end=" ")

    for nb in graph[curr]:
        if nb not in visited:
            visited.append(nb)
            heapq.heappush(heap, nb)

print("\nTraversal done")