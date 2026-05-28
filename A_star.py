from queue import PriorityQueue

graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('D', 4), ('E', 2)],
    'C': [('F', 5)],
    'D': [],
    'E': [('G', 3)],
    'F': [('G', 2)],
    'G': []
}

h = {
    'A': 7,
    'B': 5,
    'C': 4,
    'D': 4,
    'E': 2,
    'F': 1,
    'G': 0
}

def a_star(start, goal):
    pq = PriorityQueue()
    pq.put((h[start], 0, start, [start]))
    visited = set()
    while not pq.empty():
        f, cost, node, path = pq.get()
        if node == goal:
            print("Path Found:", path)
            print("Total Cost:", cost)
            return
        if node in visited:
            continue
        visited.add(node)
        for next_node, edge_cost in graph[node]:
            new_cost = cost + edge_cost
            f_cost = new_cost + h[next_node]
            pq.put((f_cost,
                    new_cost,
                    next_node,
                    path + [next_node]))

    print("Goal Not Found")


a_star('A', 'G')