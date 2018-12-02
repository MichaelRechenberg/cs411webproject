
function updateComment(){
    // TODO: need to have isResolved go here, category
    var commentID = Number(document.getElementById("commentId").value);
    // TODO: Why would we want to change MachineID and HardwareID of a comment?
    // var MachineID = Number(document.getElementById("MachineId").value);
    // var HardwareID = document.getElementById("HardwareId").value;
    var NetId = document.getElementById("NetId").value;
    var comment = document.getElementById("comment").value; 
    var category = $("input[name=Category]:checked").val();

    var isResolved = 0; 
    if(document.getElementById("isResolved").checked){
        isResolved = 1;
    }


    $.ajax({
        method: "PUT",
        url: 'http://teamrocket.web.illinois.edu/project/comment/update/' + commentID,
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify({
          "AuthorNetID": NetId,
          "CommentText": comment,
          "Category": category,
          "IsResolved": isResolved
        })
    }).then(function () {
	// Redirect to the main view comments page after editing comment
        window.location.replace("http://teamrocket.web.illinois.edu/comment");
    });
}
function deleteComment(){
    var commentID = Number(document.getElementById("commentId").value);
    $.ajax({
        method: "DELETE",
        url: 'http://teamrocket.web.illinois.edu/project/comment/delete/' + commentID,
    }).then(function () {
	// Redirect to the main view comments page after deleting comment
        window.location.replace("http://teamrocket.web.illinois.edu/comment");
    });
}

function getCategories(commentID) {
    $("#categoryChecks").html("");
    $.ajax({
        method: "GET",
        url: "http://teamrocket.web.illinois.edu/project/downage-category/editing-comment/" + commentID,
        contentType: "application/json",
        dataType: "json",
        crossDomain: true,
        success: function (data) {
            var list_html = "";
            for( var i=0; i <data.length; i++) {
                list_html += "<option value=" + data[i]["CategoryText"] + ">" + data[i]["CategoryText"] + "</option>"
            }
            $("#categoryChecks").html(list_html);
        },
        error: function(data) {
            console.log('There was a problem');
        }
     });
}

