# SendIT

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

## Badges

[![Build Status](https://travis-ci.org/patrickf949/SendIT.svg?branch=develop)](https://travis-ci.org/patrickf949/SendIT)
[![Maintainability](https://api.codeclimate.com/v1/badges/f0cc2da5a5ff305119d5/maintainability)](https://codeclimate.com/github/patrickf949/SendIT/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/patrickf949/SendIT/badge.svg?branch=develop)](https://coveralls.io/github/patrickf949/SendIT?branch=develop)

### REQUIREMENTS 

1. Install postgres
    CREATE A USER - senditdb WITH A PASSWORD - s3ndIt2m3

2. Python 3.6

### SET UP DATABASE

### SETTING UP APPLICATION

1.  Clone the repository

` $ git clone https://github.com/patrickf949/SendIT.git `

2.  Set up virutal environment

` $ virtualenv venv`

3.  Activate virtual environment

    FOR LINUX

` $ source venv/bin/activate `

    FOR WINDOWS

` $ .\venv\Scripts\activate `

4.  Inside the application folder, install all the requirements

` $ pip install -r requirements.txt`

5.  Run Application

` $ python run.py`

## Front End

[Github pages link](https://patrickf949.github.io/SendIT/Application/ui/)

### Technologies used

Html & Css - [w3schools](https://www.w3schools.com/)

## Backend

Our backend is a work-in-progress Application programming interface that emulates the functionality of the application.

### Features of application

*   Client can add a parcel delivery order providing details, such a
  * parcel description
  * recipient
  * recipient's contact
  * pickup location
  * destination
*   Client can cancel a delivery order
*   Admin can provide further details for a parcel delivery order such as,
  * weight, which automatically generates the price of parcel delivery order
  * status of parcel, whether pending, in transit, or delivered
*   Admin can view all parcel delivery orders of all clients
*   Admin can view a specific parcel delivery order

### Endpoints

| URL  | HTTP Method | Description|
|--------------|-------------|------------|
| `/api/v2/auth/signup` |`POST`| Sign up user |
| `/api/v2/auth/login` | `POST`| Login user |
| `/api/v2/parcels`    | `GET` | Fetch all parcel delivery orders-admin |
| `/api/v2/users` | `GET` | Fetch all users-admin |
| `/api/v2/parcels/<int:parcelId>` | `GET` |  Fetch a specific parcel delivery order-admin |
| `/api/v2/parcels`|`POST`| Create a parcel delivery order - client |
| `/api/v2/parcels/<int:parcel_id>/destination`|`PUT`| Update destination of parcel delivery order-client |
| `/api/v2/parcels/<int:parcel_id>/presentLocation`|`PUT`| Update present location of parcel delivery order-client/admin |
| `/api/v2/users/<int:user_id>/parcels`|`GET`| Get parcel delivery orders by user - admin|

#### SAMPLE DATA FOR THE BODY ENDPOINTS

    Use POSTMAN FOR CONSUMING THE API

    Feel free to change the variables to test validation

###### FOR SIGNUP

        {
            "username":"meltodsfdsdslo8989e",
            "email":"anoioisdioi@oorewgmdsail.com",
            "password":"andyfofofo2",
            "contact":"vtbuyiguoijpk,l"
        } 


###### FOR LOGIN 

*   As a user You can only login after signup

   
        {
            "username":"meltodsfdsdslo8989e",
            "password":"andyfofofo2"
        }
    
NB:

*   Copy the access token on user login 

*   TO CONSUME OTHER ENDPOINTS:

    *   In POSTMAN, go to the Authorisation tab
    *   Set the authorisation type to Bearer Token
    *   Paste the access token as the 'Token'

###### FOR CREATING PARCEL

        {
            "parcel_description":"Beerbongs",
            "recipient":"Mama Rhoda",
            "contact":"0773489238",
            "pickup_location":"Kawempe",
            "destination":"Kwagala, Kivumbo side"
        }
    

###### FOR EDITING A PARCEL DESTINATION - client

   
        {
            "destination":"Kwagala, Kivumbo side"
        }
   

##### FOR EDITING A PARCEL STATUS - admin only

    
        {
            "status":"pending"
        }
    

##### FOR EDITING A PARCEL PRESENT LOCATION - admin only

    
        {
            "current_location":"Kampala"
        }
    

##### FOR ADMIN LOGIN

    
        {
            "username":"Admin1",
            "password":"doNot2114"
        }
    
