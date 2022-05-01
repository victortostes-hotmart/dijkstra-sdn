from Queue import PriorityQueue

class Graph:
  def __init__(self):
    self.v = 0;
    self.edges = [];
    self.nodes = {};

  def add_node(self, node):
    if node in self.nodes:
      return;
    
    self.v += 1;
    self.nodes[node] = node;
    
    if len(self.edges) != 0:
      for i in range(self.v - 1):
        self.edges[i].extend([-1]);
    
    self.edges.append([-1 for i in range(self.v)]);
  
  def add_edge(self, u, v, weight = 1):
    self.edges[u - 1][v - 1] = weight;

  def remove_edge(self, u, v):
    self.edges[u - 1][v - 1] = -1;

  def dijkstra(self, start_vertex):
    visited = [];
  
    S ={(v+1):({'distance': float('inf'), 'prev': None}) for v in range(self.v)};
    S[start_vertex]['distance'] = 0;
    S[start_vertex]['prev'] = None;

    pq = PriorityQueue();
    pq.put((0, start_vertex));

    while not pq.empty():
      (dist, current_vertex) = pq.get();
      visited.append(current_vertex - 1);

      for neighbor in range(self.v):
        if self.edges[current_vertex - 1][neighbor] != -1:
          distance = self.edges[current_vertex - 1][neighbor];
          if neighbor not in visited:
            old_cost = S[neighbor + 1]['distance'];
            new_cost = S[current_vertex]['distance'] + distance;
            if new_cost < old_cost:
              pq.put((new_cost, neighbor + 1));
              S[neighbor + 1]['distance'] = new_cost;
              S[neighbor + 1]['prev'] = current_vertex;

    
    paths = {};
    for node in S:
      path = [];
      target = node;
      while S[target]['prev'] is not None:
        path.insert(0, S[target]['prev']);
        target = S[target]['prev'];
      
      path.append(node);
      paths[node] = path;

    return paths;