# First, let's load the JSON data to understand its structure
import json

# Load the JSON data from the provided file
with open('C:\\Users\\josep\\OneDrive\\Documents\\learninghsbc\\data.json', 'r') as file:
    json_data = json.load(file)

# Extract the nodes (apps and countries) and the links (communication between apps)
nodes = []
links = []
country_to_apps = {}

# Process the data to create nodes and links
for binding in json_data['results']['bindings']:
    app = binding['app']['value']
    country = binding['country']['value']
    upapp = binding.get('upappid', {}).get('value')

    # Add country nodes
    if country not in country_to_apps:
        country_to_apps[country] = {
            'name': country,
            'apps': []
        }
        nodes.append({
            'id': country,
            'group': country,
            'label': country,
            'level': 1
        })

    # Add app nodes and link to country
    country_to_apps[country]['apps'].append(app)
    nodes.append({
        'id': app,
        'group': country,
        'label': 'App ' + app,
        'level': 2
    })
    links.append({
        'source': country,
        'target': app
    })

    # Add links between apps
    if upapp:
        links.append({
            'source': app,
            'target': upapp
        })

# Nodes are ready, let's print them out
print("Nodes:")
print(json.dumps(nodes, indent=2))

# Links are ready too, let's print them out
print("\nLinks:")
print(json.dumps(links, indent=2))

# Now we will visualize this data using NetworkX and Matplotlib
import networkx as nx
import matplotlib.pyplot as plt

# Create a graph object
G = nx.MultiDiGraph()

# Add nodes and edges to the graph
for node in nodes:
    G.add_node(node['id'], label=node['label'], group=node['group'], level=node['level'])

for link in links:
    G.add_edge(link['source'], link['target'])

# Generate positions for each node using the spring layout
pos = nx.spring_layout(G)

# Draw the nodes and the edges (including the width for the edges and labels for the nodes)
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=500, node_color=[G.nodes[node]['level'] for node in G.nodes], cmap=plt.cm.Reds)
plt.show()

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

# Add node positions and info to the trace
for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += (x,)
    node_trace['y'] += (y,)
    node_trace['text'] += (G.nodes[node]['label'],)

# Create trace of edges
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

# Add edge positions to the trace
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += (x0, x1, None)
    edge_trace['y'] += (y0, y1, None)

# Create the figure
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://networkx.org/'> NetworkX</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

# Display the figure
fig.show()
