
function updateComment(){
    var commentID = Number(document.getElementById("commentId").val());
    var MachineID = Number(document.getElementById("MachineId").val());
    var HardwareID = Number(document.getElementById("HardwareId").val());
    var NetId = document.getElementById("NetId").val();
    var comment = document.getElementById("comment").val();
    $.ajax({
        method: "PUT",
        url: '/comment/update',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify({
          "AuthorNetID": NetId,
          "Comment": comment,
          "MachineID": MachineID,
          "HardwareID": HardwareID,
          "CommentText": comment,
          "CommentID": commentID
        })
    }).then(function () {
        window.location.replace("http://teamrocket.web.illinois.edu/project/comment");
    });
}
function deleteComment(){
    var commentID = Number(document.getElementById("commentId").val());
    $.ajax({
        method: "DELETE",
        url: 'http://teamrocket.web.illinois.edu/comment/delete/' + commentID,
    }).then(function () {
        window.location.replace("http://teamrocket.web.illinois.edu/project/comment");
    });
}
