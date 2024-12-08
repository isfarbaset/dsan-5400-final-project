import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

def generate_er_diagram(entities, relationships):
    if not entities:
        raise ValueError("No entities provided for diagram generation.")
    if not relationships:
        raise ValueError("No relationships provided for diagram generation.")
    G = nx.Graph()
    G.add_nodes_from(entities)
    
    for source, target, label in relationships:
        logger.debug(f"Adding edge: {source} -> {target} with label: {label}")

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=3000, font_size=10, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Entity Relationship Diagram", fontsize=16)
    plt.axis('off')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{graph_url}"
