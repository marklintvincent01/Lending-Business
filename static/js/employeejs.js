const body = document.querySelector("body");

// Get the modal
var modal = document.getElementById("edit-profile-modal");

// Get the trigger button
var btn = document.getElementById("edit-profile-btn");

// Element that closes the modal
var cancel = document.getElementById("close-modal");

btn.onclick = function() {
    modal.style.display = "block";
    body.style.overflow = "hidden"
}

cancel.onclick = function() {
    modal.style.display = "none";
    body.style.overflowY = "auto"
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        body.style.overflowY = "auto"
    }
}