
function updateComment(){
    var formData = $('commentForm').serialize();
    $.ajax({
        method: "PUT",
        url: '/comment/update',
        dataType: 'json',
        data: formData
    }).then(function () {
        window.location.replace("http://teamrocket.web.illinois.edu/mike-dev/project/comment");
    });
}
function deleteComment(){
    var formData = $('commentForm').serialize();
    $.ajax({
        method: "DELETE",
        url: '/comment/update',
        dataType: 'json',
        data: formData
    }).then(function () {
        window.location.replace("http://teamrocket.web.illinois.edu/mike-dev/project/comment");
    });
}