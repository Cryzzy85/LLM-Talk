document.addEventListener('DOMContentLoaded', function() {
    function filterPapers() {
        var researchField = document.getElementById('researchFieldSelect').value;
        var complexityState = document.getElementById('complexityStateSelect').value;
        var startingPoint = document.getElementById('startingPointSelect').value;
        var rows = document.getElementById('main-div').children;

        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            if ((researchField == "All" || row.getAttribute('data-research-field') == researchField) &&
                (complexityState == "All" || row.getAttribute('data-complexity-state') == complexityState) &&
                (startingPoint == "All" || row.getAttribute('data-starting-point') == startingPoint)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        }
    }

    document.getElementById('researchFieldSelect').addEventListener('change', filterPapers);
    document.getElementById('complexityStateSelect').addEventListener('change', filterPapers);
    document.getElementById('startingPointSelect').addEventListener('change', filterPapers);
});
