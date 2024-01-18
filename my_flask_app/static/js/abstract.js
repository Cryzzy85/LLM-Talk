function showAbstract(button) {
    // Get the modal
    var modal = document.getElementById("abstractModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // Get the abstract text from the button's data-attribute
    var abstract = button.getAttribute("data-abstract");

    // Fill the modal with the abstract
    document.getElementById("abstractText").innerText = abstract;

    // Show the modal
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
