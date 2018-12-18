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
    if ((/[\w-]+@([\w-]+\.)+[\w-]+/.test(email))===true){
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
    else{
        document.getElementById("api_reply").innerHTML = "Please enter a valid email address";
    }
    
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
            setUpUserDashboards(username,(data).Access_token,"admin_dashboard.html")

        }else if(data.message === "Hello "+username+" you are logged into SendIT"){
            setUpUserDashboards(username,(data).Access_token,"dashboard.html")
        }else{
            document.getElementById("api_reply").innerHTML = reply;
        }
        // document.getElementById("api_reply").innerHTML = reply;
    }).catch(error => {
        console.log(error);
    })


}
function setUpUserDashboards(username,token,dashboard){
    sessionStorage.setItem("s3nd21usertoken",token);
    sessionStorage.setItem("s3nd21username",username)
    document.getElementById("api_reply").innerHTML = reply;
    location.href = dashboard;
    closeTable();
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
        sessionStorage.removeItem('s3nd21username');
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

    viewParcels("viewParcelUser")
}

function viewParcelsAdmin(event){
    event.preventDefault();
    viewParcels("viewParcelAdmin")
    
}

function viewParcels(action){
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
                <tr class="${color}" onclick="${action}(event,${parcel.parcel_id})">
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
            document.getElementById("api_reply").innerHTML = reply;
        }

    }).catch(error => {
        console.log(error);
    })

}

function viewParcelUser(event,parcel_id){
    event.preventDefault();
    prepareParcelUpdate(parcel_id,"editParcelUser");
    
    document.getElementById("btns").innerHTML = `
                    <button type="submit" onclick="editParcelUser(event,${parcel_id})">Edit Order</button>
					<button type="button" onclick="backToTable(event)">Back</button>
					<button type="reset" id="resetbtn">r</button>
    `;
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
    document.getElementById("btns").innerHTML = `
                    <button type="submit" onclick="editParcelAdmin(event,${parcel_id})">Edit Order</button>
					<button type="button" onclick="backToTable(event)">Back</button>
					<button type="reset" id="resetbtn">r</button>
    `;
    
}



function prepareParcelUpdate(parcel_id){
    document.getElementById("api_reply1").value = null;
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
        let location1 = document.getElementById("current").value;
        let location2 = document.getElementById("pickup").value;
        if (location1===location2){
            updateParcel(event,parcel_id,"weight",weight);    
        }
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

    if(destination!==null && (document.getElementById("statusOptions1").value)==="pending"){
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
        newvalue = parseFloat(updatedvalue)
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
        reply = data.message;
        if(data.message==="Update successful" || data.message.includes("Updated")){
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
