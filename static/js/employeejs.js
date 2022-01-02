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


// $('#registerEmployee').get(0).reset()

// $('registerEmployee')[0].reset();

// window.onclick = function(event) {
//     if(event.target == modal) {
//         modal.style.display = "none";
//         body.style.overflowY = "auto"
//     }
// }

// reg_btn.onclick = function() {
//     if(pass == conf_pass) {
//         return false;
//     }
//     else {
//         return true;
//     }
// }

// (function() {
//     "use strict";
 
//     window.addEventListener("load", function() {
//       document.getElementById("registerEmployee").addEventListener("submit", function(event) {
//         event.target.checkValidity();
//         event.preventDefault(); // Prevent form submission and contact with server
//         event.stopPropagation();
//       }, false);
//     }, false);
//   }());

// function manualValidate(ev) {
//     ev.target.checkValidity();
//     if(pass.value == conf_pass.value) {
//         return true;
//     }
//     else {
//         return false;
//     }
// }
// $("#registerEmployee").bind("submit", manualValidate);

// function myValidation() {
//     if(pass == conf_pass) {
//         alert("Validations successful!");
//         return false;
//     }
//     else {
//         alert("Validations failed!");
//         return true;
//    }
   
// }

// $('#submit').click(function (event) {
//     $.post(url, data = $('#registerEmployee').serialize(), function (
//         data) {
//         if (data.status == 'ok') {
//             $('#add-profile-modal').modal('hide');
//         } else {
//             Event.preventDefault();
//         }
//     })
// });

$(function() {
    setTimeout(function() { $(".alert").fadeOut(1500); }, 5000)
})