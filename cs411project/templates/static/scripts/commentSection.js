$(document).ready(function () {
        $.ajax({
            method: "POST",
            url: "http://teamrocket.web.illinois.edu/mike-dev/project/comment/query",
            data: JSON.stringify({
                "AuthorNetID" : "hop2"
            }),
            contentType: "application/json",
            dataType: "json",
            crossDomain: true,
            success: function (data) {
                var list_html = "<ol>";
                for( var i=0; i <data.length; i++) {
                   list_html += "<li><div class='commentViewBox'>";
                   list_html += "<p> Machine ID: " + data[i]['MachineID'] + "</p>";
                   list_html += "<p> Harware ID: " + data[i]['HardwareID'];
                   list_html += "<p> Author: " + data[i]['AuthorNetID'] + "</p>";
                   list_html += "<p> Category: " + data[i]['Category'] + "</p>";
                   list_html += "<div class='commentBox'> <p>" + data[i]['CommentText'] + "</p> </div>";
                   if(data[i]['AuthorNetID'] == "hop2"){
                      list_html += "<a class='btn btn-warning' href='http://teamrocket.web.illinois.edu/mike-dev/comment/edit/'"
                      + data[i]['CommentId'] + "> Update Comment <a>";
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