 function choosePC(elementID){
                var PC = document.getElementById(elementID).textContent;
                        document.getElementById("Computer Chosen").innerHTML = "Comment on PC #"+PC;
                        document.getElementById("MachineId").value = PC;
}
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
            var list_html = "<ul style='list-style-type: none;'>";
            for( var i=0; i <5; i++) {
                list_html += "<li><div class='commentViewBox'>";
                list_html += "<div> <p class='commentInfo commentAuthor' >" + data[i]['AuthorNetID'] + "</p>";
                list_html += "<p class='commentInfo commentMachine' > Machine ID: " + data[i]['MachineID'] + "</p> </div>";
                list_html += "<div class='commentBox'> <p>" + data[i]['CommentText'] + "</p> </div>";
                list_html += "<p class='commentInfo commentMachine' > Category: " + data[i]['Category'] + "</p>";
                if(data[i]['IsResolved'] == '0'){
                    list_html+="<p style='font-weight: bold; color: red' class='commentInfo commentStatus'> Not Resolved <p>";
                }
                if(data[i]['IsResolved'] == '1'){
                    list_html+="<p style='font-weight: bold; color: green' class='commentInfo commentStatus'> Resolved <p>";
                }
               if(data[i]['AuthorNetID'] == "hop2"){
                    var editURL = "http://teamrocket.web.illinois.edu/comment/edit/" + data[i]['CommentID'];
                    list_html += ("<a class='btn btn-warning updateButton' href='" + editURL + "'> Update Comment <a>");
               }
               list_html += "</div></li>";
             }
            list_html += "</ul>"
            $("#commentList").html(list_html);
        },
        error: function(data) {
            console.log('There was a problem');
        }
     });
}


$(document).ready(function () {
    $.ajax({
        method: "GET",
        url: "http://teamrocket.web.illinois.edu/project/machine/availability",
        dataType: "json",
        crossDomain: true,
        success: function(result) {
            for(var mach =0; mach < result.length; mach++){
                var MachineID = result[mach]["MachineID"];
                var x = result[mach]["location"]["x"];
                var y = result[mach]["location"]["y"];
                var avail = result[mach]["MachineAvailability"];
                var location = "("+ x + "," + y + ")"
                document.getElementById(location).innerHTML = MachineID;
                if(avail == "BROKEN"){
                    document.getElementById(location).style.backgroundColor = "red";
                    document.getElementById(location).classList.add('column2');
                }
                if(avail == "AVAILABLE"){
                    document.getElementById(location).style.backgroundColor = "green";
                    document.getElementById(location).classList.add('column2');
                }
                if(avail == "IN-USE"){
                    document.getElementById(location).style.backgroundColor = "yellow";
                    document.getElementById(location).classList.add('column2');
                }

            }
        },
        error: function(xhr, status, error) {
            console.log(xhr);
            //console.log(status);
            console.log(error);
          }
    });
    displayComments({});
    //document.getElementById("Computer Chosen").innerHTML = "BREAKPOINT #3";

});
