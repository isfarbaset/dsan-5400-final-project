document.getElementById("fetchButton").addEventListener("click", function () {
    const query = document.getElementById("queryInput").value;
    console.log("Fetch button clicked!"); // Log when the button is clicked
    console.log("Search query:", query);  // Log the entered query

    fetch(`/api/fetch?query=${encodeURIComponent(query)}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            console.log("API Response Data:", data); // Log full API response

            if (data.results && data.results.length > 0) {
                const firstResult = data.results[0];

                // Render Entities and Relationships
                renderEntities(firstResult.entities || []);
                renderRelationships(firstResult.relationships || []);

                // Render Graph Visualization (if applicable)
                renderGraph(firstResult.entities || [], firstResult.relationships || []);

                // Render ER Diagram
                if (data.er_diagram) {
                    renderERDiagram(data.er_diagram);
                }
            } else {
                alert("No articles found!");
            }
        })
        .catch((error) => {
            console.error("Error fetching articles:", error);
            alert("An error occurred while fetching articles. Please try again.");
        });
});

function renderEntities(entities) {
    const entitiesList = document.getElementById("entities");
    entitiesList.innerHTML = ""; // Clear previous results

    entities.forEach((entity) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${entity.label || 'Unknown'}: ${entity.text || 'N/A'}`;
        listItem.className = "list-group-item";
        entitiesList.appendChild(listItem);
    });
}

function renderRelationships(relationships) {
    console.log("Relationships Data:", relationships); // Log the relationships data for debugging
    const relationshipsList = document.getElementById("relationships");
    relationshipsList.innerHTML = ""; // Clear previous results

    relationships.forEach((relationship) => {
        const entity1Text = relationship.entity1?.text || "Unknown";
        const entity2Text = relationship.entity2?.text || "Unknown";
        const relationType = relationship.relationship || "related-to";

        const listItem = document.createElement("li");
        listItem.textContent = `${entity1Text} ${relationType} ${entity2Text}`;
        listItem.className = "list-group-item";
        relationshipsList.appendChild(listItem);
    });
}


function renderGraph(entities, relationships) {
    const graphContainer = document.getElementById("graph-container");
    graphContainer.innerHTML = ""; // Clear previous content

    const width = 600;
    const height = 400;

    // Prepare data for D3
    const nodes = entities.map(e => ({ id: e.text, group: e.label }));
    const links = relationships.map(r => ({
        source: r.entity1.text,
        target: r.entity2.text,
        value: 1
    }));

    // Create SVG
    const svg = d3.select(graphContainer)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    // Create links
    const link = svg.append("g")
        .selectAll("line")
        .data(links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6);

    // Create nodes
    const node = svg.append("g")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("r", 5)
        .attr("fill", d => d3.schemeCategory10[d.group.charCodeAt(0) % 10]);

    // Add titles to nodes
    node.append("title")
        .text(d => d.id);

    // Update positions on each tick of the simulation
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });
}

// function renderERDiagram(erDiagramData) {
//     const graphImage = document.getElementById('relationship-graph');
//     if (!erDiagramData) {
//         graphImage.style.display = 'none';
//         return;
//     }
    
//     if (graphImage && graphImage.tagName === 'IMG') {
//         graphImage.style.display = 'block';
//         graphImage.src = erDiagramData;
//         graphImage.alt = "Entity Relationship Diagram";
        
//         // Add error handling for image loading
//         graphImage.onerror = function() {
//             console.error("Failed to load ER diagram");
//             graphImage.style.display = 'none';
//         };
//     } else {
//         console.error("relationship-graph element is not an img tag");
//     }
// }
