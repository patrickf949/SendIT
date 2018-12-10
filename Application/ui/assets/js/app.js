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
        if(data.message === "hello! "+username+" Your Account has been created. Please login"){
            
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
            localStorage.setItem("usertoken",(data).Access_token);
            Console.log(localStorage.getItem("usertoken"));
            document.getElementById("api_reply").innerHTML = reply;
            location.href = "admin_dashboard.html";
            
        }else if(data.message === "Hello "+username+" you are logged into SendIT"){
            localStorage.setItem("usertoken",(data).Access_token);
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

function logout(event){
    event.preventDefault()
    
    fetch('http://i-sendit.herokuapp.com/api/v2/auth/logout',{
        method: 'POST',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"POST",
            "Authorization":"Bearer "+localStorage.getItem("usertoken")
        },
        body:JSON.stringify(userdetails)
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("usertoken","");
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
            "Authorization":"Bearer "+localStorage.getItem("usertoken")
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
            "Authorization":"Bearer "+localStorage.getItem("usertoken")
        },
        body:JSON.stringify(parcel_description)
    })
    .then(response => response.json())
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
            "Authorization":"Bearer "+localStorage.getItem("usertoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        if(data.message.includes("all available")===true){
            document.getElementById("api_reply").innerHTML = reply;
            let no = 0;
            let allparcels = '';
            data.parcels.forEach(parcel => {
                no++;
                allparcels += `
                <tr onclick="viewParcel(event,parcelId)" class="${color}">			
                            <td>${no}</td>
                            <td>${parcel.parcel_description}</td>
                            <td>${parcel.recipient}</td>
                            <td>${parcel.price}</td>
                            <td>${parcel.status}</td>		
                            <td><button onclick="viewParcel(event,${parcel.parcel_id}})">Edit/view</button></td>
                </tr>
                `
            });
            
            
            document.getElementById("tbody").innerHTML = allparcels;
       
        }else{
            document.getElementById("api_reply").innerHTML = reply;
        }
        
    }).catch(error => {
        console.log(error);
    })  
    
}

function viewParcelsAdmin(event){
    event.preventDefault()
    
    fetch('http://i-sendit.herokuapp.com/api/v2/parcels',{
        method: 'GET',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods":"GET",
            "Authorization":"Bearer "+localStorage.getItem("usertoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        reply = data.message;
        if(data.message.includes("all available")===true){
            document.getElementById("api_reply").innerHTML = reply;
            let no = 0;
            let allparcels = '';
            data.parcels.forEach(parcel => {
                no++;
                allparcels += `
                <tr onclick="viewParcel(event,parcelId)" class="${color}">			                      
                            
                        <td>${no}</td>
						<td class="not">${parcel.recipient}</td>
						<td>${parcel.parcel_description}</td>
						<td class="not">${parcel.pickup_location}</td>
						<td>${parcel.destination}</td>
						<td>${parcel.current_location}</td>
						<td class="not">${parcel.price}</td><td class="not">2</td>		
                        <td class="status">${parcel.status}</td>
                        
                        <td><button onclick="viewParcel(event,${parcel.parcel_id}})">Edit/view</button></td>
					</tr>
					
				</tbody>
                </tr>
                `
            });
            
            
            document.getElementById("tbody").innerHTML = allparcels;
       
        }else{
            document.getElementById("api_reply").innerHTML = reply;
        }
        
    }).catch(error => {
        console.log(error);
    })  
    
}

function viewParcel(event,parcel_id){
    event.preventDefault();


}

function openTable(event){
    document.getElementsByClassName("client_table").style.display='block'
}

function viewUsers(event){

}