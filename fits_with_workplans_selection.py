import networkx as nx
import matplotlib.pyplot as plt

disass = 'disass'
assembled = 'assembled'
workplan = 'workplan'
dic = {assembled: 'green', disass: 'red', workplan: 'violet'}
class Chart:
    def __init__(self, Nodes):
        self.nodes = Nodes
        self.adj_list = {}
        self.g = nx.DiGraph()

        for node in self.nodes:
            self.adj_list[node] = []
    def add_nodes_graph(self, node, x):
        self.g.add_node(node, color = x)
    def add_edge_graph(self, u, v, z, t):
        self.g.add_edge(u, v, weight = z, color = t)
    def add_edge_workplan_graph(self, u, v, t):
        self.g.add_edge(u, v, color = t)
    def add_edge(self, u, v, z):
        a = []
        a.append(v)
        a.append(z)
        b = []
        b.append(u)
        b.append(z)
        self.adj_list[u].append(a)
        self.adj_list[v].append(b)
    def disass_adj_list(self):
        self.disass_adj_list = {}
        for node in self.nodes:
            if self.nodes[node] == disass:
                self.disass_adj_list[node]=self.adj_list[node]
                print (node, '->', self.disass_adj_list[node])
            else:
                continue

edges = [['High Pressure Turbine Case', 'Low Pressure Turbine Case', '2863', 'assembled'],
         ['Low Pressure Turbine Case', 'Turbine Exhaust Case Assembly', '2864', 'assembled'],
         ['Turbine Exhaust Case Assembly', 'No. 5 Bearing Housing Assembly', '1000', 'assembled'],
         ['No. 5 Bearing Rear Seal Support Assembly', 'No. 5 Bearing Housing Assembly', '1005', 'assembled'],
         ['No. 5 Bearing Housing Assembly', 'Cylindrical Roller Bearing Ring', '1004', 'assembled'],
         ['No. 5 Bearing Housing Assembly', 'No. 6 Bearing Housing Assembly', '1001', 'assembled'],
         ['No. 6 Bearing Housing Assembly', 'No. 6 Bearing Outer Housing Assembly', '1002', 'assembled'],
         ['No. 6 Bearing Outer Housing Assembly', 'Cylindrical Roller Bearing Ring', '1003', 'assembled']]
workplans = [['Q72-52-00FM01E', 'High Pressure Turbine Case', 'workplan'],
             ['Q72-53-00FM01E', 'Low Pressure Turbine Case', 'workplan'],
             ['Q72-54-04FM01E', 'Turbine Exhaust Case Assembly', 'workplan'],
             ['Q72-54-00FM01E', 'No. 5 Bearing Rear Seal Support Assembly', 'workplan'],
             ['Q72-54-00FM01E', 'No. 5 Bearing Housing Assembly', 'workplan'],
             ['Q72-54-00FM01E', 'No. 6 Bearing Housing Assembly', 'workplan'],
             ['Q72-54-00FM01E', 'No. 6 Bearing Outer Housing Assembly', 'workplan'],
             ['Q72-54-00FM01E', 'Cylindrical Roller Bearing Ring', 'workplan']]
workplans_dictionary = {}
for k in workplans:
    workplans_dictionary[k[1]]=k[0]
        
pre_nodes = [('High Pressure Turbine Case', 'assembled'),
             ('Low Pressure Turbine Case', 'assembled'),
             ('Turbine Exhaust Case Assembly', 'assembled'),
             ('No. 5 Bearing Housing Assembly', 'assembled'),
             ('No. 5 Bearing Rear Seal Support Assembly', 'assembled'),
             ('No. 6 Bearing Housing Assembly', 'assembled'),
             ('No. 6 Bearing Outer Housing Assembly', 'assembled'),
             ('Cylindrical Roller Bearing Ring', 'assembled'),
             ('Q72-52-00FM01E', 'workplan'),
             ('Q72-53-00FM01E', 'workplan'),
             ('Q72-54-04FM01E', 'workplan'),
             ('Q72-54-00FM01E', 'workplan')]

nodes = dict(pre_nodes)
while True:
    print('Do you want to change the status of the part? ')
    decision = input()
    if decision != 'yes':
        break
    else:
        part = input()
        status = input()
        nodes[part] = status
    for y in edges:
        indx = edges.index(y)
        if part in y:
            edges[indx][3]=status

graph = Chart(nodes)
for node, x in nodes.items():
    graph.add_nodes_graph(node, x)
for u, v, z, t in edges:
    graph.add_edge_graph(u, v, z, t)
    graph.add_edge(u, v, z)
for u, v, t in workplans:
    graph.add_edge_workplan_graph(u, v, t)
print('Disassembled parts and adjacent parts to them: ')
graph.disass_adj_list()
for node in graph.disass_adj_list.keys():    
    variable = graph.disass_adj_list[node]
    for inception in variable:
        if (inception[0] in graph.disass_adj_list.keys()) and (workplans_dictionary[inception[0]] == workplans_dictionary[node]):
            print(node + ' ->' + ' Docu sheet -> ' + inception[1] + ' with ' + inception[0])
        else:
            print(node + ' ->' + ' Split-line sheet -> ' + inception[1])

weight = nx.get_edge_attributes(graph.g, 'weight')
color_edge = nx.get_edge_attributes(graph.g, 'color')
color = nx.get_node_attributes(graph.g, 'color')
pos = nx.shell_layout(graph.g)
    
nx.draw_networkx(graph.g, pos, arrows = False, node_color = [dic[x] for x in color.values()],
                 edge_color =[dic[x] for x in color_edge.values()], font_size = 8)
nx.draw_networkx_edge_labels(graph.g, pos, edge_labels=weight, font_size = 8)
plt.show()
    


