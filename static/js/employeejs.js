const body = document.querySelector("body");

// Get the modal
var modal = document.getElementById("add-profile-modal");

// Get the trigger button
var btn = document.getElementById("add-profile-btn");

// Element that closes the modal
var cancel = document.getElementById("close-modal");

var form = document.getElementById("registerEmployee")
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

// holder = document.getElementById("amount");
// amount = holder.value
// holder.innerHTML = amount.toLocaleString(); 


$(function() {
    setTimeout(function() { $(".alert").fadeOut(1500); }, 5000)
})

$(function(){
    var dtToday = new Date();

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDay();
    var year = dtToday.getFullYear();

    if(month < 10)
        month = '0' + month.toString();
    if(day < 10)
        day = '0' + day.toString();
    
    var maxDate = year + '-' + month + '-' + day;
    $('#dateofbirth').attr('max', maxDate);
});


