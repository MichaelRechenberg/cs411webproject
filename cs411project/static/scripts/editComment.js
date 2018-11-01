
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
        method: "DELETE",
        url: '/comment/update',
        dataType: 'json',
        data: formData
    });
}