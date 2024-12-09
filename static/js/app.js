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
    graphContainer.innerHTML = "Graph rendering not implemented."; // Placeholder for actual graph rendering logic
}

function renderERDiagram(erDiagramData) {
    const graphImage = document.getElementById('relationship-graph');
    if (!erDiagramData) {
        graphImage.style.display = 'none';
        return;
    }
    
    if (graphImage && graphImage.tagName === 'IMG') {
        graphImage.style.display = 'block';
        graphImage.src = erDiagramData;
        graphImage.alt = "Entity Relationship Diagram";
        
        // Add error handling for image loading
        graphImage.onerror = function() {
            console.error("Failed to load ER diagram");
            graphImage.style.display = 'none';
        };
    } else {
        console.error("relationship-graph element is not an img tag");
    }
}
