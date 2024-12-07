document.getElementById("extractButton").addEventListener("click", function () {
    const text = document.getElementById("inputText").value;

    fetch("/api/extract", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // Display entities
        const entitiesList = document.getElementById("entities");
        entitiesList.innerHTML = "";
        data.entities.forEach(entity => {
            const li = document.createElement("li");
            li.textContent = `${entity.text} (${entity.label})`;
            entitiesList.appendChild(li);
        });

        // Display relationships
        const relationshipsList = document.getElementById("relationships");
        relationshipsList.innerHTML = "";
        data.relationships.forEach(relationship => {
            const li = document.createElement("li");
            li.textContent = `${relationship.entity1} ${relationship.relationship} ${relationship.entity2}`;
            relationshipsList.appendChild(li);
        });
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while processing your request.");
    });
});