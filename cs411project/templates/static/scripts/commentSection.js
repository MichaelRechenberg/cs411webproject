$(document).ready(displayComments({}));

function displayComments(filters) {
    $("#commentList").html("");
    $.ajax({
        method: "POST",
        url: "http://teamrocket.web.illinois.edu/project/comment/query",
        data: JSON.stringify(filters),
        contentType: "application/json",
        dataType: "json",
        crossDomain: true,
        success: function (data) {
            var list_html = "<ol>";
            for( var i=0; i <data.length; i++) {
               list_html += "<li><div class='commentViewBox'>";
               list_html += "<p> Machine ID: " + data[i]['MachineID'] + "</p>";
               list_html += "<p> Hardware ID: " + data[i]['HardwareID'];
               list_html += "<p> Author: " + data[i]['AuthorNetID'] + "</p>";
               list_html += "<p> Category: " + data[i]['Category'] + "</p>";
               if(data[i]['IsResolved'] == '0'){
                   list_html+="<p> Status: <span style='color: red; font-weight: bold;'> Not Resolved </span> <p>";
               }
               if(data[i]['IsResolved'] == '1'){
                list_html+="<p> Status: <span style='color: green; font-weight: bold;'> Resolved </span> <p>";
            }
               list_html += "<div class='commentBox'> <p>" + data[i]['CommentText'] + "</p> </div>";
               if(data[i]['AuthorNetID'] == "hop2"){
          var editURL = "http://teamrocket.web.illinois.edu/comment/edit/" + data[i]['CommentID'];
                  list_html += ("<a class='btn btn-warning' href='" + editURL + "'> Update Comment <a>");
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
}
