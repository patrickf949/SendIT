function activatePlacesSearch(){
    let inputs = [document.getElementById("pickuplocation"),
                document.getElementById("destination"),
                document.getElementById("current"),
                document.getElementById("pickup")
                ];
    
    arrayLength = inputs.length
    
    for (var i=0;i<arrayLength;i++){
        input = inputs[i];
        let autocomplete = new google.maps.places.Autocomplete(input);
    }
    
}