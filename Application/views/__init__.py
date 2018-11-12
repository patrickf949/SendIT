from flask import jsonify,Flask,request

app = Flask(__name__)

parcels =[
    {
        'parcelId':1,
        'parcelDescription':'Pumped Up Kicks & pinnata',
        'client': 'B cky',
        'recipient':'Mart',
        'pickUpLocation':'Quality Shopping Village',
        'destination':'Andela Uganda,Kira Road',
        'currentLocation':'Tuskys, Ntinda',
        'status':'Pending'
    }
]

@app.route('/')
def kingsLanding():

    return 'Welcome to SendIT'

@app.route('/api/v1/parcels')
def getParcels():
   return jsonify({
       'parcels':parcels
   })

@app.route('/api/v1/parcel/<int:parcelId>')
def getParcel(parcelId):
    if len(parcels)==0:
        return jsonify({
            'message':'No Parcel delivery orders yet'
        }),205
    if not parcelId or parcelId < 1 or type(parcelId)!=int:
        return jsonify({
            'message': 'sorry! book ID is required and can not be less than 1'
        }), 400
    for parcel in parcels:
        if parcel['parcelId'] == parcelId:
            return jsonify({
                'Specified parcel':parcel
            }), 200
    return jsonify({
        'message':'the book was not found'
    }), 205

@app.route ('/api/v1/addParcel', methods = ['POST'])
def addParcel():
    data = request.get_json()
    
    parcelId=len(parcels)+1
    parcelDescription = data.get('parcelDescription')
    client = data.get('client')
    recipient = data.get('recipient')
    pickUpLocation = data.get('pickUpLocation')
    destination =data.get('destination')
    status='pending'
    if not parcelDescription or parcelDescription.isspace():
        return jsonify({
            'message':'sorry! the parcelDescription is required and can not be an empty string'
        }), 400

    if not client or client.isspace():
        return jsonify({
            'message':'sorry! the client is required and can not be an empty string'
        }), 400

    if not recipient or recipient.isspace():
        return jsonify({
            'message':'sorry! the recipient is required and can not be an empty string'
        }), 400

    if not pickUpLocation or pickUpLocation.isspace():
        return jsonify({
            'message':'sorry! the pickUpLocation is required and can not be an empty string'
        }), 400

    

    parcel =dict(
        parcelId=parcelId,
        parcelDescription = parcelDescription,
        client = client,
        recipient = recipient,
        pickUpLocation = pickUpLocation,
        destination =destination,
        status = status
    )
    
    parcels.append(parcel)

    return jsonify({
        'message': 'Parcel Delivery order has been placed',
        'Parcel':parcels[-1]
    }),200

@app.route('/api/v1/updateParcel/<int:parcelId>', methods = ['PUT'])
def updateParcel(parcelId):
    data = request.get_json()
    
    parcelDescription = data.get('parcelDescription')
    client = data.get('client')
    recipient = data.get('recipient')
    pickUpLocation = data.get('pickUpLocation')
    destination =data.get('destination')
    status = 'pending'
    

    if not parcelDescription or parcelDescription.isspace():
        return jsonify({
            'message':'sorry! the parcelDescription is required and can not be an empty string'
        }), 400

    if not client or client.isspace():
        return jsonify({
            'message':'sorry! the client is required and can not be an empty string'
        }), 400

    if not recipient or recipient.isspace():
        return jsonify({
            'message':'sorry! the recipient is required and can not be an empty string'
        }), 400

    if not pickUpLocation or pickUpLocation.isspace():
        return jsonify({
            'message':'sorry! the pickUpLocation is required and can not be an empty string'
        }), 400

    
    i=0
    for existing_parcel in parcels:
        i+=1
        if existing_parcel['parcelId']==parcelId:
            status =parcels[i]['status']
            parcel =dict(
                parcelDescription = parcelDescription,
                client = client,
                recipient = recipient,
                pickUpLocation = pickUpLocation,
                destination =destination,
                status=status
            )
            del parcels[i]
            parcels[i]=parcel
            return jsonify({
                'Message': 'Parcel has been Updated',
                'parcel': parcel
            }),200

        
    return jsonify({
        'Message':'Parcel order does not exist'
    }),405

# def validation(parcelDescription,client, recipient, pickUpLocation,Destination):
#     if not parcelDescription or parcelDescription.isspace():
#         return jsonify({
#             'message':'sorry! the parcelDescription is required and can not be an empty string'
#         }), 400

#     if not client or client.isspace():
#         return jsonify({
#             'message':'sorry! the client is required and can not be an empty string'
#         }), 400

#     if not recipient or recipient.isspace():
#         return jsonify({
#             'message':'sorry! the recipient is required and can not be an empty string'
#         }), 400

#     if not pickUpLocation or pickUpLocation.isspace():
#         return jsonify({
#             'message':'sorry! the pickUpLocation is required and can not be an empty string'
#         }), 400

    