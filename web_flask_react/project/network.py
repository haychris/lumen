import os
import cPickle as pickle
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from collections import defaultdict

filename = os.path.join(os.getcwd(),
                        'project/static/website_necessities.pickle')
course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, k, vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list, course_info_dict, course_association_dictionary, pagerank_dict = pickle.load(
    open(filename, 'rb'))

G = nx.Graph()
G.add_nodes_from(course_id_list)
for course_id, mentions_dict in course_association_dictionary.items():
    for mention, num in mentions_dict.items():
        if not course_id == mention:
            if (course_id, mention) in G.edges():
                G.add_edge(
                    course_id,
                    mention,
                    weight=num + G.edge[course_id][mention]['weight'])
            elif (mention, course_id) in G.edges():
                G.add_edge(
                    mention,
                    course_id,
                    weight=num + G.edge[mention][course_id]['weight'])
            else:
                G.add_edge(course_id, mention, weight=num)

for node in G.nodes():
    if G.degree(node) == 0:
        G.remove_node(node)

labels_dict = defaultdict(str)
for key, val in class_number_lookup_dict.items():
    if key in G.node:
        labels_dict[key] = ' '.join(val)

# nx.draw_networkx(G, node_size=50, font_size=10, labels=labels_dict)
# plt.show()

pagerank_dict = nx.pagerank(G)
print 'PAGERANK'
for val, key in sorted(
    [(val, key) for key, val in pagerank_dict.items()], reverse=True)[:10]:
    print labels_dict[key], ':', val

hubs, authorities = nx.hits(G)
print 'HUBS'
for val, key in sorted(
    [(val, key) for key, val in hubs.items()], reverse=True)[:10]:
    print labels_dict[key], ':', val

print 'AUTHORITIES'
for val, key in sorted(
    [(val, key) for key, val in authorities.items()], reverse=True)[:10]:
    print labels_dict[key], ':', val

mean = lambda x: 1. * sum(x) / len(x)
print 'Mean degree', mean(nx.degree(G).values())
print 'Max degree', max(nx.degree(G).values())
print 'TOP DEGREE NODES'
for val, key in sorted(
    [(val, key) for key, val in nx.degree(G).items()], reverse=True)[:10]:
    print labels_dict[key], ':', val

for size, clique_list in sorted(
    [(len(clique_list), clique_list) for clique_list in nx.find_cliques(G)],
        reverse=True)[:10]:
    print [labels_dict[k] for k in clique_list], ':', size

richclub = nx.rich_club_coefficient(G)

subgraphs = [
    g
    for size, g in sorted(
        [(g.number_of_nodes(), g)
         for g in nx.connected_component_subgraphs(G)],
        reverse=True)
]
for i, g in enumerate(subgraphs[:10]):
    print 'For subgraph', i
    print 'Number of nodes', g.number_of_nodes()
    print 'Number of edges', g.number_of_edges()
    print 'Mean degree', mean(nx.degree(g).values())
    print 'Max degree', max(nx.degree(g).values())
    print 'Center:', [labels_dict[k] for k in nx.center(g)]
    print 'Radius:', nx.radius(g)
    print 'Eccentricity', mean(nx.eccentricity(g).values())
    # print 'Avg. Node Connectivity', nx.average_node_connectivity(g)
    print 'Avg. Shortest Path Length', nx.average_shortest_path_length(g)
    cur_labels_dict = defaultdict(str)
    for key, val in class_number_lookup_dict.items():
        if key in g.node:
            cur_labels_dict[key] = val[0]
    nx.draw_networkx(
        g,
        linewidths=0,
        node_color='#33ccff',
        edge_color='#cccccc',
        labels=cur_labels_dict)
    plt.show()
