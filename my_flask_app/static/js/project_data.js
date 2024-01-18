window.onload = function() {
    // Get the modal
    var headerModal = document.getElementById("headerModal");

    // Get the <span> element that closes the modal
    var headerClose = document.getElementsByClassName("close")[0];

    // Open Header Modal
    function openHeaderModal() {
        console.log("Opening modal");
        headerModal.style.display = "block";
    }

    // Close Header Modal
    function closeHeaderModal() {
        console.log("Closing modal");
        headerModal.style.display = "none";
    }

    // When the user clicks the "x", close the modal
    if (headerClose) {
        headerClose.onclick = function() {
            headerModal.style.display = "none";
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == headerModal) {
            headerModal.style.display = "none";
        }
    }
}
