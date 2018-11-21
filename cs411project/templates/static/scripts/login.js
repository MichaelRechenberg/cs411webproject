function loginUser(){
    var MachineID = Number(document.getElementById("MachineId").value);
    var NetId = document.getElementById("NetId").value;

    var data = {};
		    data['NetId'] = NetId;
		    data['MachineID'] = MachineID;
            $.ajax({
                method: "POST",
                url: 'http://127.0.0.1:8080/login/user',
                dataType: 'json',
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(data, textStatus, xhr) {
                    if(xhr.status == 200){

                    }

                },
                complete: function(textStatus, xhr) {
                    if(xhr.status == 400){

                    }
                } 
            });
    }
function createUser(){
    var NetId = document.getElementById("createNetId").value;
    var name = document.getElementById("name").value;
    var data = {};
    data['AuthorNetID'] = NetId;
    data['Name'] = name;
    $.ajax({
        method: "POST",
        url: 'http://teamrocket.web.illinois.edu/project/users/new',
        dataType: 'json',
        data: JSON.stringify(data),
        contentType: "application/json"
    }).then(function(result) {
        $.ajax({
            method: "POST",
            url: 'http://teamrocket.web.illinois.edu/login',
            data: data,
        })
    });
}