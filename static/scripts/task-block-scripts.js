/*
   Copyright 2023 Simplii from Group74 NCSU CSC510

   Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
*/


function showVal(newVal){
    document.getElementById("valBox").innerHTML=newVal;
}

function show1Val(newVal){
    document.getElementById("val1Box").innerHTML=newVal;
}

function show2Val(newVal){
    document.getElementById("val2Box").innerHTML=newVal;
}

// Code to set up current time on deadline datefield. 
window.addEventListener('load', () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('deadline').value = now.toISOString().slice(0, -8);
    });

$(document).ready(function(){
    $('input[type="radio"]').click(function(){
        var inputValue = $(this).attr("value");
        $("div.desc").hide();
        $("#" + inputValue + "Split").show();
    });
});

function submitTask(formData) {
    let httpReq = new XMLHttpRequest();
    httpReq.open("POST", "/submit_task_details", false);
    httpReq.open(JSON.stringify(formData))
}