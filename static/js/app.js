document.getElementById("fetchButton").addEventListener("click", function () {
    const query = document.getElementById("queryInput").value;

    fetch(`/api/fetch?query=${query}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.results.length > 0) {
                const firstResult = data.results[0];

                // Debugging: Log data structure
                console.log("Entities:", firstResult.entities);
                console.log("Relationships:", firstResult.relationships);

                // Render Entities and Relationships
                renderEntities(firstResult.entities);
                renderRelationships(firstResult.relationships);

                // Render Graph Visualization (if applicable)
                renderGraph(firstResult.entities, firstResult.relationships);
            } else {
                alert("No articles found!");
            }
        })
        .catch((error) => {
            console.error("Error fetching articles:", error);
        });
});

function renderEntities(entities) {
    const entitiesList = document.getElementById("entities");
    entitiesList.innerHTML = ""; // Clear previous results

    entities.forEach((entity) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${entity.label}: ${entity.text}`; // Format entity details
        entitiesList.appendChild(listItem);
    });
}

function renderRelationships(relationships) {
    const relationshipsList = document.getElementById("relationships");
    relationshipsList.innerHTML = ""; // Clear previous results

    relationships.forEach((relationship) => {
        const entity1Text = relationship.entity1?.text || "Unknown";
        const entity2Text = relationship.entity2?.text || "Unknown";
        const relationType = relationship.relationship || "related-to";

        const listItem = document.createElement("li");
        listItem.textContent = `${entity1Text} ${relationType} ${entity2Text}`;
        relationshipsList.appendChild(listItem);
    });
}

function renderGraph(entities, relationships) {
    console.log("Rendering graph with:", { entities, relationships });
    const graphContainer = document.getElementById("relationship-graph");
    graphContainer.innerHTML = "Graph rendering not implemented.";
}