function signUp(){
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

    fetch('http://127.0.0.1:5000/api/v2/auth/signup',{
        method: 'POST',
        headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body:JSON.stringify(userdetails)
    })
    .then(response => response.json())
    .then(data => {
        if(data.message === "hello! "+username+" Your Account has been created. Please login"){
            
            document.getElementById("api_reply").innerHTML = reply;
        }else{
            reply = data.message;
            document.getElementById("api_reply").innerHTML = reply;
        }
    }).catch(error => {
        console.log(error);
    })

    
}

function loginUser(){
    let username = document.getElementById("username").value;
    let password = String(document.getElementById("password").value);

    let userdetails = {
        "username":username,
        "password":password
    }

    fetch('http://127.0.0.1:5000/api/v2/auth/login',{
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
        if(data.message === "hello! "+username+" You Account has been created. Please login"){

            document.getElementById("api_reply").innerHTML = reply;
        }else{
            reply = data.message;
            document.getElementById("api_reply").innerHTML = reply;
        }
        // document.getElementById("api_reply").innerHTML = reply;
    }).catch(error => {
        console.log(error);
    })

    
}

function logout(){

}

function addParcel(){

}

function updateParcel(){

}

function viewParcels(){

}

function viewParcel(){

}