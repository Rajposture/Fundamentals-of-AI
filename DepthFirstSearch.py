# Exp 4 Depth first search using heap and user input

graph = {}

n = int(input("Enter number of nodes: "))
for i in range(n):
    node = input("Enter node name: ")
    neighbors = input(f"Enter neighbors of {node} separated by space: ").split()
    graph[node] = neighbors

start = input("Enter start node: ")
visited = []

def dfs(node):
    if node not in visited:
        print(node, end=" ")
        visited.append(node)

        for nb in graph[node]:
            dfs(nb)

dfs(start)

print("\nDFS traversal done")