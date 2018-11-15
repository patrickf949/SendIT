"""
This module handles all parcels in our application
"""

class Parcels:
    """
    This class handles all parcel delivery order manipulation
    """
    parcels=[]
    def __init__(self, parcel_description, recipient, 
                contact, pickup_location,destination):
        self.parcel_description = parcel_description
        self.recipient = recipient
        self.contact = contact
        self.pickup_location = pickup_location
        self.destination = destination
    
    def create_parcel(self):
        """
        creates a parcel delivery order
        params:n/a
        return: n/a
        """
        parcels.append
    
    @staticmethod
    def cancel_parcel():
        """
        Cancels a parcel delivery order
        params: n/a
        returns: parcel created
        """
        pass

    @staticmethod
    def time_details():
        """
        Adds current time, parcel pick up time, parcel delivery time
        params: n/a
        returns:current time, parcel pick up time, parcel delivery time
        """
        pass

    @staticmethod
    def client_update_parcel():
        """
        Client Updates a parcel based on its id
        params: parcelid
        returns: updated parcel
        """
        pass
    
    @staticmethod
    def admin_update_parcel():
        """
        Admin Updates a parcel status, weight, price
        params: parce
        returns: Updated parcel
        """
        pass

    @staticmethod
    def parcels_by_user():
        """
        Gets all parcels by a specific user
        params: user id
        returns:all parcels by a specific user
        """
        pass
    
