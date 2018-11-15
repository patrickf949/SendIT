"""Contains all data to be tested"""

class TestData():  
    valid_parcel ={
            "client":"Wademu",
            "parcel_description":"Yanga",
            "recipient":"Carol",
            "contact":"0756372818",
            "pickup_location":"Kawempe, industrial area",
            "destination":"Jinja town council"
        }
    
    invalid_recipient_parcel ={
            "client":"Wademu",
            "parcel_description":"Yanga",
            "recipient":3,
            "contact":"0756372818",
            "pickup_location":"Kawempe, industrial area",
            "destination":"Jinja town council"
        }

    invalid_parcel_less_params = {
            "client":"Wademu",
            "parcel_description":"Yanga",
            "contact":"0756372818",
            "pickup_location":"Kawempe, industrial area",
            "destination":"Jinja town council"
        }
    
    invalid_parcel_shortcontact={
        "client":"Wademu",
        "parcel_description":"Yanga",
        "recipient":"Jessica",
        "contact":"02abc38",
        "pickup_location":"Kwagala Restaurant, Kito",
        "destination":"Aweber Clicks international"

    }