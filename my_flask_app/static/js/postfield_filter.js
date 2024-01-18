// Event listener for when a checkbox is changed.
document.querySelectorAll("input[type=checkbox]").forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        console.log('Checkbox change detected.');  // Debugging line
        filterPapers();
    });
});

function filterPapers() {
    // Get all selected research fields.
    var selectedFields = [];
    document.querySelectorAll("input[type=checkbox]:checked").forEach(function(checkbox) {
        selectedFields.push(checkbox.value);
    });

    console.log('Selected fields:', selectedFields);  // Debugging line

    // If no fields are selected, show all papers.
    if (selectedFields.length === 0) {
        document.querySelectorAll(".row").forEach(function(row) {
            row.style.display = "";
        });
        return;
    }

    // Hide or show each paper based on the selected research fields.
    document.querySelectorAll(".row").forEach(function(row) {
        var researchField = row.getAttribute("data-research-field");
        if (selectedFields.includes(researchField)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}


