
(function checkSession(){
    if (sessionStorage.getItem("s3nd21usertoken")!==null){
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
        }).catch(error => {
            console.log(error)
        })
    }
    
})();