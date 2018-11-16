"""
This module handles all parcels in our application
"""

class Parcels():
    """
    This class handles all parcel delivery order manipulation
    """
    parcels=[]
    def __init__(self, parcel):
        self.parcel=parcel
    
    def create_parcel(self):
        """
        creates a parcel delivery order
        params:n/a
        return: n/a
        """
        Parcels.parcels.append(self.parcel)
    
    @staticmethod
    def cancel_parcel(parcel_id):
        """
        Cancels a parcel delivery order
        params: n/a
        returns: parcel created
        """
        Parcels.parcels[parcel_id]['status']='canceled'

    @staticmethod
    def time_details():
        """
        Adds current time, parcel pick up time, parcel delivery time
        params: n/a
        returns:current time, parcel pick up time, parcel delivery time
        """
        

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
    
