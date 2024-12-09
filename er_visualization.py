# import networkx as nx
# import matplotlib.pyplot as plt
# import io
# import base64
# import logging
# import matplotlib
# matplotlib.use('Agg')

# logger = logging.getLogger(__name__)

# def generate_er_diagram(entities, relationships):
#     try:
#         G = nx.Graph()
        
#         # Add nodes (entities)
#         entity_labels = {}
#         for entity in entities:
#             # Use entity text as node identifier
#             node_id = entity.get('text', str(entity))
#             G.add_node(node_id)
#             entity_labels[node_id] = node_id

#         # Add edges (relationships)
#         for rel in relationships:
#             source = rel.get('entity1', {}).get('text', '')
#             target = rel.get('entity2', {}).get('text', '')
#             label = rel.get('relationship', 'relates to')
            
#             if source and target:
#                 G.add_edge(source, target, label=label)

#         plt.figure(figsize=(12, 8))
#         pos = nx.spring_layout(G)
        
#         # Draw nodes
#         nx.draw(G, pos, with_labels=True, labels=entity_labels,
#                 node_color='lightblue', node_size=3000, 
#                 font_size=10, font_weight='bold')
        
#         # Draw edge labels
#         edge_labels = nx.get_edge_attributes(G, 'label')
#         nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

#         plt.title("Entity Relationship Diagram", fontsize=16)
#         plt.axis('off')
#         plt.tight_layout()

#         # Convert to base64
#         img = io.BytesIO()
#         plt.savefig(img, format='png', bbox_inches='tight')
#         img.seek(0)
#         graph_url = base64.b64encode(img.getvalue()).decode()
#         plt.close()

#         return f"data:image/png;base64,{graph_url}"
#     except Exception as e:
#         logger.error(f"Error generating ER diagram: {str(e)}")
#         raise