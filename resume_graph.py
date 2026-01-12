import json
import networkx as nx
import matplotlib.pyplot as plt

def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
def resume_graph(data):
    G = nx.Graph()

    for person in data:
        person_name = person["name"]
        person_role = person["role"]

        G.add_node(person_name, type = "candidate", role = person_role)

        for skill in person["skills"]:
            skill_name = skill["name"]
            exp = skill["years_experience"]

            G.add_node(skill_name, type = "skill")

            G.add_edge(person_name, skill_name, weight = exp)

    return G

def visualize(G):
    plt.figure(figsize = (20,15))
    
    pos = nx.spring_layout(G, k = 0.8, iterations = 100, seed = 42)

    candidate_nodes = [n for n, attr in G.nodes(data = True) if attr["type"] == "candidate"]
    skill_nodes = [n for n, attr in G.nodes(data = True) if attr["type"] == "skill"]

    nx.draw_networkx_nodes(G, pos, nodelist = candidate_nodes, node_color = "lightblue", node_size = 2000, label = "Candidates")

    nx.draw_networkx_nodes(G, pos, nodelist = skill_nodes, node_color = "lightgreen", node_size = 1000, label = "Skills")

    nx.draw_networkx_labels(G, pos, font_size = 9, font_weight = "bold")

    nx.draw_networkx_edges(G, pos, width = 1.5, alpha = 0.3, edge_color = "gray")

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, font_size = 8)

    plt.legend(loc = "upper right")
    plt.title("Knowledge Graph for Resumes")
    plt.axis("off")

    plt.show()

if __name__ == "__main__":
    resumes = load_data("resume.json")
    G = resume_graph(resumes)
    visualize(G)