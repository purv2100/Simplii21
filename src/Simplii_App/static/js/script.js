/*
   Copyright 2023 Simplii from Group74 NCSU CSC510

   Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
*/


function addToLocalStorage(key, data) {
    localStorage.setItem(key) = data;
}

function retrieveFromLocalStorage(key) {
    return localStorage.getItem(key)
}

function sendRequest(e, clickedId) {
    console.log('sendRequest function called with clickedId:', clickedId);
    $.ajax({
        type: "POST",
        url: "/ajaxsendrequest",
        data: {
            "receiver": clickedId
        },
        success: function (response) {
            location.reload();
            console.log(JSON.parse(response));
        }
    })
}

function cancelRequest(e, clickedId) {
    $.ajax({
        type: "POST",
        url: "/ajaxcancelrequest",
        data: {
            "receiver": clickedId
        },
        success: function (response) {
            location.reload()
            console.log(JSON.parse(response))
        }
    })
}

function approveRequest(e, clickedId) {
    $.ajax({
        type: "POST",
        url: "/ajaxapproverequest",
        data: {
            "receiver": clickedId
        },
        success: function (response) {
            location.reload()
            console.log(JSON.parse(response))
        }
    })
}

function updateBadgeCount(sectionId, count) {
    document.getElementById(sectionId + 'Count').innerText = count;
}

function logout() {
    $.ajax({
        type: "POST",
        url: "/logout",
        success: function (data) {
            console.log(data)
            window.location.href = "login";
        }
    });
}

$(document).ready(function () {

    // code to read selected table row cell data (values).
    $("#myTable").on('click', '.deleteButton', function () {
        // get the current row
        var currentRow = $(this).closest("tr");

        var col1 = currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        var col2 = currentRow.find("td:eq(1)").text(); // get current row 2nd TD
        var col3 = currentRow.find("td:eq(2)").text(); // get current row 3rd TD
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/deleteTask",
            data: {
                "task": col1,
                "status": col2,
                "category": col3
            },
            success: function (response) {
                var url = "/dashboard"
                window.location.href = url;
            }
        })
    });
});

$(document).ready(function () {

    // code to read selected table row cell data (values).
    $("#myTable").on('click', '.completeButton', function () {
        // get the current row
        var currentRow = $(this).closest("tr");

        var task = currentRow.find("td:eq(0)").text(); // get taskname value
        var actualhours = $("#actualhours").val();// get actual hours value
        $.ajax({
            type: "POST",
            url: "/completeTask",
            data: {
                "task": task,
                "actualhours": actualhours
            },
            success: function (response) {
                resdata = JSON.parse(response)
                var url = "/dashboard"
                window.location.href = url;
            }
        })

    });
});

// sidebar collapse toggle
$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

});
