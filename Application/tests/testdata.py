"""Contains all data to be tested"""
from ..models.parcels import Parcels
from ..models.users import Users

class TestData():  
    empty={}
    valid_parcel ={
            "client":"Wademu",
            "parcel_description":"Yanga",
            "recipient":"Carol",
            "contact":"0756372818",
            "pickup_location":"Kawempe, industrial area",
            "destination":"Jinja town council"
        }
    valid_parcel1 ={
            "client":"Kwage",
            "parcel_description":"Yanga",
            "recipient":"Casrol",
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
    valid_admin_signup={
        "username":"Andrew",
        "email":"andrew@gmail.com",
        "contact":"0758688174",
        "password":"andyfofofo"
    }
    invalid_admin_signup={
        "username":"bumbelidaha",
        "books":"na"

    }
    valid_admin_login={
        "email":"andrew@gmail.com",
        "password":"andyfofofo"
    }
    invalid_admin_login={
        "email":"andrew@gmaidsdsl.com",
        "password":"andyfofofo"
    }
    valid_user_signup={
        "username":"Kwage",
        "email":"andrdddew@gmail.com",
        "contact":"0824323423",
        "password":"andyfofofo"
    }
    valid_user_login={
        "email":"andrdddew@gmail.com",
        "password":"andyfofofo"
    }
    invalid_user_login={
        "email":"kwage@gmail.com",
        "password":"andyfofofo"
    }
    