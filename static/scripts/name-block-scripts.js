/*
   Copyright 2023 Simplii from Group74 NCSU CSC510

   Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
*/


// Email verification copied from : https://stackoverflow.com/a/46181
function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function showPrefModal() {
  // Get the modal
  var modal = document.getElementById("prefModal");

  // Get the button that opens the modal
  var btn = document.getElementById("prefBtn");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks on the button, open the modal
  btn.onclick = function() {
    modal.style.display = "block";
  }
  // $("#prefModal").modal('show');

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

function closeModal() {
  var modal = document.getElementById("prefModal");
  modal.style.display = "none";
}

function saveAndCloseModal() {
  var modal = document.getElementById("prefModal");
  modal.style.display = "none";
}

function submitUserInfo(formData) {
  let httpReq = new XMLHttpRequest();
  httpReq.open("POST", "/submit_user_details", false);
  httpReq.open(JSON.stringify(formData))
}


// function change_pref(data){
//   let new_preferences = {
//     "initialized" : "yes",
//     "name" : "",
//     "email_id" : "",
//     "email_notifications" : ""
//   }


//   let new_name = null;
//   while(new_name == null || new_name == ""){
//   new_name = prompt('Please enter your name (required)',String(data["name_block"]["name"]));
//   }
//   new_preferences["name"] = new_name;


//   let new_email_id = null; 
//   while(new_email_id == null || !validateEmail(new_email_id)){
//     new_email_id = prompt('Please enter your e-mail (keep empty if you do not wish to share)',String(data["name_block"]["email_id"]));

//     if(new_email_id == ""){
//       break;
//     }
//   }
//   new_preferences["email"] = new_email_id;


//   if(new_preferences["email"] != ""){
//     let new_email_notifications = prompt('Do you want critical e-mail notifications for your tasks? (yes/no) - NOT IMPLEMENTED YET',String(data["name_block"]["email_notifications"]));
//     if(String(new_email_notifications).toLowerCase() == "yes"){
//       new_preferences["emailChoose"] = "yes";
//     }
//     else{
//       new_preferences["emailChoose"] = "no";
//     }
//   }else{
//     new_preferences["emailChoose"] = "no";
//   }

//   let httpReq = new XMLHttpRequest();
//   httpReq.open("POST", "/update_user_info", false);
//   httpReq.send(JSON.stringify(new_preferences));

// }


function force_initialization(data){

  if(String(data["name_block"]["initialized"]) != "yes"){
    alert ("Welcome to Simpli! Please enter some information to get started!");
    change_pref(data);
  }

}
