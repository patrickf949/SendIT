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
    valid_parcel ={
            "client":"me",
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
    valid_admin_signup={
        "username":"Andrew",
        "email":"andrew@gmail.com",
        "password":"andyfofofo"
    }
    invalid_admin_signup={
        "email":"bumbelidaha",
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
    def add_parcel_delivery_order(self,parcel_to_add):
        """Adds parcel to list for testing purposes"""
        parcel_to_add['status']='pending'
        parcel_to_add['parcel_id']=len(Parcels.parcels)+1
        parcel_to_add['user_id']=len(Users.user_accounts)+1
        Users.user_accounts.append(dict(
            username = parcel_to_add['client'],
            user_id= parcel_to_add['user_id'],
            email ='random@gmail.com'
        ))
        print(parcel_to_add)
    
        Parcels.parcels.append(parcel_to_add)
        print(Parcels.parcels)
        
    

    def empty_all_lists(self):
        del Parcels.parcels[:]
        del Users.user_accounts[:]