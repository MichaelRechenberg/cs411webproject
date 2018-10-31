$(document).ready(function () {
    $.ajax({
        method: "GET",
        url: "http://teamrocket.web.illinois.edu/mike-dev/project/machine/availability",
        dataType: "json",
        crossDomain: true,
        success: function(result) {
            document.getElementById("commentId").innerHTML = result["commentId"];
            document.getElementById("Computer Chosen").innerHTML = "Update comment on PC#" + result["MachineID"];
            document.getElementById("MachineId").innerHTML = result["MachineId"];
            document.getElementById("NetId").innerHTML = result["NetId"];
            document.getElementById("HardwareId").innerHTML = result["HardwareId"];
            document.getElementById("comment").innerHTML = result["comment"];
                        
        },
        error: function(xhr, status, error) {
            console.log(xhr);
            //console.log(status);
            console.log(error);
          }
    });
    //document.getElementById("Computer Chosen").innerHTML = "BREAKPOINT #3";

});
function updateComment(){
    var formData = $('commentForm').serialize();
    $.ajax({
        method: "PUT",
        url: '/comment/update',
        dataType: 'json',
        data: formData
    });
}
function deleteComment(){
    var formData = $('commentForm').serialize();
    $.ajax({
        method: "PUT",
        url: '/comment/update',
        dataType: 'json',
        data: formData
    });
}