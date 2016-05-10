import os
import cPickle as pickle
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from collections import defaultdict

filename = os.path.join(os.getcwd(), 'project/static/website_necessities.pickle')
course_id_lookup_dict, class_number_lookup_dict, course_cluster_probs_dict, k, vectorizer, tfidf_mat, word_dict, course_doc_dict, course_id_list, course_info_dict, course_association_dictionary = pickle.load(open(filename, 'rb'))
 
G = nx.Graph()
G.add_nodes_from(course_id_list)
for course_id, mentions in course_association_dictionary.items():
	for mention in mentions:
		if not course_id == mention:
			G.add_edge(course_id, mention)	

for node in G.nodes():
	if G.degree(node) == 0:
		G.remove_node(node)

labels_dict = defaultdict(str)
for key, val in class_number_lookup_dict.items():
	if key in G.node:
		labels_dict[key] = ' '.join(val)

nx.draw_networkx(G, node_size=50, font_size=10, labels=labels_dict)
plt.show()