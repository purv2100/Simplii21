
function showVal(newVal){
document.getElementById("valBox").innerHTML=newVal;
}

// Code to set up current time on deadline datefield. 
window.addEventListener('load', () => {
const now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
document.getElementById('deadline').value = now.toISOString().slice(0, -8);
});

function submitTask(formData) {
    let httpReq = new XMLHttpRequest();
    httpReq.open("POST", "/submit_task_details", false);
    httpReq.open(JSON.stringify(formData))
}