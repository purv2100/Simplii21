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
        var col2=currentRow.find("td:eq(1)").text(); // get current row 2nd TD
        var col3=currentRow.find("td:eq(2)").text(); // get current row 3rd TD
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/deleteTask",
            data:{
                "task":col1,
                "status":col2,
                "category":col3
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
    $("#myTable").on('click','.editButton',function(){
        // get the current row
        var currentRow=$(this).closest("tr"); 
            
        var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        var col2=currentRow.find("td:eq(1)").text(); // get current row 2nd TD
        var col3=currentRow.find("td:eq(2)").text(); // get current row 3rd TD
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/editTask",
            data:{
                "task":col1,
                "status":col2,
                "category":col3
            },
            success: function(response){
                resdata = JSON.parse(response)
                var url = "/updateTask?taskname=" + resdata.taskname + "&category=" + currentRow.find("td:eq(2)").html() + "&startdate=" + resdata.startdate + "&duedate="+resdata.duedate+"&status="+resdata.status+"&hours="+resdata.hours+"&des="+resdata.description;
                window.location.href = url;
            }
        })
        
    });
});
