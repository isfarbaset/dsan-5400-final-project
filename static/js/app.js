/**
 * Adds an event listener to the "fetchButton" button. On click, it retrieves a query from the input field,
 * sends it to the server via an API call, and processes the response to render entities, relationships,
 * and a graph visualization.
 */
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
                renderEntities(data.entities || []);
                renderRelationships(data.relationships || []);

                // Render Graph Visualization (if applicable)
                renderGraph(data.entities || [], data.relationships || []);
            } else {
                alert("No articles found!");
            }
        })
        .catch((error) => {
            console.error("Error fetching articles:", error);
            alert("An error occurred while fetching articles. Please try again.");
        });
});

/**
 * Renders a list of entities in the "entities" section of the UI.
 * @param {Array} entities - An array of entity objects with `text` and `label` properties.
 */
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

/**
 * Renders a list of relationships in the "relationships" section of the UI.
 * @param {Array} relationships - An array of relationship objects with `entity1`, `entity2`, and `relationship` properties.
 */
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

/**
 * Renders a graph visualization of entities and relationships using D3.js.
 * @param {Array} entities - An array of entity objects with `text` and `label` properties.
 * @param {Array} relationships - An array of relationship objects with `entity1`, `entity2`, and `relationship` properties.
 */
function renderGraph(entities, relationships) {
    const graphContainer = document.getElementById("graph-container");
    graphContainer.innerHTML = ""; // Clear previous content

    const width = 1200;
    const height = 600;

    // Prepare data for D3
    const nodes = entities.map(e => ({ id: e.text, group: e.label }));
    const links = relationships.map(r => ({
        source: r.entity1.text,
        target: r.entity2.text,
        value: 1
    }));

    // Create SVG
    const svg = d3.select("#graph-container").html("")
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
        .attr("r", 6.5)
        .attr("fill", d => d3.schemeCategory10[d.group.charCodeAt(0) % 10]);

    // Add titles to nodes
    node.append("title")
        .text(d => d.id);

    // Add a drag behavior.
    node.call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

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

    /**
     * Handles the drag start event.
     * @param {Object} event - The drag event object.
     */
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }

    /**
     * Handles the dragging event.
     * @param {Object} event - The drag event object.
     */
    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }

    /**
     * Handles the drag end event.
     * @param {Object} event - The drag event object.
     */
    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
}