// Email verification copied from :  https://stackoverflow.com/a/46181
function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function change_pref(data){
  data = JSON.parse(data);
  let new_preferences = {
    "initialized" : "yes",
    "name" : "",
    "email_id" : "",
    "email_notifications" : ""
  }


  let new_name = null;
  while(new_name == null || new_name == ""){
  new_name = prompt('Please enter your name (required)',String(data["name_block"]["name"]));
  }
  new_preferences["name"] = new_name;


  let new_email_id = null; 
  while(new_email_id == null || !validateEmail(new_email_id)){
    new_email_id = prompt('Please enter your e-mail (keep empty if you do not wish to share)',String(data["name_block"]["email_id"]));

    if(new_email_id == ""){
      break;
    }
  }
  new_preferences["email_id"] = new_email_id;


  if(new_preferences["email_id"] != ""){
    let new_email_notifications = prompt('Do you want critical e-mail notifications for your tasks? (yes/no) - NOT IMPLEMENTED YET',String(data["name_block"]["email_notifications"]));
    if(String(new_email_notifications).toLowerCase() == "yes"){
      new_preferences["email_notifications"] = "yes";
    }
    else{
      new_preferences["email_notifications"] = "no";
    }
  }else{
    new_preferences["email_notifications"] = "no";
  }

  let httpReq = new XMLHttpRequest();
  httpReq.open("POST", "/update_user_info", false);
  httpReq.send(JSON.stringify(new_preferences));

}


function force_initialization(data){
  data = JSON.parse(data);

  if(String(data["name_block"]["initialized"]) != "yes"){
    alert ("Welcome to Simpli! Please enter some information to get started!");
    change_pref(data);
  }

}

function reset_things(){
  
  let reset_tasks = prompt("Type 'yes' if you want to reset the task-list", "no");
  let reset_user_information = prompt("Type 'yes' if you want to delete all user_infromation", "no");


  if(reset_tasks == "yes"){
    let httpReq = new XMLHttpRequest();
    httpReq.open("POST", "/reset_tasks", false);
    httpReq.send();
  }
  if(reset_user_information == "yes"){
    let httpReq = new XMLHttpRequest();
    httpReq.open("POST", "/reset_all", false);
    httpReq.send();
  }

}