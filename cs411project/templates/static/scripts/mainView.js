 function choosePC(elementID){
                var PC = document.getElementById(elementID).textContent;
                        document.getElementById("Computer Chosen").innerHTML = "Comment on PC #"+PC;
                        document.getElementById("MachineId").value = PC;
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
                }
                if(avail == "AVAILABLE"){
                    document.getElementById(location).style.backgroundColor = "green";
                }
                if(avail == "IN-USE"){
                    document.getElementById(location).style.backgroundColor = "yellow";
                }

            }
        },
        error: function(xhr, status, error) {
            console.log(xhr);
            //console.log(status);
            console.log(error);
          }
    });
    //document.getElementById("Computer Chosen").innerHTML = "BREAKPOINT #3";

});

