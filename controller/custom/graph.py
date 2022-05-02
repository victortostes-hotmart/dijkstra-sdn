from Queue import PriorityQueue;
from collections import defaultdict;

class Graph:
  def __init__(self):
    self.v = 0;
    self.edges = [];
    self.nodes = {};
    self.adjacency = defaultdict(lambda : defaultdict(lambda : None));

  def add_node(self, node):
    if node in self.nodes:
      return;
    
    self.v += 1;
    self.nodes[node] = node;
    
    if len(self.edges) != 0:
      for i in range(self.v - 1):
        self.edges[i].extend([-1]);
    
    self.edges.append([-1 for i in range(self.v)]);
  
  def add_edge(self, sw1, sw2, pt1, pt2, weight = 1):
    self.edges[sw1 - 1][sw2 - 1] = weight;
    
    if self.adjacency[sw1][sw2] is None:
      self.adjacency[sw1][sw2] = pt1;
      self.adjacency[sw2][sw1] = pt2;

  def remove_edge(self, sw1, sw2):
    self.edges[sw1 - 1][sw2 - 1] = -1;
    
    if sw2 in self.adjacency[sw1]:
        del self.adjacency[sw1][sw2];
    if sw1 in self.adjacency[sw2]:
        del self.adjacency[sw2][sw1];

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

  def find_shortest_path(self, src, dst):
      switch_src = src[0];
      port_src = src[1];

      switch_dst = dst[0];
      port_dst = dst[1];

      # Find shortest path to all graph nodes starting from source switch;
      routes = self.dijkstra(switch_src);
      switches_path = routes[switch_dst];
      
      path = [];
      in_port = port_src;
      
      for s1,s2 in zip(switches_path[:-1],switches_path[1:]):
          out_port = self.adjacency[s1][s2];
          path.append((s1,in_port,out_port));
          in_port = self.adjacency[s2][s1];
      
      path.append((switch_dst,in_port,port_dst));

      return path;
