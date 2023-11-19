function addToLocalStorage(key,data){
    localStorage.setItem(key) = data;
}

function retrieveFromLocalStorage(key){
    return localStorage.getItem(key)
}

function logout(){
    $.ajax({
        type: "POST",
        url: "/logout",
        success: function(data) {
            console.log(data)
            window.location.href = "login";
        }
    });
}

$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#myTable").on('click','.deleteButton',function(){
        // get the current row
        var currentRow=$(this).closest("tr"); 
            
        var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/deleteTask",
            data:{
                "task":col1
            },
            success: function(response){
                var url = "/dashboard"
                window.location.href = url;
            }
        })
        
    });
});

$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#myTable").on('click','.completeButton',function(){
        // get the current row
        var currentRow=$(this).closest("tr"); 
            
        var task=currentRow.find("td:eq(0)").text(); // get taskname value
        var actualhours = $("#actualhours").val();// get actual hours value
        $.ajax({
            type: "POST",
            url: "/completeTask",
            data:{
                "task":task,
                "actualhours":actualhours
            },
            success: function(response){
                resdata = JSON.parse(response)
                var url = "/dashboard"
                window.location.href = url;
            }
        })
        
    });
});
