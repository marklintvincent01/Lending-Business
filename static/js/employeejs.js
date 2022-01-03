const body = document.querySelector("body");

// Get the modal
var modal = document.getElementById("add-profile-modal");

// Get the trigger button
var btn = document.getElementById("add-profile-btn");

// Element that closes the modal
var cancel = document.getElementById("close-modal");

var pass = document.getElementById("password");
var conf_pass = document.getElementById("confirm_password");
var reg_btn = document.getElementById("submit");
var err_ms = document.getElementById("error-text");

btn.onclick = function() {
    modal.style.display = "block";
    body.style.overflow = "hidden";
}

cancel.onclick = function() {
    modal.style.display = "none";
    body.style.overflowY = "auto";
}

reg_btn.onclick = function() {
    if(pass.value == conf_pass.value) {
        return true;
    }
    else {
        err_ms.style.display = "block";
        pass.classList.add("is-invalid");
        conf_pass.classList.add("is-invalid");
        return false;
    }
}

$(function() {
    setTimeout(function() { $(".alert").fadeOut(1500); }, 5000)
})