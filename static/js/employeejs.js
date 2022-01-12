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

// reg_btn.addEventListener("click", function (e) {
//     e.preventDefault();
// });
// $(document).ready(function () {
//     $('#submit').click(function (event) {
//         $.post(url, data = $('#registerEmployee').serialize(), function (
//             data) {
//             if (!(data.status == 'ok')) {
//                 event.preventDefault();
//                 var obj = JSON.parse(data);
//                 for (var key in obj) {
//                     if (obj.hasOwnProperty(key)) {
//                         var value = obj[key];
//                     }
//                 }
//                 $('.help-block').remove()
//                 $('<p class="help-block">' + value + '</p>')
//                     .insertAfter('#' + key);
//             }
//         })
//     });
// })

//sulayanan pa ni
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

// $(function(event) {
//     var x = "alert-danger";
//     var y = $("#alert-mess").hasClass(x);
//     if (y) {
//         event.preventDefault();
//         event.stopImmediatePropagation();
        
//     }
//     else {
//         return true;
//     }
// });

// function updateTextView(_obj){
//     var num = getNumber(_obj.val());
//     if(num==0){
//         _obj.val('');
//     }else{
//         _obj.val(num.toLocaleString());
//     }
// }
// function getNumber(_str){
//     var arr = _str.split('');
//     var out = new Array();
//     for(var cnt=0;cnt<arr.length;cnt++){
//         if(isNaN(arr[cnt])==false){
//         out.push(arr[cnt]);
//         }
//     }
//     return Number(out.join(''));
// }
// $(document).ready(function(){
//     $('#amount').on('keyup',function(){
//         updateTextView($(this));
//     });
// });

$(function() {
    setTimeout(function() { $(".alert").fadeOut(1500); }, 5000)
})

