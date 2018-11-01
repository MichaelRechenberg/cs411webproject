$(document).ready(function () {
        $.ajax({
            method: "POST",
            url: "http://teamrocket.web.illinois.edu/mike-dev/comment/read",
            dataType: "json",
            crossDomain: true,
            success: function (data) {
                var list_html = "<ol>";
                for( var i=0; i <data.length; i++) {
                   list_html += "<li><div class='commentViewBox'>";
                   list_html += "<p> Machine ID: " + data[i]['MachineId'] + "</p>";
                   list_html += "<p> Harware ID: " + data[i]['HardwareId'];
                   list_html += "<p> Author: " + data[i]['netId'] + "</p>";
                   list_html += "<p> Category: " + data[i]['category'] + "</p>";
                   list_html += "<div class='commentBox'> <p>" + data[i]['comment'] + "</p> </div>";
                   if(data[i]['netId'] == "aburket2"){
                      list_html += "<a class='btn btn-warning' href='http://teamrocket.web.illinois.edu/mike-dev/comment/edit/'"
                      + data[i]['commentId'] + "> Update Comment <a>";
                   }
                   list_html += "</div></li>";
                 }
                list_html += "</ol>"
                $("#commentList").html(list_html);
            },
            error: function(data) {
                console.log('There was a problem');
            }
         });
         return false;    
     });
function sendComment(){
    var formData = $('commentForm').serialize();
    $.ajax({
        method: "POST",
        url: '/comment/create',
        dataType: 'json',
        data: formData
    });
}