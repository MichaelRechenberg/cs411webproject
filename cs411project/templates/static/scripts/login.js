function loginUser(){
    var MachineID = Number(document.getElementById("MachineID").value);
    var NetId = document.getElementById("NetId").value;
    var data = {};
		    data['NetId'] = NetId;
		    data['MachineID'] = MachineID;
            $.ajax({
                method: "GET",
                url: 'http://teamrocket.web.illinois.edu/project/users/' + NetId,
                success: function(data, textStatus, xhr) {
                    if(xhr.status == 200){
                        console.log(xhr.status)
                        window.location.replace("http://teamrocket.web.illinois.edu/login/" + NetId);
                    }

                },
                complete: function(textStatus, xhr) {
                    if(xhr.status == 400){
                        console.log(xhr.status)
                        window.location.replace("http://teamrocket.web.illinois.edu/login/error");
                    }
                } 
            });
            window.location.replace("http://teamrocket.web.illinois.edu/login/error");

    }
function createUser(){
    var NetId = document.getElementById("createNetId").value;
    var FirstName = document.getElementById("FirstName").value;
    var LastName = document.getElementById("LastName").value;
    var isTA = Number($("input[name=isTA]:checked").val());
    var data = {};
    data['NetID'] = NetId;
    data['isTA'] = isTA;
    data['FirstName'] =FirstName;
    data['LastName'] = LastName;
    $.ajax({
        method: "POST",
        url: 'http://teamrocket.web.illinois.edu/project/users/new',
        dataType: 'json',
        data: JSON.stringify(data),
        contentType: "application/json"
    }).then(function(result) {
        window.location.replace("http://teamrocket.web.illinois.edu/login/" + NetId);
    });
}