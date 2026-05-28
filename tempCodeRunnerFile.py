def dfs(node, result, visited, adj):
    visited[node] = 1
    result.append(node)

    for n in adj[node]:
        if visited[n] == 0:
            dfs(n, result, visited, adj)

adj = [[], [2,4], [1,3,6], [2], [1,5,7], [4,8], [2], [4,8], [5,7]]

number_of_nodes = len(adj) - 1

visited = [0] * (number_of_nodes + 1)
result = []

dfs(1, result, visited, adj)

print("Depth First Search OUTPUT ARRAY:")
print(result)