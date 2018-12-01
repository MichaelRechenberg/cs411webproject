function choosePC(machineID){
                        document.getElementById("Computer Chosen").innerHTML = "Comment on PC #"+machineID;
                        document.getElementById("MachineId").value = machineID;
}

function sendHeartbeat(netId, machineId) { 
  var url = "http://teamrocket.web.illinois.edu/project/hb/" + netId + "/" + machineId;
  console.log("Attempting to send heartbeat for net Id " + netId + " and machine Id " + machineId);
  $.ajax({
   type: "POST",
   url: url,
   data: "",
   success: function() {
     console.log("Successfully sent heartbeat");
   }
  });
}

function sendHeartbeatsContinually(netId, machineId){
  setInterval(function() {sendHeartbeat(netId, machineId);}, 10*1000);
}

function displayComments(filters, netId) {
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
            if(data[i]['AuthorNetID'] == netId){
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

function getCategories() {
    $("#categoryChecks").html("");
    $.ajax({
        method: "GET",
        url: "http://teamrocket.web.illinois.edu/project/downage-category/simple",
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
