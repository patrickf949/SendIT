function signUp(event){

    event.preventDefault()
    let username = document.getElementById("username").value;
    let email = String(document.getElementById("email").value);
    let contact = String(document.getElementById("contact").value);
    let password = String(document.getElementById("password").value);

    let userdetails = {
        "username":username,
        "email":email,
        "contact":contact,
        "password":password
    }

    fetch('http://i-sendit.herokuapp.com//api/v2/auth/signup',{
        method: 'POST',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"POST"
        },
        body:JSON.stringify(userdetails)
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        if(data.message === "hello! "+username+" Your Account has been created."
          +"Please login"){

            document.getElementById("api_reply").innerHTML = reply;
        }else{

            document.getElementById("api_reply").innerHTML = reply;
        }
    }).catch(error => {
        console.log(error);
    })


}

function loginUser(event){
    event.preventDefault()
    let username = document.getElementById("username").value;
    let password = String(document.getElementById("password").value);

    let userdetails = {
        "username":username,
        "password":password
    }

    fetch('http://i-sendit.herokuapp.com/api/v2/auth/login',{
        method: 'POST',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"POST"
        },
        body:JSON.stringify(userdetails)
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        if(data.message === "Hello "+username+" you are logged into SendIT as admin"){
            sessionStorage.setItem("s3nd21usertoken",(data).Access_token);
            document.getElementById("api_reply").innerHTML = reply;
            location.href = "admin_dashboard.html";
            closeTable();

        }else if(data.message === "Hello "+username+" you are logged into SendIT"){
            sessionStorage.setItem("s3nd21usertoken",(data).Access_token);
            document.getElementById("api_reply").innerHTML = reply;
            location.href = "dashboard.html"
            closeTable();

        }else{
            document.getElementById("api_reply").innerHTML = reply;
        }
        // document.getElementById("api_reply").innerHTML = reply;
    }).catch(error => {
        console.log(error);
    })


}
function closeTable(){
    document.getElementById("client_table").style.display='none'
}

function logout(event){
    event.preventDefault()

    fetch('http://i-sendit.herokuapp.com/api/v2/auth/logout',{
        method: 'POST',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"POST",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        },
        body:JSON.stringify(userdetails)
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.removeItem('s3nd21usertoken');
        location.href = "index.html"


    }).catch(error => {
        console.log(error);
    })


}

function addParcel(event){
    event.preventDefault()
    let parcel = document.getElementById("parcel").value;
    let recipient = String(document.getElementById("recipient").value);
    let contact = String(document.getElementById("contact").value);
    let pickuplocation = String(document.getElementById("pickuplocation").value);
    let destination = String(document.getElementById("destination").value);

    let parcel_description = {
        "parcel_description":parcel,
        "recipient":recipient,
        "contact":contact,
        "pickup_location":pickuplocation,
        "destination":destination
    };

    fetch('http://i-sendit.herokuapp.com/api/v2/parcels',{
        method: 'POST',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"POST",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        },
        body:JSON.stringify(parcel_description)
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        if(data.message.includes("Your Parcel Delivery order has been placed")===true){
            document.getElementById("api_reply").innerHTML = reply;
            location.href = "dashboard.html"

        }else{
            document.getElementById("api_reply").innerHTML = reply;
        }
        // document.getElementById("api_reply").innerHTML = reply;
    }).catch(error => {
        console.log(error);
    })

}

function updateParcel(event){
    event.preventDefault()
    let parcel = document.getElementById("parcel").value;
    let recipient = String(document.getElementById("recipient").value);
    let contact = String(document.getElementById("contact").value);
    let pickuplocation = String(document.getElementById("pickuplocation").value);
    let destination = String(document.getElementById("destination").value);

    let parcel_description = {
        "parcel_description":parcel,
        "recipient":recipient,
        "contact":contact,
        "pickup_location":pickuplocation,
        "destination":destination
    };

    fetch('http://i-sendit.herokuapp.com/api/v2/parcels',{
        method: 'PUT',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"POST",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        },
        body:JSON.stringify(parcel_description)
    })
    .then( response => response.json())
    .then(data => {
        reply = data.message;
        if(data.message.includes("Your Parcel Delivery order has been placed")===true){
            document.getElementById("api_reply").innerHTML = reply;


        }else{
            document.getElementById("api_reply").innerHTML = reply;
        }
        // document.getElementById("api_reply").innerHTML = reply;
    }).catch(error => {
        console.log(error);
    })

}

function viewParcelsUser(event){
    event.preventDefault()

    fetch('http://i-sendit.herokuapp.com/api/v2/parcels',{
        method: 'GET',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"GET",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        openTable(event);
        if(data.message.includes("all available")===true){
            document.getElementById("api_reply").innerHTML = reply+"shut up";
            let no = 0;
            let allparcels = '';
            data.parcels.forEach(parcel => {
                no++;
                allparcels += `
                <tr onclick="viewParcel(event,${parcel.parcel_id}}" class="${color}">
                    <td>${no}</td>
                    <td>${parcel.parcel_description}</td>
                    <td>${parcel.recipient}</td>
                    <td>${parcel.price}</td>
                    <td>${parcel.status}</td>
                </tr>
                `
            });


            document.querySelector("tbody").innerHTML = allparcels;

        }else{
            document.getElementById("api_reply").innerHTML = reply+" NOt";
        }

    }).catch(error => {
        console.log(error);
    })

}

function viewParcelsAdmin(event){
    event.preventDefault();

    fetch('http://i-sendit.herokuapp.com/api/v2/parcels',{
        method: 'GET',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"GET",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        if((data).message.includes("all available")===true){
            openTable();
            // document.getElementById("api_reply").innerHTML = reply+"NIvgsa";
            let no = 0;
            let allparcels = '';
            let color=''
            data.parcels.forEach(parcel => {
                if((no%2)==0){
                    color="light";
                }else{
                    color="dark";
                }
                no++;
                s= String(no)
                allparcels += `
                <tr class="${color}" onclick="viewParcelAdmin(event,${parcel.parcel_id})">
                    <td>${s}</td>
                    <td class="not1">${parcel.recipient}</td>
                    <td>${parcel.parcel_description}</td>
                    <td class="not">${parcel.pickup_location}</td>
                    <td>${parcel.destination}</td>
                    <td>${parcel.current_location}</td>
                    <td class="not">${parcel.price}</td>
                    <td class="not1">${parcel.weight_kgs}</td>
                    <td class="status">${parcel.status}</td>
                </tr>
                `

            });


            document.querySelector("tbody").innerHTML = allparcels;

        }else{
            document.getElementById("api_reply").innerHTML = reply+" Not";
        }

    }).catch(error => {
        console.log(error);
    })

}

function viewParcel(event,parcel_id){
    event.preventDefault();
    prepareParcelUpdate(parcel_id,"editParcelUser");
    document.getElementById("update").onclick = editParcelUser(event,parcel_id);
}

function openTable(){
    document.getElementById("client_table").style.display='inline'
}

function viewUsers(event){
    event.preventDefault()

}

function viewParcelAdmin(event,parcel_id){
    event.preventDefault();
    prepareParcelUpdate(parcel_id);
    document.getElementById("update").onclick = editParcelAdmin(event,parcel_id);
}



function prepareParcelUpdate(parcel_id){

    fetch('https://i-sendit.herokuapp.com/api/v2/parcels/'+parcel_id,{
        method: 'GET',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"GET",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.Parcel===null){
            document.getElementById("api_reply").innerHTML = reply;
        }
        else{
            openModal();
            let bodyDivs = document.getElementsByClassName("content");
            let arrayLength = bodyDivs.length;
            for (var i=0; i<arrayLength;i++){
                bodyDivs[i].style.display ='none';
            }
            data.Parcel.forEach(parcel => {
                document.getElementById("parcel").value = parcel.parcel_description;
                document.getElementById("recipient").value = parcel.recipient;
                document.getElementById("contact").value = parcel.recipient_contact;
                document.getElementById("pickup").value = parcel.pickup_location;
                document.getElementById("current").value = parcel.current_location;
                document.getElementById("weight").value = parcel.weight_kgs;
                document.getElementById("price").value = parcel.price;
                document.getElementById("statusOptions1").value = parcel.status;
                document.getElementById("destination").value = parcel.destination;

            });
        }

    }).catch(error => {
        console.log(error);
    })
}

let currentParcel = 0;

function editParcelAdmin(event, parcel_id){
    event.preventDefault();
    let weight = String(document.getElementById("weight").value);
    if(weight!==null){
        updateParcel(event,parcel_id,"weight",weight);
        updateParcel(event,parcel_id,"presentLocation",String(document.getElementById("current").value));
        updateParcel(event,parcel_id,"status",String(document.getElementById("statusOptions1").value));
    }else{
        document.getElementById("api_reply1").value = "You cannot edit present location or status of parcel before editing the weight";
    }
}

function editParcelUser(event, parcel_id){
    event.preventDefault();
    let destination = String(document.getElementById("destination").value);

    if(destination!=null && (document.getElementById("status"))==="pending"){
        updateParcel(event, parcel_id,"destination",destination)
    }else{
        document.getElementById("api_reply1").value = "You can only update a parcel thats still pending"
    }

}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

window.onclick = function(event) {
    if (event.target == document.getElementById("modal")) {
        document.getElementById("modal").style.display = "none";
    }
}
function openModal(){
    document.getElementById("modal").style.display = "inline";
}

function updateParcel(event, parcel_id, column, updatedvalue){
    event.preventDefault();
    let newvalue = '';

    if(column==="weight"){
        newvalue = updatedvalue
    }else{
        newvalue = String(updatedvalue)
    }
    console.log(newvalue)
    let updatedParcelDetail = updateDictionary(column, newvalue)

    fetch('https://i-sendit.herokuapp.com/api/v2/parcels/'+parcel_id+'/'+column,{
        method: 'PUT',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"PUT",
            "Authorization":"Bearer "+sessionStorage.getItem("s3nd21usertoken")
        },
        body:JSON.stringify(updatedParcelDetail)

    })
    .then(response => response.json())
    .then(data => {
        reply = data.Message;
        if(data.Message==="Update successful"){
            document.getElementById("api_reply1").innerHTML = reply;
        }
        else{
            document.getElementById("api_reply1").innerHTML = reply;

        }
    }).catch(error => {
        console.log(error);

    })

}

function backToTable(event){
    event.preventDefault()
    document.getElementById("modal").style.display = 'none';
    document.getElementsByClassName("content")[0].style.display ='block';
    closeTable();
}

function updateDictionary(column, value){
    console.log("Column: "+column);
    console.log("Value: "+value);
    if(column==="destination"){
        return {
            "destination":value
        }
    }else if(column==="status"){
        return {
            "status":value
        }
    }else if(column==="weight"){
        return {
            "weight":value
        }
    }else if(column==="presentLocation"){
        return {
            "current_location":value
        }
    }else{
        return {
            "message":"Please be epic"
        }
    }
}
